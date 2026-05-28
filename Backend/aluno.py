from Conectar_Banco import conectar_banco

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

senha_padrao = 'senha1234+'

def email_valido(email):
    partes = email.split('@')
    if len(partes) != 2:
        return False
    return partes[1].split('.') == ['aluno', 'cps', 'gov', 'br']

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']
        self.tipo = data['tipo']
        self.turma = data['turma']

    def buscar(email, senha):
        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s AND senha = %s AND tipo = 'aluno'",
            (email, senha)
        )
        return cursor.fetchone()

    def login(email, senha):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"
        dados = Usuario.buscar(email, senha)
        if not dados:
            return None, "E-mail ou senha incorretos."
        return Usuario(dados), "ok"

    def cadastrar(nome, email, turma):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"
        cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            return None, "E-mail já cadastrado."
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, tipo, turma) VALUES (%s, %s, %s, 'aluno', %s)",
            (nome, email, senha_padrao, turma)
        )
        conexao.commit()
        return Usuario(Usuario.buscar(email, senha_padrao)), "ok"

    def menu():
        opcao = input("1 - Login\n2 - Cadastrar\nOpção: ").strip()

        if opcao == "1":
            email = input("E-mail: ").strip()
            senha = input("Senha: ").strip()
            res = Usuario.login(email, senha)
            try:
                user, status = res
            except Exception:
                print('Erro.')
                return None
            if user:
                return user
            else:
                print(status)
                return None

        elif opcao == "2":
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            turma = input("Turma: ").strip()
            res = Usuario.cadastrar(nome, email, turma)
            try:
                user, status = res
            except Exception:
                if res:
                    print(res)
                    return None
                else:
                    print('Erro.')
                    return None
            if user:
                return user
            else:
                print(status)
                return None