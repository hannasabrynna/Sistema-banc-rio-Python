from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(conta, transacao):
        pass

    def adicionar_conta(conta):
        pass

class PessoaFisica(Cliente):
    def __init__(self, endereco,  cpf, nome, data_nascimento):
        super().__init__(endereco) #Chama a implementação da classe pai
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente,):
        self._saldo = 0 #Atributo privado: Nçaos deve ser acessado diretamente fora da classe
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property #Transforma o metodo em atributo que poderá ser acessado posteriormente
    def saldo(self):
        return self.saldo()

    @classmethod #Metodo de classe: Modifica e acessa a classe
    def nova_conta(cls, cliente, numero):
        return(numero, cliente)
    
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
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=500, limite_saques=3 ): ##Sobreescrevendo o construtor Pai
        super().__init__(numero, cliente)  #Chamando novamente a implementação da classe pai - assim podemos utilizar seus metodos
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            #Verifica se a operação é saque e adiciona ao Historico
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if  valor > self.limite:
            print (f"O valor ultrapassa o limite de R${self.limite}")
        elif numero_saques >= self.limite_saques:
            print (f"Voce so pode sacar {self.limite_saques} ao dia")
        else:
            return super().sacar(valor)

        return False
    
    
        
class Historico:
    def __init__(self) :
        self._transacoes = []
 
    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__, #Tipo:nome_da_classe
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"), #Data atual - do dia da transação
            }
        )

class Transacao(ABC): #Classe abstrata

    # @abstractclassmethod #permite que defina-mos o metodo que deve ser implementado por qualquer subclasse (obrigatoriamente)
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

    @property 
    # @abstractproperty
    @abstractmethod #atributo que deve ser implementado por qualquer subclasse (obrigatoriamente)
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)
 

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)
    

