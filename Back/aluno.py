from Back.Conectar_Banco import conectar_banco

# Não abrir conexão ao importar o módulo — cria uma conexão por operação.
senha_padrao = 'senha1234+'

def _get_conn_cursor():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True, buffered=True)
    return conexao, cursor

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
        conexao, cursor = _get_conn_cursor()
        try:
            cursor.execute(
                "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s AND tipo = 'aluno'",
                (email, senha)
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    def login(email, senha):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"
        dados = Usuario.buscar(email, senha)
        if not dados:
            return None, "E-mail ou senha incorretos."
        return Usuario(dados), "ok"

    def cadastrar(nome, email, turma, senha=None):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"

        # Usa senha fornecida pelo frontend; se não informar, usa senha padrão.
        senha_a_usar = senha if senha else senha_padrao

        conexao, cursor = _get_conn_cursor()
        try:
            cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
            if cursor.fetchone():
                return None, "E-mail já cadastrado."
            cursor.execute(
                "INSERT INTO usuario (nome, email, senha_hash, tipo, turma) VALUES (%s, %s, %s, 'aluno', %s)",
                (nome, email, senha_a_usar, turma)
            )
            conexao.commit()
            # buscar novo usuário
            cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha_hash = %s", (email, senha_a_usar))
            dados = cursor.fetchone()
            if not dados:
                return None, "Erro ao criar usuário."
            return Usuario(dados), "ok"
        finally:
            cursor.close()
            conexao.close()

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