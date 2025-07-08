from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

class Conta:
    def __init__(self, numero, cliente: Cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

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

        @classmethod
        def nova_conta(cls, cliente, numero):
            return cls(numero, cliente)

        def saldo(self):
            return self._saldo
        
        def nova_conta(self, cliente: Cliente, numero: int):
            return Conta(cliente)

        def sacar(self, valor):
            excedeu_saldo = valor > self._saldo

            if excedeu_saldo:
                print("Saldo insuficiente.")
            elif valor > 0:
                self._saldo -= valor
                print('Saque realizado com sucesso.')
                return True
            else:
                print('Valor inválido.')
            return False
        
        def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                print('Deposito realizado com sucesso.')
                return True
            else:
                print('Valor inválido.')
                return False

class ContaCorrente(Conta):
    def __init__(self, cliente, limite = 500, limite_saques = 3):
        super().__init__(cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico._transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print('Valor do saque excede o limite.')
        elif excedeu_saques:
            print('Limite de saques excedido.')
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
    Agencia: \t{self._agencia}
    C/C: \t{self._numero}
    Titular: \t{self._cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data:': datetime.now().strftime('%d-%m-%Y %H:%M:%s')
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)