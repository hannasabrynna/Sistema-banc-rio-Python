
def menu():
    menu= """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

    """
    return input(menu)

def deposito(valor,saldo,extrato,/):
    
    if valor > 0:
        saldo+=valor
        print(f"Deposito realizado com sucesso!")
        extrato+= f"Deposito no valor de R$ {valor}\n"
    else:
        print("Ops! operação falhou, valor Inválido!")
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
        print("Ops! operação falhou, valor Inválido!") 

    return saldo, extrato, numero_saques

def ver_extrato(saldo,/,*, extrato):
    title = " SEU EXTRATO "
    print(title.center(35, "#"))
    print(f"Saldo: R${saldo}")
    print("Sem movimentaçãoes na sua conta" if not extrato else extrato)
    print("###################################")
    

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = menu()
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(valor, saldo, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = saque(
                saldo = saldo,
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                limite_saques=LIMITE_SAQUES, 
                numero_saques=numero_saques
                )

        elif opcao == "3":
           ver_extrato(saldo, extrato=extrato)
        elif opcao == "4":
            break
        else:
            return "Opcão Invalida"

main()
