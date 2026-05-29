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
    Simula login de aluno.

    Quem chama isso?
    -----------------
    AuthController._login_aluno()

    O controller usa o retorno para:
    - salvar usuário logado no sistema
    - navegar para a próxima tela (pg_tipo_jogo)
    - mostrar erro caso login falhe

    IMPORTANTE:
    -----------
    Este STUB aceita QUALQUER e-mail e senha válidos,
    sem autenticação real.
    """

    # Simulação de resposta do banco de dados
    return {
        "id_usuario": 1,
        "nome": "Aluno Teste",
        "email": email,
        "tipo": "aluno",
        "turma": "3INFO1",
        "senha_hash": "hash_ficticio",
    }, None


def cadastrar_aluno(nome: str, email: str, turma: str):
    """
    Simula cadastro de aluno.

    Observação:
    ----------
    Ainda não há validação de duplicidade ou banco real.

    Senha padrão (no sistema real):
    - senha1234+
    """

    return {
        "id_usuario": 99,
        "nome": nome,
        "email": email,
        "tipo": "aluno",
        "turma": turma,
        "senha_hash": "hash_ficticio",
    }, None


# =========================================================
# FUNÇÕES DO PROFESSOR
# =========================================================

def login_prof(email: str, senha: str):
    """
    Simula login de professor.

    Fluxo no sistema:
    - AuthController._login_prof()
    - salva usuário logado
    - vai para pg_areaprof
    """

    return {
        "id_usuario": 2,
        "nome": "Professor Teste",
        "email": email,
        "tipo": "professor",
        "turma": None,
    }, None


def cadastrar_prof(nome: str, email: str):
    """
    Simula cadastro de professor.

    Importante:
    ----------
    - A senha é gerada automaticamente como 'senha1234+'
    - O nome já vem formatado pelo controller
      (ex: "maria.souza" → "Maria Souza")
    """

    return {
        "id_usuario": 98,
        "nome": nome,
        "email": email,
        "tipo": "professor",
        "turma": None,
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