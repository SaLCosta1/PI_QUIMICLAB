from Back.Conectar_Banco import conectar_banco

senha_padrao = 'senha1234+'

def _get_conn_cursor():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True, buffered=True)
    return conexao, cursor

def email_valido(email):
    email = email.strip().lower()
    return email.endswith('@cps.sp.gov.br')

class Professor:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']

    @staticmethod
    def buscar(email, senha):
        conexao, cursor = _get_conn_cursor()
        try:
            cursor.execute(
                "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s AND tipo = 'professor'",
                (email, senha)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"[professor.buscar] Erro ao buscar professor: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def login(email, senha):
        try:
            if not email_valido(email):
                return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"
            dados = Professor.buscar(email, senha)
            if not dados:
                return None, "E-mail ou senha incorretos."
            return Professor(dados), None
        except Exception as e:
            print(f"[professor.login] Erro ao fazer login: {e}")
            return None, f"Erro ao fazer login: {str(e)}"

    @staticmethod
    def cadastrar(nome, email):
        try:
            if not email_valido(email):
                return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"
            conexao, cursor = _get_conn_cursor()
            try:
                cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
                if cursor.fetchone():
                    return None, "E-mail já cadastrado."
                cursor.execute(
                    "INSERT INTO usuario (nome, email, senha_hash, tipo) VALUES (%s, %s, %s, 'professor')",
                    (nome, email, senha_padrao)
                )
                conexao.commit()
                cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha_hash = %s", (email, senha_padrao))
                dados = cursor.fetchone()
                if not dados:
                    return None, "Erro ao criar usuário."
                return Professor(dados), None
            finally:
                cursor.close()
                conexao.close()
        except Exception as e:
            print(f"[professor.cadastrar] Erro ao cadastrar professor: {e}")
            return None, f"Erro ao cadastrar: {str(e)}"
