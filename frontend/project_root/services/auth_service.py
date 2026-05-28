# =========================================================
# services/auth_service.py
# Login e cadastro de alunos e professores.
# Baseado em aluno.py e professor.py do Arthur.
# =========================================================
from services.db import conectar, hash_senha


def _email_valido_aluno(email: str) -> bool:
    partes = email.split("@")
    if len(partes) != 2:
        return False
    return partes[1].split(".") == ["aluno", "cps", "gov", "br"]


def _email_valido_prof(email: str) -> bool:
    partes = email.split("@")
    if len(partes) != 2:
        return False
    return partes[1].split(".") == ["cps", "sp", "gov", "br"]


# ---------------------------------------------------------
# ALUNO
# ---------------------------------------------------------

def login_aluno(email: str, senha: str):
    """
    Retorna (dict_usuario, None) em caso de sucesso
    ou (None, mensagem_de_erro).
    """
    if not _email_valido_aluno(email):
        return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"

    conn = conectar()
    if not conn:
        return None, "Não foi possível conectar ao banco de dados."

    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            "SELECT * FROM usuario WHERE email=%s AND senha_hash=%s AND tipo='aluno'",
            (email, hash_senha(senha)),
        )
        dados = cur.fetchone()
        if not dados:
            return None, "E-mail ou senha incorretos."
        return dados, None
    finally:
        conn.close()


def cadastrar_aluno(nome: str, email: str, turma: str):
    """
    Cadastra novo aluno com senha padrão 'senha1234+'.
    Retorna (dict_usuario, None) ou (None, mensagem_erro).
    """
    SENHA_PADRAO = "senha1234+"

    if not _email_valido_aluno(email):
        return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.gov.br"

    conn = conectar()
    if not conn:
        return None, "Não foi possível conectar ao banco de dados."

    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT id_usuario FROM usuario WHERE email=%s", (email,))
        if cur.fetchone():
            return None, "E-mail já cadastrado."

        cur.execute(
            "INSERT INTO usuario (nome, email, senha_hash, tipo, turma) VALUES (%s,%s,%s,'aluno',%s)",
            (nome, email, hash_senha(SENHA_PADRAO), turma),
        )
        conn.commit()

        cur.execute(
            "SELECT * FROM usuario WHERE email=%s AND tipo='aluno'", (email,)
        )
        return cur.fetchone(), None
    finally:
        conn.close()


# ---------------------------------------------------------
# PROFESSOR
# ---------------------------------------------------------

def login_prof(email: str, senha: str):
    if not _email_valido_prof(email):
        return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"

    conn = conectar()
    if not conn:
        return None, "Não foi possível conectar ao banco de dados."

    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            "SELECT * FROM usuario WHERE email=%s AND senha_hash=%s AND tipo='professor'",
            (email, hash_senha(senha)),
        )
        dados = cur.fetchone()
        if not dados:
            return None, "E-mail ou senha incorretos."
        return dados, None
    finally:
        conn.close()


def cadastrar_prof(nome: str, email: str):
    SENHA_PADRAO = "senha1234+"

    if not _email_valido_prof(email):
        return None, "E-mail inválido. Use nome.sobrenome@cps.sp.gov.br"

    conn = conectar()
    if not conn:
        return None, "Não foi possível conectar ao banco de dados."

    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT id_usuario FROM usuario WHERE email=%s", (email,))
        if cur.fetchone():
            return None, "E-mail já cadastrado."

        cur.execute(
            "INSERT INTO usuario (nome, email, senha_hash, tipo) VALUES (%s,%s,%s,'professor')",
            (nome, email, hash_senha(SENHA_PADRAO)),
        )
        conn.commit()

        cur.execute(
            "SELECT * FROM usuario WHERE email=%s AND tipo='professor'", (email,)
        )
        return cur.fetchone(), None
    finally:
        conn.close()


def trocar_senha(id_usuario: int, senha_atual: str, nova_senha: str):
    """Troca a senha do usuário após validar a senha atual."""
    conn = conectar()
    if not conn:
        return False, "Não foi possível conectar ao banco de dados."

    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            "SELECT id_usuario FROM usuario WHERE id_usuario=%s AND senha_hash=%s",
            (id_usuario, hash_senha(senha_atual)),
        )
        if not cur.fetchone():
            return False, "Senha atual incorreta."

        cur.execute(
            "UPDATE usuario SET senha_hash=%s WHERE id_usuario=%s",
            (hash_senha(nova_senha), id_usuario),
        )
        conn.commit()
        return True, None
    finally:
        conn.close()
