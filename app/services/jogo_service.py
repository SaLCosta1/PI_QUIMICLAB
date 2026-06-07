import math

from Back import Jogo as backend_jogo

# Porcentagem de acerto exigida no nível para desbloquear o próximo.
PERCENTUAL_DESBLOQUEIO = 60

NIVEL = {"facil": 1, "medio": 2, "dificil": 3}

NIVEL_NOME = {1: "Fácil", 2: "Médio", 3: "Difícil"}


def carregar_perguntas(dificuldade: str) -> list:
    """Busca perguntas do banco por dificuldade (facil/medio/dificil/aleatorio/milhao/desafio)."""
    try:
        # Aceita tanto nomes quanto números de nível
        nivel_map = {"1": "facil", "2": "medio", "3": "dificil"}
        if dificuldade in nivel_map:
            dificuldade = nivel_map[dificuldade]
        
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
    """Ranking de um nível (pontuação só do modo Desafio)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT u.id_usuario, u.nome, u.turma, r.melhor_pontuacao
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


def ja_acertou_pergunta_nesta_sessao(id_sessao: int, id_pergunta: int) -> bool:
    """Diz se o aluno já acertou essa pergunta nesta mesma sessão (evita pontuar duas vezes)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(*) as total
                FROM resposta r
                WHERE r.id_sessao = %s
                AND r.id_pergunta = %s
                AND r.correta = 1
                """,
                (id_sessao, id_pergunta),
            )
            resultado = cursor.fetchone()
            return resultado.get('total', 0) > 0 if resultado else False
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao verificar pergunta nesta sessão: {e}")
        return False


def contar_acertos_nivel_aluno(id_usuario: int, id_nivel: int) -> int:
    """Conta perguntas distintas que o aluno acertou num nível (qualquer modo)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(DISTINCT r.id_pergunta) as total
                FROM resposta r
                JOIN sessao_jogo sj ON r.id_sessao = sj.id_sessao
                JOIN pergunta p ON r.id_pergunta = p.id_pergunta
                WHERE sj.id_usuario = %s
                AND p.id_nivel = %s
                AND r.correta = 1
                """,
                (id_usuario, id_nivel),
            )
            resultado = cursor.fetchone()
            return resultado.get('total', 0) if resultado else 0
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao contar acertos: {e}")
        return 0


def buscar_ranking_geral(limite: int = 10) -> list[dict]:
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT u.id_usuario, u.nome, u.turma, SUM(r.melhor_pontuacao) AS pontuacao_total
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


def buscar_ranking_alunos(turma: str | None = None, limite: int = 200) -> list[dict]:
    """Ranking de alunos por pontuação de Desafio (inclui quem nunca jogou com 0; filtra por turma)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            base = """
                SELECT u.id_usuario, u.nome, u.turma,
                       COALESCE(SUM(r.melhor_pontuacao), 0) AS pontuacao
                FROM usuario u
                LEFT JOIN ranking r ON r.id_usuario = u.id_usuario
                WHERE u.tipo = 'aluno'{filtro}
                GROUP BY u.id_usuario, u.nome, u.turma
                ORDER BY pontuacao DESC, u.nome
                LIMIT %s
            """
            if turma and turma != "Todas":
                cursor.execute(base.format(filtro=" AND u.turma = %s"), (turma, limite))
            else:
                cursor.execute(base.format(filtro=""), (limite,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao buscar ranking de alunos: {e}")
        return []


def buscar_ranking_turmas() -> list[dict]:
    """Ranking de turmas pela pontuação média (Desafio) dos seus alunos."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                """
                SELECT pts.turma,
                       ROUND(AVG(pts.pontuacao), 1) AS media,
                       COUNT(*) AS n_alunos
                FROM (
                    SELECT u.id_usuario, u.turma,
                           COALESCE(SUM(r.melhor_pontuacao), 0) AS pontuacao
                    FROM usuario u
                    LEFT JOIN ranking r ON r.id_usuario = u.id_usuario
                    WHERE u.tipo = 'aluno' AND u.turma IS NOT NULL AND u.turma <> ''
                    GROUP BY u.id_usuario, u.turma
                ) pts
                GROUP BY pts.turma
                ORDER BY media DESC, pts.turma
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao buscar ranking de turmas: {e}")
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
    """Busca as respostas do aluno só no modo Desafio (usado nos relatórios do professor)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            query = """
            SELECT r.*, sj.modo
            FROM resposta r
            JOIN sessao_jogo sj ON r.id_sessao = sj.id_sessao
            WHERE sj.id_usuario = %s
            AND sj.modo = 'desafio'
            ORDER BY sj.id_sessao DESC
            """
            cursor.execute(query, (id_usuario,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao buscar desempenho: {e}")
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


def buscar_turmas() -> list[str]:
    """Lista todas as turmas cadastradas (sem repetição, ordenadas)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute("SELECT DISTINCT turma FROM usuario WHERE turma IS NOT NULL ORDER BY turma")
            resultados = cursor.fetchall()
            turmas = [r.get('turma') for r in resultados if r.get('turma')]
            return sorted(list(set(turmas)))  # Remove duplicatas e ordena
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao buscar turmas: {e}")
        return []


def buscar_alunos_por_turma(turma: str = None) -> list[dict]:
    """Lista alunos de uma turma (ou todos, se turma for None)."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            if turma and turma != "Todas":
                cursor.execute(
                    "SELECT id_usuario, nome, email, turma FROM usuario WHERE tipo = 'aluno' AND turma = %s ORDER BY nome",
                    (turma,)
                )
            else:
                cursor.execute(
                    "SELECT id_usuario, nome, email, turma FROM usuario WHERE tipo = 'aluno' ORDER BY nome"
                )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao buscar alunos por turma: {e}")
        return []


def contar_perguntas_nivel(id_nivel: int) -> int:
    """Conta quantas perguntas ativas existem num nível."""
    try:
        conexao, cursor = backend_jogo._get_conn_cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM pergunta WHERE id_nivel = %s AND ativa = 1",
                (id_nivel,),
            )
            resultado = cursor.fetchone()
            return resultado.get('total', 0) if resultado else 0
        finally:
            cursor.close()
            conexao.close()
    except Exception as e:
        print(f"[jogo_service] Erro ao contar perguntas do nível: {e}")
        return 0


def verificar_desbloqueio_nivel(id_usuario: int, id_nivel_atual: int) -> dict:
    """Verifica se o aluno desbloqueou o próximo nível (precisa acertar 60% das perguntas do nível)."""
    try:
        total_perguntas = contar_perguntas_nivel(id_nivel_atual)
        acertos_atuais = contar_acertos_nivel_aluno(id_usuario, id_nivel_atual)
        # Quantos acertos representam os 60% (arredondando para cima).
        acertos_necessarios = math.ceil(total_perguntas * PERCENTUAL_DESBLOQUEIO / 100)

        proximo_nivel = id_nivel_atual + 1
        if proximo_nivel > 3:
            proximo_nivel = None

        # Nível sem perguntas cadastradas não tem o que bloquear.
        if total_perguntas == 0:
            desbloqueado = True
        else:
            desbloqueado = acertos_atuais >= acertos_necessarios

        if desbloqueado and proximo_nivel:
            mensagem = f"Parabéns! Você desbloqueou o nível {proximo_nivel}!"
        elif proximo_nivel:
            faltam = max(acertos_necessarios - acertos_atuais, 0)
            mensagem = (
                f"Você acertou {acertos_atuais} de {total_perguntas} perguntas. "
                f"São necessários {PERCENTUAL_DESBLOQUEIO}% "
                f"({acertos_necessarios} acertos) para desbloquear o próximo nível "
                f"— faltam {faltam}."
            )
        else:
            mensagem = "Você completou todos os níveis!"

        return {
            'desbloqueado': desbloqueado,
            'percentual_exigido': PERCENTUAL_DESBLOQUEIO,
            'total_perguntas': total_perguntas,
            'acertos_necessarios': acertos_necessarios,
            'acertos_atuais': acertos_atuais,
            'proximo_nivel': proximo_nivel,
            'mensagem': mensagem
        }
    except Exception as e:
        print(f"[jogo_service] Erro ao verificar desbloqueio: {e}")
        return {
            'desbloqueado': False,
            'percentual_exigido': PERCENTUAL_DESBLOQUEIO,
            'total_perguntas': 0,
            'acertos_necessarios': 0,
            'acertos_atuais': 0,
            'proximo_nivel': None,
            'mensagem': 'Erro ao verificar desbloqueio.'
        }
