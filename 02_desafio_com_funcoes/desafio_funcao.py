
def menu():
    menu= """
    [mku] Criar Usuario
    [mkc] Criar Conta
    [liu] Listar usuarios
    [lic] Listar Contas
    [dep] Depositar
    [sac] Sacar
    [ext] Extrato
    [q] Sair

    """
    return input(menu)

##### Usuario #####

def criar_usuario(usuarios):
    cpf = input("Insira seu CPF (apenas numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n CPF já cadastrado!")
        return
    
    nome = input("Nome Completo: ")
    data_nascismento = input("Data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Enreço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "cpf":cpf, "data_nascimento": data_nascismento, "endereco": endereco})
    print("\n Usuario cadastrado")

def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def listar_usuarios(usuarios):
    for usuario in usuarios:
        lista = f"""
            Nome:{usuario['nome']}
            CPF:{usuario['cpf']}
            DN:{usuario['data_nascimento']}
            Endereço:{usuario['endereco']}
        """
        print(lista)

###### Conta #####

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta Criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado")

def listar_contas(contas):
    for conta in contas:
        lista = f"""
        Agencia: {conta['agencia']}
        Numero_Conta: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}
        """
        print(lista)

##### Operações Bancarias #####

def deposito(valor,saldo,extrato,/):
    
    if valor > 0:
        saldo+=valor
        print(f"Deposito realizado com sucesso!")
        extrato+= f"Deposito no valor de R$ {valor}\n"
    else:
        print("\n Ops! operação falhou, valor Inválido!")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    if  valor > limite:
        print (f"O valor ultrapassa o limite de R${limite}")
    elif numero_saques >= limite_saques:
        print (f"Voce so pode sacar {limite_saques} ao dia")
    elif valor > saldo:
        print ("Saldo insuficiente")
    elif valor > 0:
        saldo-=valor
        numero_saques+=1
        extrato+= f"Saque no valor de R$ {valor}\n"
        print("Saque realizado com sucesso!")
    else:
        print("\n Ops! operação falhou, valor Inválido!") 

    return saldo, extrato, numero_saques

def ver_extrato(saldo,/,*, extrato):
    title = " SEU EXTRATO "
    print(title.center(35, "#"))
    print(f"Saldo: R${saldo}")
    print("Sem movimentaçãoes na sua conta" if not extrato else extrato)
    print("###################################")    

##### Chamando funções ###### 

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    AGENCIA = "0001"
    

    while True:
        opcao = menu()
        #Criar usuario
        if opcao == "mku":
            criar_usuario(usuarios)

        #Criar conta
        elif opcao == "mkc":
            numero_conta = len(contas)+1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        #Listar usuarios
        elif opcao == "liu":
            if usuarios:
                print("########## Lista de usuarios #########")
                listar_usuarios(usuarios)
            else:   
                print("Ainda não há usuarios cadastrados!")

        #Listar contas
        elif opcao == "lic":
            if contas:
                print("########## Lista de Contas #########")
                listar_contas(contas)
            else:   
                print("Ainda não há usuarios cadastrados!")

        #Depositar
        elif opcao == "dep":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(valor, saldo, extrato)

        #Sacar
        elif opcao == "sac":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = saque(
                saldo = saldo,
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                limite_saques=LIMITE_SAQUES, 
                numero_saques=numero_saques
                )

        #Ver Extrato
        elif opcao == "ext":
           ver_extrato(saldo, extrato=extrato)

        #Sair
        elif opcao == "q":
            break
        
        else:
            return "Opcão Invalida"

main()
