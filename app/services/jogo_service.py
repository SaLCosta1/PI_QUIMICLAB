# =========================================================
# Serviço de jogo — integração com Back/Jogo.py e MySQL
# =========================================================

from Back import Jogo as backend_jogo

NIVEL = {"facil": 1, "medio": 2, "dificil": 3}

NIVEL_NOME = {1: "Fácil", 2: "Médio", 3: "Difícil"}


def carregar_perguntas(dificuldade: str) -> list:
    """
    Busca perguntas do banco por dificuldade.

    dificuldade: facil | medio | dificil | aleatorio | milhao
    Retorna lista de Back.Perguntas.Pergunta ou [] em caso de erro.
    """
    try:
        if dificuldade in NIVEL:
            return backend_jogo.carregar_perguntas(str(NIVEL[dificuldade]))
        if dificuldade == "aleatorio":
            return backend_jogo.carregar_perguntas("4")
        if dificuldade == "milhao":
            return backend_jogo.carregar_perguntas("5")
        if dificuldade == "desafio":
            return backend_jogo.carregar_perguntas("4")
    except Exception as exc:
        print(f"[jogo_service] Erro ao carregar perguntas ({dificuldade}): {exc}")
    return []


def criar_sessao(id_usuario: int, id_nivel: int, modo: str = "tradicional") -> int | None:
    try:
        return backend_jogo.criar_sessao(id_usuario, id_nivel, modo)
    except Exception as exc:
        print(f"[jogo_service] Erro ao criar sessão: {exc}")
        return None


def registrar_resposta(id_sessao, pergunta, alternativa, correta, tempo_seg):
    try:
        alt = alternativa if isinstance(alternativa, dict) else {
            "id_alternativa": alternativa.id_alternativa,
        }
        backend_jogo.registrar_resposta(id_sessao, pergunta, alt, correta, tempo_seg)
    except Exception as exc:
        print(f"[jogo_service] Erro ao registrar resposta: {exc}")


def registrar_uso_dica(id_sessao, pergunta, dica):
    if not id_sessao or dica is None:
        return
    id_dica = dica.get("id_dica") if isinstance(dica, dict) else getattr(dica, "id_dica", None)
    if id_dica is None:
        return
    id_pergunta = pergunta.id_pergunta if hasattr(pergunta, "id_pergunta") else pergunta["id_pergunta"]
    try:
        backend_jogo.registrar_uso_dica(id_sessao, id_pergunta, id_dica)
    except Exception as exc:
        print(f"[jogo_service] Erro ao registrar dica: {exc}")


def finalizar_sessao(id_sessao: int, pontuacao: int):
    if not id_sessao:
        return
    try:
        backend_jogo.finalizar_sessao(id_sessao, pontuacao)
    except Exception as exc:
        print(f"[jogo_service] Erro ao finalizar sessão: {exc}")


def atualizar_ranking(id_usuario: int, id_nivel: int, pontuacao: int):
    try:
        backend_jogo.atualizar_ranking(id_usuario, id_nivel, pontuacao)
    except Exception as exc:
        print(f"[jogo_service] Erro ao atualizar ranking: {exc}")


def buscar_ranking(id_nivel: int, limite: int = 10) -> list[dict]:
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT u.nome, u.turma, r.melhor_pontuacao
                FROM ranking r
                JOIN usuario u ON u.id_usuario = r.id_usuario
                WHERE r.id_nivel = %s
                ORDER BY r.melhor_pontuacao DESC
                LIMIT %s
                """,
                (id_nivel, limite),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception:
        return []


def buscar_ranking_geral(limite: int = 10) -> list[dict]:
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT u.nome, u.turma, SUM(r.melhor_pontuacao) AS pontuacao_total
                FROM ranking r
                JOIN usuario u ON u.id_usuario = r.id_usuario
                GROUP BY u.id_usuario, u.nome, u.turma
                ORDER BY pontuacao_total DESC
                LIMIT %s
                """,
                (limite,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception:
        return []


def buscar_desempenho_geral() -> list[dict]:
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute("SELECT * FROM vw_questoes_mais_erradas LIMIT 50")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception:
        return []


def buscar_desempenho_aluno(id_usuario: int) -> list[dict]:
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                "SELECT * FROM vw_desempenho WHERE id_usuario = %s",
                (id_usuario,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception:
        return []


def ordenar_ranking_alunos(ranking_alunos: list[dict]) -> list[dict]:
    return sorted(ranking_alunos, key=lambda x: x.get("pontos", x.get("melhor_pontuacao", 0)), reverse=True)


def ordenar_ranking_turmas(ranking_turmas: list[dict]) -> list[dict]:
    return sorted(ranking_turmas, key=lambda x: x.get("pontos", 0), reverse=True)


def calcular_media(acertos: int, total: int) -> float:
    if total == 0:
        return 0
    return round(acertos / total, 2)


def adicionar_pontos(aluno: dict, pontos: int):
    aluno["pontos"] = aluno.get("pontos", 0) + pontos


def filtrar_por_turma(ranking_alunos: list[dict], turma: str) -> list[dict]:
    return [a for a in ranking_alunos if a.get("turma") == turma]
