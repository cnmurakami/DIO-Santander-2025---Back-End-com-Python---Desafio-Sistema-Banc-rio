extrato = []
saldo = 2000.0
limite_saques_diarios = 3
saques_diarios = 0
limite_saque = 500

def atualizar_extrato(valor: float):
    global saldo
    msg = f'Saque realizado: - R$ {-valor:.2f}' if valor < 0 else f'Depósito realizado: + R$ {valor:.2f}'
    # msg += '\nSaldo atual: {saldo}'
    extrato.append(msg)

def deposito():
    try:
        valor = float(input("Insira o valor a depositar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de depósito inválido')
        return
    global saldo
    saldo += valor
    print(f'Deposito efetuado com sucesso. Saldo: {saldo:.2f}')
    atualizar_extrato(valor)

def saque():
    global saques_diarios, limite_saques_diarios
    if saques_diarios >= limite_saques_diarios:
        print(f'Operação negada. Limite de saques diários atingido.')
        return
    try:
        valor = float(input("Insira o valor a sacar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de saque inválido')
        return
    global limite_saque
    if valor > limite_saque:
        print(f'Operação negada. Valor máximo permitido: R$ {limite_saque:.2f}')
        return
    global saldo
    if valor > saldo:
        print(f'Operação negada. Saldo insuficiente.')
        return
    saldo -= valor
    saques_diarios += 1
    print(f'Saque realizado com sucesso. Saldo: {saldo:.2f}')
    atualizar_extrato(-valor)

def exibir_extrato():
    global extrato, saldo
    print('\n================== EXTRATO ==================\n')
    if not extrato:
        print('Não foram realizadas movimentações.')
    else:
        for i in extrato:
            print(i)
    print(f'Saldo atual: R$ {saldo:.2f}')
    print('\n=============================================')

def main():
    menu = """

Menu:
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

==> 
"""
    while True:
        opcao = input(menu)
        opcao = opcao.lower()
        if opcao == 'd':
            deposito()
        elif opcao == 's':
            saque()
        elif opcao == 'e':
            exibir_extrato()
        elif opcao == 'q':
            break
        else:
            print("Opção inválida")

if __name__ == '__main__':
    main()