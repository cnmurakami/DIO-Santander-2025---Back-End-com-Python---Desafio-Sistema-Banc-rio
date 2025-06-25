clientes = [
        # Mock
        # {
        #     'nome': 'aaaaaaaaa',
        #     'cpf': '12345678911',
        #     'data_nascimento': '11/11/1111',
        #     'endereco': 'skjhdfkjsdfdsfsd'
        # },
        # {
        #     'nome': 'bbbbbbbbbb',
        #     'cpf': '12345678912',
        #     'data_nascimento': '11/11/1111',
        #     'endereco': 'skjhdfkjsdfdsfsd'
        # }
    ]
contas = [
    # Mock
    # {'cliente_id': 0, 'ag': '0001', 'saldo': 0.0, 'limite_saques_diarios': 3, 'saques_diarios': 0, 'limite_saque': 500, 'extrato': []},
    # {'cliente_id': 1, 'ag': '0001', 'saldo': 0.0, 'limite_saques_diarios': 3, 'saques_diarios': 0, 'limite_saque': 500, 'extrato': []}
    ]
def cadastrar_cliente():
    global clientes
    try:
        cpf = input('Digite o CPF: ').replace('.', '').replace('-', '').replace(' ','').strip()
        if len(cpf) != 11:
            raise
        for i in clientes:
            if i['cpf'] == cpf:
                raise
    except:
        print('CPF inválido ou já cadastrado.')
        return
    nome = input('Digite o nome: ').strip()
    data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ').replace('-', '/').strip()
    try:
        dia, mes, ano = data_nascimento.split('/')
        if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
            raise
    except:
        print('Data de nascimento inválida')
        return
    endereco = input('Digite o endereco: ').strip()
    clientes.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print('Usuário cadastrado com sucesso.')
    return

def selecionar_cliente(cpf):
    global clientes
    try:
        cpf = cpf.replace('.', '').replace('-', '').replace(' ','').strip()
        if len(cpf) != 11:
            raise
        for i in range(len(clientes)):
            if clientes[i]['cpf'] == cpf:
                return i
        raise
    except:
        print('CPF inválido ou nao cadastrado')
        return -1

def cadastrar_conta(id):
    global contas
    contas.append({'cliente_id': id, 'ag': '0001', 'saldo': 0.0, 'limite_saques_diarios': 3, 'saques_diarios': 0, 'limite_saque': 500, 'extrato': []})
    print(f'Conta criada com sucesso. Número da conta: {len(contas)-1}.')

def selecionar_conta(id):
    global contas
    contas_ativas = {}
    for i in range(len(contas)):
        if contas[i]['cliente_id'] == id:
            contas_ativas[i] = {'ag': contas[i]['ag'], 'saldo': contas[i]['saldo']}
    if len(contas_ativas) == 0:
        print('Não há contas ativas para este usuário')
        return -1
    while True:
        print('\n\nContas ativas:')
        for k in contas_ativas.keys():
            print(f'    Conta: {k}, Agência: {contas_ativas[k]['ag']}, Saldo: {contas_ativas[k]['saldo']:.2f} ')
        escolha = input('\nDigite o numero da conta ou V para voltar: ').lower()
        try:
            if escolha == 'v':
                return -1
            elif int(escolha) in contas_ativas.keys():
                return int(escolha)
            else:
                raise
        except:
            print('Opção inválida')
            
def atualizar_extrato(conta_id, valor: float):
    global contas
    conta = contas[conta_id]
    msg = f'Saque realizado: - R$ {-valor:.2f}' if valor < 0 else f'Depósito realizado: + R$ {valor:.2f}'
    conta['extrato'].append(msg)

def deposito(id_conta):
    global contas
    conta = contas[id_conta]
    try:
        valor = float(input("Insira o valor a depositar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de depósito inválido')
        return
    conta['saldo'] += valor
    print(f'Deposito efetuado com sucesso. Saldo: {conta['saldo']:.2f}')
    atualizar_extrato(id_conta, valor)

def saque(id_conta):
    global contas
    conta = contas[id_conta]
    if conta['saques_diarios'] >= conta['limite_saques_diarios']:
        print(f'Operação negada. Limite de saques diários atingido.')
        return
    try:
        valor = float(input("Insira o valor a sacar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de saque inválido')
        return
    if valor > conta['limite_saque']:
        print(f'Operação negada. Valor máximo permitido: R$ {conta['limite_saque']:.2f}')
        return
    if valor > conta['saldo']:
        print(f'Operação negada. Saldo insuficiente.')
        return
    conta['saldo'] -= valor
    conta['saques_diarios'] += 1
    print(f'Saque realizado com sucesso. Saldo: {conta['saldo']:.2f}')
    atualizar_extrato(id_conta, -valor)

def exibir_extrato(id_conta):
    global contas
    conta = contas[id_conta]
    print('\n================== EXTRATO ==================\n')
    if not conta['extrato']:
        print('Não foram realizadas movimentações.')
    else:
        for i in conta['extrato']:
            print(i)
    print(f'Saldo atual: R$ {conta['saldo']:.2f}')
    print('\n=============================================')

def main():
    global contas, clientes

    cliente_atual = -1
    logado = False
    conta_selecionada = -1
    nome = ''
    conta = ''

    while True:

        menu = """

Menu:
    [c] Cadastrar usuário
    [l] Login
    [q] Sair

"""

        menu_login = f"""

Usuário: {nome}
Menu:
    [c] Criar nova conta
    [s] Selecionar conta
    [v] Voltar
    [q] Sair

"""

        menu_conta = f"""

Usuário: {nome}
Conta: {conta}
Menu:
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [v] Voltar
    [q] Sair

==> 
"""
    
        if not logado:
            opcao = input(menu)
            opcao = opcao.lower()

            if opcao == 'c':
                cadastrar_cliente()
            elif opcao == 'l':
                cpf = input('Digite o CPF: ')
                cliente_atual = selecionar_cliente(cpf)
                if cliente_atual != -1:
                    logado = True
                    nome = clientes[cliente_atual]['nome']
            elif opcao == 'q':
                break
            else:
                print("Opção inválida")
        elif logado and conta_selecionada == -1:
            opcao = input(menu_login)
            opcao = opcao.lower()
            if opcao == 'c':
                cadastrar_conta(cliente_atual)
            elif opcao == 's':
                conta_selecionada = selecionar_conta(cliente_atual)
                if conta_selecionada != -1:
                    conta = conta_selecionada
            elif opcao == 'v':
                logado = False
                cliente_atual = -1
                nome = ''
            elif opcao == 'q':
                break
            else:
                print("Opção inválida")
        else:
            opcao = input(menu_conta)
            opcao = opcao.lower()
            if opcao == 'c':
                cadastrar_cliente(conta_selecionada)
            elif opcao == 'd':
                deposito(conta_selecionada)
            elif opcao == 's':
                saque(conta_selecionada)
            elif opcao == 'e':
                exibir_extrato(conta_selecionada)
            elif opcao == 'v':
                conta_selecionada = -1
                conta = ''
            elif opcao == 'q':
                break
            else:
                print("Opção inválida")

if __name__ == '__main__':
    main()