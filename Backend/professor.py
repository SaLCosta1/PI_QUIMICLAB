from Conectar_Banco import conectar_banco

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

senha_padrao = 'senha1234+'

def email_valido(email):
    partes = email.split('@')
    if len(partes) != 2:
        return False
    return partes[1].split('.') == ['cps', 'sp', 'gov', 'br']

class Professor:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']

    def buscar(email, senha):
        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s AND tipo = 'professor'",
            (email, senha)
        )
        return cursor.fetchone()

    def login(email, senha):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"
        dados = Professor.buscar(email, senha)
        if not dados:
            return None, "E-mail ou senha incorretos."
        return Professor(dados), "ok"

    def cadastrar(nome, email):
        if not email_valido(email):
            return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"
        cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            return None, "E-mail já cadastrado."
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha_hash, tipo) VALUES (%s, %s, %s, 'professor')",
            (nome, email, senha_padrao)
        )
        conexao.commit()
        return Professor(Professor.buscar(email, senha_padrao)), "ok"
