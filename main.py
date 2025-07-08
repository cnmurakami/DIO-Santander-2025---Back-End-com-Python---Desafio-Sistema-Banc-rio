from classes import *

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
        cliente_existente = selecionar_cliente(cpf)
        if cliente_existente != None:
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
    clientes.append(PessoaFisica(endereco, cpf, nome, data_nascimento))
    print('Usuário cadastrado com sucesso.')
    return

def selecionar_cliente(cpf):
    global clientes
    try:
        cpf = cpf.replace('.', '').replace('-', '').replace(' ','').strip()
        if len(cpf) != 11:
            raise
        for cliente in clientes:
            if cliente.cpf == cpf:
                return cliente
        raise
    except:
        print('CPF inválido ou nao cadastrado')
        return None

def cadastrar_conta(numero_conta, cliente):
    global contas
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f'Conta criada com sucesso.')

def selecionar_conta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    return cliente.contas[0]
            
def atualizar_extrato(conta_id, valor: float):
    global contas
    conta = contas[conta_id]
    msg = f'Saque realizado: - R$ {-valor:.2f}' if valor < 0 else f'Depósito realizado: + R$ {valor:.2f}'
    conta['extrato'].append(msg)

def deposito(conta):
    global clientes
    try:
        valor = float(input("Insira o valor a depositar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de depósito inválido')
        return
    
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)

def saque(conta):
    global contas
    try:
        valor = float(input("Insira o valor a sacar: R$ "))
        if valor <= 0:
            raise
    except:
        print('Valor de saque inválido')
        return
    
    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)

def exibir_extrato(conta):
    print('\n================== EXTRATO ==================\n')
    if not conta.historico:
        print('Não foram realizadas movimentações.')
    else:
        for i in conta.historico:
            print(i)
    print(f'Saldo atual: R$ {conta.saldo:.2f}')
    print('\n=============================================')

def main():
    global contas, clientes

    cliente_atual = None
    logado = False
    conta_selecionada = None
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
                if cliente_atual != None:
                    logado = True
                    nome = cliente_atual.nome
            elif opcao == 'q':
                break
            else:
                print("Opção inválida")
        elif logado and conta_selecionada == None:
            opcao = input(menu_login)
            opcao = opcao.lower()
            if opcao == 'c':
                cadastrar_conta(cliente_atual)
            elif opcao == 's':
                conta_selecionada = selecionar_conta(cliente_atual)
                if conta_selecionada != None:
                    conta = conta_selecionada
            elif opcao == 'v':
                logado = False
                cliente_atual = None
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
                conta_selecionada = None
                conta = ''
            elif opcao == 'q':
                break
            else:
                print("Opção inválida")

if __name__ == '__main__':
    main()