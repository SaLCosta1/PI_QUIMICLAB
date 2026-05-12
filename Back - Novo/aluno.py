import mysql.connector
from Conectar_Banco import conectar_banco 

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

class Usuario:
    def __init__(self, data):
        # Tente usar letras minúsculas se as maiúsculas falharem
        self.id = data.get('id') or data.get('ID')
        self.nome = data.get('nome') or data.get('Nome')
        self.turma = data.get('turma') or data.get('Turma')
        self.email = data.get('email') or data.get('Email')
        self.senha = data.get('senha') or data.get('Senha')
        self.pontos = data.get('pontuacao') or data.get('Pontuacao')

    @staticmethod
    def verificar_logins(email, turma, nome):
        # Ordem: Email, Turma, Nome (deve bater com o execute abaixo)
        sql = "SELECT * FROM USUARIO WHERE Email = %s AND Turma = %s AND Nome = %s"
        cursor.execute(sql, (email, turma, nome))
        return cursor.fetchone()

    @staticmethod
    def salvar_login(nome, turma, email):
        # REMOVIDO 'Senha' daqui para o banco usar o DEFAULT 'senha1234+'
        sql = "INSERT INTO Usuario (Nome, Turma, Email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, turma, email))
        conexao.commit()
    
    @classmethod
    def login(cls):
        print("\n--- LOGIN ---")
        nome = input("Nome Completo: ").strip()
        email = input("Email: ").strip()
        turma = input("Turma: ").strip().upper()
        # Se for usar senha no futuro, precisa validar no WHERE do verificar_logins
        
        logins = cls.verificar_logins(email, turma, nome)
        
        if logins:
            print(f"Login Realizado! Bem-vindo, {nome}!")
            return cls(logins)
        else:
            print("Usuário não encontrado.")
            return None
    
    @classmethod
    def cadastrar(cls):
        print("\n--- CADASTRO ---")
        nome = input("Nome Completo: ").strip()
        email = input("Email: ").strip()
        turma = input("Turma: ").strip().upper()

        usuario_existente = cls.verificar_logins(email, turma, nome)

        if usuario_existente:
            print(f"Usuário já cadastrado! Entrando como {nome}...")
            return cls(usuario_existente)
        
        cls.salvar_login(nome, turma, email)
        print(f"Usuário {nome} cadastrado com sucesso!")
        
        dados = cls.verificar_logins(email, turma, nome)
        return cls(dados)

    @classmethod
    def menu(cls):
        print("\n=== Sistema de Login ===")
        print("1 - Login")
        print("2 - Cadastrar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            return cls.login()
        elif opcao == "2":
            return cls.cadastrar()
        else:
            print("Opção inválida.")
            return None
