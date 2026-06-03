# =========================================================
# frontend/services/auth_service.py  — STUB (sem banco)
#
# O que é este arquivo?
# ---------------------
# Este arquivo é uma VERSÃO FALSA (stub) do serviço de autenticação.
# Ele existe para permitir que o FRONTEND funcione mesmo sem o banco
# de dados conectado.
#
# Ou seja:
# - Ele NÃO valida usuários de verdade
# - Ele NÃO acessa banco de dados
# - Ele apenas SIMULA respostas como se tudo estivesse funcionando
#
# Isso é muito comum em projetos grandes para permitir desenvolvimento
# paralelo entre frontend e backend.
#
# =========================================================

# ---------------------------------------------------------
# PADRÃO IMPORTANTE DO PROJETO
# ---------------------------------------------------------
# Todas as funções seguem o mesmo padrão de retorno:
#
#   Sucesso → (dados, None)
#   Erro    → (None, "mensagem de erro")
#
# Para funções booleanas:
#   Sucesso → (True, None)
#   Erro    → (False, "mensagem de erro")
#
# O frontend (controllers) depende EXATAMENTE desse padrão.
# ---------------------------------------------------------


# ---------------------------------------------------------
# VALIDAÇÃO DE E-MAIL (FUNÇÕES AUXILIARES INTERNAS)
# ---------------------------------------------------------
# Essas funções verificam se o e-mail pertence ao domínio correto
# da instituição.
#
# Importante:
# - Aqui elas são apenas simuladas/localizadas no frontend
# - Na versão real (com banco), elas já existirão no backend
#   e serão copiadas/integradas, não recriadas
# ---------------------------------------------------------

from Back.aluno import Usuario as BackAluno
from Back.professor import Professor as BackProfessor


def _formatar_nome(email: str) -> str:
    partes = email.split("@")[0].split(".")
    return " ".join(part.capitalize() for part in partes if part)


def _email_valido_aluno(email: str) -> bool:
    """
    Verifica se o e-mail é de aluno institucional.

    Formato esperado:
    nome.sobrenome@aluno.cps.gov.br
    """
    partes = email.split("@")

    # Se não tiver exatamente 1 "@", o e-mail é inválido
    if len(partes) != 2:
        return False

    # Divide o domínio e confere se bate com o padrão esperado
    return partes[1].split(".") == ["aluno", "cps", "gov", "br"]


def _email_valido_prof(email: str) -> bool:
    """
    Verifica se o e-mail é de professor institucional.

    Formato esperado:
    nome.sobrenome@cps.sp.gov.br
    """
    partes = email.split("@")

    if len(partes) != 2:
        return False

    return partes[1].split(".") == ["cps", "sp", "gov", "br"]


# =========================================================
# FUNÇÕES DO ALUNO
# =========================================================

def login_aluno(email: str, senha: str):
    """
    Faz login de aluno usando o backend existente.
    """

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
    """
    Faz cadastro de aluno usando o backend existente.
    """

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


# =========================================================
# FUNÇÕES DO PROFESSOR
# =========================================================

def login_prof(email: str, senha: str):
    """
    Faz login de professor usando o backend existente.

    Fluxo no sistema:
    - AuthController._login_prof()
    - salva usuário logado
    - vai para pg_areaprof
    """

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
    """
    Faz cadastro de professor usando o backend existente.
    """

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


# =========================================================
# TROCA DE SENHA
# =========================================================

def trocar_senha(id_usuario: int, senha_atual: str, nova_senha: str):
    """
    Simula troca de senha do usuário.

    Usado por:
    - aluno → volta para pg_tipo_jogo
    - professor → volta para pg_areaprof

    IMPORTANTE:
    ----------
    No sistema real, aqui ocorreria:
    - validação da senha atual no banco
    - hash da nova senha
    - atualização no banco de dados
    """

    # Validação mínima apenas para evitar campos vazios
    if not senha_atual or not nova_senha:
        return False, "Preencha todos os campos."

    # STUB: sempre aprova a troca
    return True, None