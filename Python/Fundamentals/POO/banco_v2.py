from typing import Final

class SistemaBancario:
   __LIMITE_SAQUE: Final[int] = 3
   __AGENCIA: Final[str] = '0001'
   def __init__(self):
      self._usuarios = []
      self._contas = []
      self._numero_contas = 1

   @property
   def limite_saque(self):
      return self.__LIMITE_SAQUE
   
   @property
   def agencia(self):
      return self.__AGENCIA

   def filtrar_usuarios(self, cpf):
      usuarios_filtrados = [usuario for usuario in self._usuarios if usuario['cpf'] == cpf]
      return usuarios_filtrados[0] if usuarios_filtrados else None

   def criar_usuario(self):
      cpf = input('Informe o CPF (somente números)\n')
      usuario = self.filtrar_usuarios(cpf)
      
      if usuario:
         print('CPF já cadastrado!')
         return
      print('DADOS PESSOAIS')
      nome = input('Nome: ').strip()
      sobrenome = input('Sobrenome: ')
      nome_completo = f'{nome} {sobrenome}'
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
      novo_usuario = {'nome_completo': nome_completo, 'data_nascimento': data_nascimento, 'endereco': endereco,'cpf': cpf, 'contas': []}
      self._usuarios.append(novo_usuario)
      print('Usuário cadastrado com sucesso!!')

   def criar_conta(self):
      cpf = input('Informe o CPF (somente números)\n')
      usuario = self.filtrar_usuarios(cpf)

      if usuario:
         
         return self.extrair_usuario_conta(usuario)
      print('Usuário não encontrado!')

   def extrair_usuario_conta(self, usuario):
      saldo = 0
      conta = {'agencia': self.__AGENCIA, 'numero': self._numero_contas, 'saldo': saldo, 'saques':[], 'depositos': [], 'titular': usuario['nome_completo']}
      usuario['contas'].append(conta)
      self._numero_contas += 1
      print('Conta criada com sucesso!')
      self._contas.append(conta)
      return conta

   def listar_contas_usuario(self, cpf):
      usuario = self.filtrar_usuarios(cpf)
      if not usuario:
         print('Usuário não encontrado!')
         return
      print(f"Titular: {usuario['nome_completo']}")
      for conta in usuario['contas']:
         print(f"Agência: {conta['agencia']} Nº: {conta['numero']} - Saldo: R$ {conta['saldo']:.2f} - Nº de saques: {len(conta['saques'])}")

   def listar_contas(self):
      for conta in self._contas:
         print(f"Titular: {conta['titular']} Agência: {conta['agencia']} - Nº {conta['numero']}")

   def saque(self, cpf):
      usuario = self.filtrar_usuarios(cpf)

      if not usuario:
         print('Usuário não encontrado!')
         return

      self.listar_contas_usuario(cpf)
      numero = int(input('Informe o número da conta:\n'))

      conta = self.buscar_conta_por_numero(usuario, numero)

      if not conta:
         print('Conta não encontrada!')
         return

      valor = float(input('Informe o valor do saque:\n'))

      if valor <= 0:
         print('Valor inválido! O saque deve ser maior que zero.')
         return

      excedeu_limite = valor > 500
      excedeu_saldo = valor > conta['saldo']
      excedeu_saque = len(conta['saques']) >= self.__LIMITE_SAQUE

      if excedeu_limite:
         print('Operação inválida! Não é possível sacar um valor maior que R$ 500.00')
      elif excedeu_saldo:
         print('Operação inválida! Saldo insuficiente!')
      elif excedeu_saque:
         print('Operação inválida! Não é possível fazer mais de 3 saques por dia!')
      else:
         conta['saldo'] -= valor
         conta['saques'].append(valor)
         print(f'Saque de R$ {valor:.2f} realizado com sucesso!')

   def buscar_conta_por_numero(self, usuario, numero):
      return next((conta for conta in usuario['contas'] if conta['numero'] == numero),
         None,
      )
   
   def deposito(self, cpf):
      usuario = self.filtrar_usuarios(cpf)

      if not usuario:
         print('Usuário não encontrado!')
         return

      self.listar_contas_usuario(cpf)
      numero = int(input('Informe o número da conta:\n'))

      conta = self.buscar_conta_por_numero(usuario, numero)

      if not conta:
         print('Conta não encontrada!')
         return

      valor = float(input('Informe o valor do depósito:\n'))
      if valor <= 0:
         print('Valor inválido! O depósito deve ser maior que zero.')
         return

      conta['saldo'] += valor
      conta['depositos'].append(valor)
      print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')


   def exibir_extrato(self, cpf):
      usuario = self.filtrar_usuarios(cpf)

      if not usuario:
         print('Usuário não encontrado!')
         return

      self.listar_contas_usuario(cpf)
      numero = int(input('Informe o número da conta para ver o extrato:\n'))

      conta = self.buscar_conta_por_numero(usuario, numero)

      if not conta:
         print('Conta não encontrada!')
         return

      print('\n====== Extrato ======')
      print(f"Titular: {usuario['nome_completo']}")
      print(f"Agência: {conta['agencia']} - Conta Nº: {conta['numero']}")
      print('\nSAQUES:')
      if conta['saques']:
         for i, saque in enumerate(conta['saques']):
            print(f'{i + 1} - R$ {saque:.2f}')
      else:
         print('Nenhum saque realizado.')

      print('\nDEPÓSITOS:')
      if conta['depositos']:
         for i, deposito in enumerate(conta['depositos']):
            print(f'{i + 1} - R$ {deposito:.2f}')
      else:
         print('Nenhum depósito realizado.')

      print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")


   def menu(self):
      texto = 'MENU'
      while True:
         print(texto.center(28)+'\n')
         print('[1] - Criar usuário\n[2] - Criar conta\n[3] - Listar contas\n[4] - Depositar\n[5] - Sacar\n[6] - Extrato\n[7] - Listar todas as contas\n[8] - Sair do sistema\n')
         opcao = input('Escolha o tipo de transação:\n')
         if opcao == '1':
            self.criar_usuario()
         elif opcao == '2':
            self.criar_conta()
         elif opcao == '4':
            cpf = input('Informe o CPF do titular da conta (apenas números)\n')
            self.deposito(cpf)
         elif opcao == '5':
            cpf = input('Informe o CPF do titular da conta (apenas números)\n')
            self.saque(cpf)
         elif opcao == '6':
            cpf = input('Informe o CPF do titular da conta (apenas números)\n')
            self.exibir_extrato(cpf)
         elif opcao == '7':
            self.listar_contas()         
         elif opcao == '8':
            print('Saindo do sistema...')
            break
         else:
            print('Digite uma opção válida!')


if __name__ == '__main__':
   banco = SistemaBancario()
   banco.menu()