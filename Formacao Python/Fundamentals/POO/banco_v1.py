from typing import Final

class SistemaBancario:
   __LIMITE_SAQUE: Final[int] = 3
   def __init__(self):
      self._saldo = 0
      self._extrato = {'saques': [], 'depositos': []}
      self._numero_saques = 0

   @property
   def limite_saque(self):
      return self.__LIMITE_SAQUE
   
   @property
   def saldo(self):
      return self._saldo
      
   def saque(self, valor=0):
      excedeu_limite = valor > 500
      excedeu_saldo = valor > self._saldo
      excedeu_saque = self._numero_saques >= self.__LIMITE_SAQUE
      if not isinstance(valor, float):
         raise ValueError
      if excedeu_limite:
         print('Operação inválida! Não possível sacar um valor maior que R$ 500.00')
      elif excedeu_saldo:
         print('Operação inválida! Saldo insuficiente!')
      elif excedeu_saque:
         print('Operação inválida! Não é possível fazer mais de 3 saques por dia!')
      else:
         self._saldo -= valor
         self._numero_saques += 1
         print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
         self._extrato['saques'].append(f'Saque de R$ {valor:.2f}')

   def deposito(self, valor=0):
      if not isinstance(valor, float):
         raise ValueError
      self._saldo += valor
      print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
      self._extrato['depositos'].append(f'Depósito de R$ {valor:.2f}\n')

   def exibir_extrato(self):
      print('======Extrato======')
      print('SAQUES:')
      for i, saque in enumerate(self._extrato['saques']):
         print(f'{i + 1} - {saque}')
      print('DEPÓSITOS:')
      for i, deposito in enumerate(self._extrato['depositos']):
         print(f'{i + 1} - {deposito}')
      print(f'Saldo atual R$ {self._saldo:.2f}')
   
   def menu(self):
      texto = 'MENU'
      while True:
         print(texto.center(21))
         print('\n[1] - Depósito\n[2] - Saque\n[3] - Exibir extrato\n[4] - Sair do sistema\n')
         opcao = input('Escolha o tipo de transação:\n')
         if opcao == '1':
            valor = float(input('Informe o valor do depósito: '))
            self.deposito(valor)
         elif opcao == '2':
            valor = float(input('Informe o valor do saque: '))
            self.saque(valor)
         elif opcao == '3':
            self.exibir_extrato()
         elif opcao == '4':
            print('Saindo do sistema...')
            break
         else:
            print('Digite uma opção válida!')


if __name__ == '__main__':
   banco = SistemaBancario()
   banco.menu()