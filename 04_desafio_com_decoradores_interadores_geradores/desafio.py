
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap #fornece funções para formatar parágrafos de texto

class ContaIterador:
    def __init__(self, contas): #Construtor
        self.contas = contas
        self._index = 0

    def __iter__(self): #Define o valor a ser iterado
        pass

    def __next__(self):
        try:
            conta = self.contas[self._index] #conta[indice] para imprimir as contas
            return f"""\ 
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration #para a iteraçao
        finally:
            self._index += 1 #acrescenta +1 em index

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        
        if valor > self.saldo:
            print ("Saldo insuficiente")
        elif valor > 0:
            self.saldo-=valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("\n Ops! operação falhou, valor Inválido!") 
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo+=valor
            print(f"Deposito realizado com sucesso!")
        else:
            print("\n Ops! operação falhou, valor Inválido!")
            return False
        
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            #Verifica se a operação é saque e adiciona ao Historico
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if  valor > self._limite:
            print (f"O valor ultrapassa o limite de R${self.limite}")
        elif numero_saques >= self._limite_saques:
            print (f"Voce so pode sacar {self._limite_saques} ao dia")
        else:
            return super().sacar(valor)

        return False
    

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__, #Pega o tipo da transacao (saque ou deposito)
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            #Verifica se "tipo_transacao" é None (ou seja, nenhum e none é o valor padrão)
            # e se transacao["tipo"] o tipo de transação que foi passado é o mesmo da variael "tipo_transação"
            #caso uma das duas seja True elas ficaram guardadas para gerar o relatorio
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao #Retorno (em gerador)


class Transacao(ABC): #Classe Abstrata
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(func): # Função Decorador que recebe uma função como parametro
    def envelope(*args, **kwargs): #Usamos *args, **kwargs quando queremos passar argumentos
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}") #Printa a hora e o nome da função(saque ou deposito) em maiusculo
        return resultado

    return envelope


def menu():
    menu= """
    [mku] Criar Usuario
    [mkc] Criar Conta
    [lic] Listar Contas
    [dep] Depositar
    [sac] Sacar
    [ext] Extrato
    [q] Sair

    """
    return input(menu)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    #FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

@log_transacao #Chama a função (decorador) "log_transao" e passa "depositar" como parametro
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

@log_transacao #Decorador
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

@log_transacao #Decorador
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado! ")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    #itera sobre todas as transações retornadas pelo método gerar_relatorio do objeto historico associado a conta, filtrando apenas as transações do tipo "saque".
    for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque"):
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao #Decorador
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n Já existe cliente com esse CPF! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

@log_transacao #Decorador
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado, fluxo de criação de conta encerrado! ")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

@log_transacao #Decorador
def listar_contas(contas):
    for conta in ContaIterador: #Classe Iterador
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "dep":
            depositar(clientes)

        elif opcao == "sac":
            sacar(clientes)

        elif opcao == "ext":
            exibir_extrato(clientes)

        elif opcao == "mku":
            criar_cliente(clientes)

        elif opcao == "mkc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lic":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            return "Opcão Invalida"


main()