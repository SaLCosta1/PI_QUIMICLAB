# Ponte entre os controllers (frontend) e o backend de autenticação (Back/).
# Padrão de retorno de todas as funções: sucesso -> (dados, None); erro -> (None, "mensagem").

from Back.aluno import Usuario as BackAluno
from Back.professor import Professor as BackProfessor


def _formatar_nome(email: str) -> str:
    partes = email.split("@")[0].split(".")
    return " ".join(part.capitalize() for part in partes if part)


def _email_valido_aluno(email: str) -> bool:
    # Aluno: nome.sobrenome@aluno.cps.sp.gov.br
    partes = email.split("@")
    if len(partes) != 2:
        return False
    return partes[1].split(".") == ["aluno", "cps", "sp", "gov", "br"]


def _email_valido_prof(email: str) -> bool:
    # Professor: nome.sobrenome@cps.sp.gov.br
    partes = email.split("@")
    if len(partes) != 2:
        return False
    return partes[1].split(".") == ["cps", "sp", "gov", "br"]


def login_aluno(email: str, senha: str):
    """Faz login de aluno pelo backend."""
    usuario, status = BackAluno.login(email, senha)
    if not usuario:
        return None, status or "E-mail ou senha incorretos."

    return {
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "turma": usuario.turma,
    }, None


def cadastrar_aluno(nome: str, email: str, turma: str, senha: str | None = None):
    """Cadastra um aluno pelo backend."""
    try:
        usuario, status = BackAluno.cadastrar(nome, email, turma, senha)
    except Exception as exc:
        return None, f"Erro ao cadastrar aluno: {exc}"

    if not usuario:
        return None, status or "Não foi possível cadastrar o aluno."

    return {
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "turma": usuario.turma,
    }, None


def login_prof(email: str, senha: str):
    """Faz login de professor pelo backend."""
    professor, status = BackProfessor.login(email, senha)
    if not professor:
        return None, status or "E-mail ou senha incorretos."

    return {
        "id_usuario": professor.id_usuario,
        "nome": professor.nome,
        "email": professor.email,
        "tipo": "professor",
    }, None


def cadastrar_prof(nome: str, email: str):
    """Cadastra um professor pelo backend (nome derivado do e-mail)."""
    nome_formatado = _formatar_nome(email)
    professor, status = BackProfessor.cadastrar(nome_formatado, email)
    if not professor:
        return None, status or "Não foi possível cadastrar o professor."

    return {
        "id_usuario": professor.id_usuario,
        "nome": professor.nome,
        "email": professor.email,
        "tipo": "professor",
    }, None


def trocar_senha_aluno(email: str, nova_senha: str):
    """Persiste a nova senha do aluno. Retorna (True, None) ou (False, erro)."""
    return BackAluno.atualizar_senha(email, nova_senha)


def trocar_senha_prof(email: str, nova_senha: str):
    """Persiste a nova senha do professor. Retorna (True, None) ou (False, erro)."""
    return BackProfessor.atualizar_senha(email, nova_senha)
