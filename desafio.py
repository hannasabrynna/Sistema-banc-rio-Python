menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

"""
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
deposito = 0
saque = 0

while True:

    opcao = input(menu)

###### OPERAÇÃO DE DEPOSITO ######

    if opcao == "1":
        deposito = float(input("Digite o valor:"))

        if deposito > 0:
            saldo+=deposito
            print(f"Deposito realizado com sucesso!")

            extrato+= f"Deposito no valor de R$ {deposito}\n"
        else:
            print("Ops! operação falhou, valor Inválido!")

###### OPERAÇÃO DE SAQUE ######

    elif opcao == "2":

        saque = float(input("Digite o valor:"))

        if  saque > limite:
            print (f"O valor ultrapassa o limite de R${limite}")
        elif numero_saques >= LIMITE_SAQUES:
            print (f"Voce so pode sacar {LIMITE_SAQUES} ao dia")
        elif saque > saldo:
            print ("Saldo insuficiente")
        elif saque > 0:
            saldo-=saque
            numero_saques+=1
            extrato+= f"Saque no valor de R$ {saque}\n"
            print("Saque realizado com sucesso!")
        else:
            print("Ops! operação falhou, valor Inválido!")   

###### VIZUALIZAR EXTRATO ######

    elif opcao == "3":
        title = " SEU EXTRATO "
        print(title.center(35, "#"))
        print(f"Saldo: R${saldo}")
        print("Sem movimentaçãoes na sua conta" if not extrato else extrato)
        print("###################################")

    elif opcao == "4":
        break

    else:
        print("Opção Inválida")