import re
from Conectar_Banco import conectar_banco

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

def email_valido(email):
    padrao = r'^[a-z]+\.[a-z]+@luno\.cps\.gov\.br$'
    return re.match(padrao, email)

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']
        self.tipo = data['tipo']
        self.turma = data['turma']

    def verificar_login(email, senha):
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha_hash = %s", (email, senha))
        return cursor.fetchone()

    def salvar_usuario(nome, email, senha, turma):
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha_hash, tipo, turma) VALUES (%s, %s, %s, 'aluno', %s)",
            (nome, email, senha, turma)
        )
        conexao.commit()

    def login():
        print("\n- Login -")
        email = input("Email: ").strip()

        if not email_valido(email):
            print("Email inválido")
            return None

        senha = input("Senha: ").strip()

        dados = Usuario.verificar_login(email, senha)
        if dados:
            print(f"Bem-vindo, {dados['nome']}!")
            return Usuario(dados)
        else:
            print("Email ou senha incorretos")
            return None

    def cadastrar():
        print("\n- Cadastrar -")
        nome = input("Nome completo: ").strip()
        email = input("Email: ").strip()

        if not email_valido(email):
            print("Email inválido")
            return None

        senha = input("Senha: ").strip()
        turma = input("Turma: ").strip().upper()

        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        existente = cursor.fetchone()

        if existente:
            print("Email já cadastrado.")
            return None

        Usuario.salvar_usuario(nome, email, senha, turma)
        dados = Usuario.verificar_login(email, senha)
        print(f"Cadastro realizado! Bem-vindo, {nome}!")
        return Usuario(dados)

    def menu():
        print("\n - Menu - ")
        print("1 - Login")
        print("2 - Cadastrar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            return Usuario.login()
        elif opcao == "2":
            return Usuario.cadastrar()
        else:
            print("Opção inválida.")
            return None