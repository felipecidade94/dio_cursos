import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
   def __init__(self, endereco):
      self.endereco = endereco
      self.contas = []
   
   def realizar_transacao(self, conta, transacao):
      if isinstance(conta, Conta) and isinstance(transacao, Transacao):
         transacao.registrar(conta)

   def adicionar_conta(self, conta):
      if isinstance(conta, Conta):
         self.contas.append(conta)

class PessoaFisica(Cliente):
   def __init__(self, nome, data_nascimento, cpf, endereco):
      super().__init__(endereco)
      self._nome = nome
      self._data_nascimento = data_nascimento
      self._cpf = cpf

   @property
   def nome(self):
      return self._nome

   @property
   def data_nascimento(self):
      return self._data_nascimento


   @property
   def cpf(self):
      return self._cpf


class Conta:
   def __init__(self, numero, cliente: Cliente):
      self._saldo = 0
      self._agencia = '0001'
      self._numero = numero
      self._cliente = cliente
      self._historico = Historico()
      
   @property
   def saldo(self):
      return self._saldo
   
   @property
   def agencia(self):
      return self._agencia
   
   @property
   def numero(self):
      return self._numero
   
   @property
   def cliente(self):
      return self._cliente
   
   @property
   def historico(self):
      return self._historico
   @classmethod
   def nova_conta(cls, numero, cliente):
      return cls(numero, cliente)

   def sacar(self, valor):
      saldo = self.saldo
      excedeu_saldo = valor > saldo
      
      if excedeu_saldo:
         print('Saldo insuficiente!')
      elif valor > 0:
         self._saldo -= valor
         print('Saque realizado com sucesso!')
         return True
      else:
         print('Valor informado inválido!')
      
      return False

   def depositar(self, valor):
      if valor > 0:
         self._saldo += valor
         print('Depósito realizado com sucesso!')
         return True
      else:
         print('Valor informado inválido!')
      return False

class ContaCorrente(Conta):
   def __init__(self, numero, cliente, limite=500, limite_saques=3):
      super().__init__(numero, cliente)
      self._limite = limite
      self._limite_saques = limite_saques
      
   def sacar(self, valor):
      numero_saques = len(
         [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
      )
      excedeu_limite = valor > self._limite
      excedeu_saques = numero_saques >= self._limite_saques
      
      if excedeu_limite:
         print(f'Limite de saque excedido! Insira um valor até R$ {self._limite:.2f}')
      elif excedeu_saques:
         print('Limite de saques diários excedido!')
      else:
         return super.sacar(valor)
      return False

   def __str__(self):
      
      return f'''
         Agência:\t{self.agencia}
         C/C:\t\t{self.numero}
         Titular:\t{self.cliente.nome}
      '''

class Transacao(ABC):
   @property
   @abstractmethod
   def valor(self):
      pass

   @abstractmethod
   def registrar(self, conta):
      pass

class Historico:
   def __init__(self):
      self._transacoes = []
   
   @property
   def transacoes(self):
      return self._transacoes
   
   def adicionar_transacao(self, transacao):
      if isinstance(transacao, Transacao):
         self._transacoes.append(
            {
               'tipo': transacao.__class__.__name__,
               'valor': transacao.valor,
               'data': datetime.now().strftime('%d/%m/%y %H:%M:%S')
            }
         )

class Saque(Transacao):
   def __init__(self, valor):
      self._valor = valor

   @property
   def valor(self):
      return self._valor
   
   def registrar(self, conta):
      if isinstance(conta, Conta):
         sucesso_transacao = conta.sacar(self._valor)
      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
   def __init__(self, valor):
      self._valor = valor

   @property
   def valor(self):
      return self._valor

   def registrar(self, conta):
      if isinstance(conta, Conta):
         sucesso_transacao = conta.depositar(self._valor)
      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)
         
class Banco:   
   def filtrar_clientes(self, clientes, cpf):
      if isinstance(clientes, list):
         clientes_filtrados = [cliente for cliente in clientes if isinstance(cliente, Cliente) and cliente.cpf == cpf]
         if clientes_filtrados:
            return clientes_filtrados[0]
      return
   
   def recuperar_conta(self, cliente):
      if isinstance(cliente, Cliente):
         if cliente.contas:
            return cliente.contas[0]
         print('Cliente não possui conta!')
         return
      else:
         print('Foi informado um valor inválido!')
      return
   
   def depositar(self, clientes):
      cpf = input('Informe o CPF do cliente (somente os números)\n').strip()
      cliente = self.filtrar_clientes(clientes, cpf)
      
      if not cliente:
         print('Cliente não encontrado!')
         return
      
      conta = self.recuperar_conta(cliente)
      if not conta:
         return
      
      valor = float(input('Informe o valor do depósito:\n'))
      transacao = Deposito(valor)
      cliente.realizar_transacao(conta, transacao)

   def sacar(self, clientes):
      cpf = input('Informe o CPF do cliente (somente os números)\n').strip()
      cliente = self.filtrar_clientes(clientes, cpf)
      
      if not cliente:
         print('Cliente não encontrado!')
         return
      
      conta = self.recuperar_conta(cliente)
      if not conta:
         return
      valor = float(input('Informe o valor do saque:\n'))
      transacao = Saque(valor)
      cliente.realizar_transacao(conta, transacao)
   
   def exibir_extrato(self,clientes):
      if isinstance(clientes, list):
         cpf = input('Informe o CPF do cliente (somente os números)\n').strip()
         cliente = self.filtrar_clientes(clientes, cpf)
         
         if not cliente:
            print('Cliente não encontrado!')
            return
         
         conta = self.recuperar_conta(cliente)
         if not conta:
            return
         
         print('======EXTRATO======')
         if isinstance(conta, Conta):
            transacoes = conta.historico.transacoes
            extrato = ''

            if not transacoes:
               extrato = 'Não houveram movimentações nessa conta!'
            else:
               for transacao in transacoes:
                  extrato += f"\n{transacao['tipo']}\n\tR$ {transacao['valor']:.2f}"
            print(extrato)
            print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
      else:
         print('Foi informado um valor inválido!')
      return
   
   def criar_cliente(self, clientes):
      if isinstance(clientes, list):
         cpf = input('Informe o seu CPF (somente números):\n').strip()
         cliente = self.filtrar_clientes(clientes, cpf)
         
         if cliente:
            print('Já existe um usuário com esse cadastrado com esse CPF!')
            return
         print('======DADOS PESSOAIS======')
         primeiro_nome = input('Informe seu primeiro nome:\n').strip()
         sobrenome = input('Informe seu sobrenome:\n').strip()
         nome = f'{primeiro_nome} {sobrenome}'
         dia = input('Dia: ').strip()
         mes = input('Mês: ').strip()
         ano = input('Ano: ').strip()
         data_nascimento = f'{dia}/{mes}/{ano}'
         logradouro = input('Logradouro: ')
         numero = input('Número: ')
         bairro = input('Bairro: ')
         cidade = input('Cidade: ')
         estado = input('Estado (Sigla): ')
         pais = input('País: ')
         endereco = f'{logradouro}, {numero}, {bairro}, {cidade}/{estado}, {pais}'
         cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf, endereco=endereco)
         clientes.append(cliente)
         print("\n=== Cliente criado com sucesso! ===")
         
   def criar_conta(self, numero_conta, clientes, contas):
      if isinstance(clientes, list) and isinstance(contas, list):
         cpf = input('Informe o CPF do cliente (somente os números)\n').strip()
         cliente = self.filtrar_clientes(clientes, cpf)
         
         if not cliente:
            print('Cliente não encontrado!')
            return
         conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
         contas.append(conta)
         cliente.contas.append(conta)
         print("\n=== Conta criada com sucesso! ===")
      else:
         print('Foi informado um valor inválido!')
         return
      
   def listar_contas(self, contas):
      if isinstance(contas, list):
         for conta in contas:
            print('='*100)
            print(textwrap.dedent(str(conta)))

def menu():
   menu = """\n
   ================ MENU ================
   [d]\tDepositar
   [s]\tSacar
   [e]\tExtrato
   [nu]\tNovo usuário
   [nc]\tNova conta
   [lc]\tListar contas   
   [q]\tSair
   => """
   return input(textwrap.dedent(menu))

def main():
   contas = []
   clientes = []
   banco = Banco()
   while True:
      opcao = menu()
      
      if opcao == 'd':
         banco.depositar(clientes)
      elif opcao == 's':
         banco.sacar(clientes)
      elif opcao == 'e':
         banco.exibir_extrato(clientes)
      elif opcao == 'nu':
         banco.criar_cliente(clientes)
      elif opcao == 'nc':
         numero_conta = len(contas) + 1
         banco.criar_conta(numero_conta=numero_conta, clientes=clientes, contas=contas)
      elif opcao == 'lc':
         banco.listar_contas(contas)
      elif opcao == 'q':
         print('Saindo...')
         break
      else:
         print('Opção inválida!')
         
main()