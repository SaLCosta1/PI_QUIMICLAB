from Back.Conectar_Banco import conectar_banco


def _nivel_para_id(nivel_str: str) -> int:
    if not nivel_str:
        return 1
    s = nivel_str.strip().lower()
    if s in ("1", "facil", "fácil"):
        return 1
    if s in ("2", "medio", "médio"):
        return 2
    if s in ("3", "dificil", "difícil"):
        return 3
    # fallback: try to parse integer
    try:
        v = int(s)
        if v in (1, 2, 3):
            return v
    except Exception:
        pass
    return 1


def criar_pergunta(dados: dict, criador_id: int | None = None) -> tuple[bool, str | None]:
    """
    Cria uma pergunta no banco com alternativas e uma dica (se houver).

    dados esperado: {
        'pergunta': str,
        'nivel': str,
        'dica': str,
        'altA': str,
        'altB': str,
        'altC': str,
        'altD': str,
    }

    Retorna (True, None) em sucesso ou (False, mensagem_erro).
    """

    enunciado = dados.get("pergunta", "").strip()
    if not enunciado:
        return False, "Enunciado vazio."

    id_nivel = _nivel_para_id(dados.get("nivel", ""))

    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pergunta (id_nivel, id_criador, enunciado, imagem_url, ativa) VALUES (%s, %s, %s, %s, %s)",
            (id_nivel, criador_id, enunciado, None, 1),
        )
        conn.commit()
        pid = cursor.lastrowid

        # Alternativas: marca a A como correta por padrão
        alternativas = [
            (dados.get("altA", "").strip(), None, 1),
            (dados.get("altB", "").strip(), None, 0),
            (dados.get("altC", "").strip(), None, 0),
            (dados.get("altD", "").strip(), None, 0),
        ]

        for texto, imagem, correta in alternativas:
            if not texto:
                continue
            cursor.execute(
                "INSERT INTO alternativa (id_pergunta, texto, imagem_url, correta) VALUES (%s, %s, %s, %s)",
                (pid, texto, imagem, correta),
            )

        # Dica (texto)
        dica = dados.get("dica", "").strip()
        if dica:
            cursor.execute(
                "INSERT INTO dica (id_pergunta, tipo, conteudo, penalizacao_pontos) VALUES (%s, %s, %s, %s)",
                (pid, 'texto', dica, 0),
            )

        conn.commit()
        return True, None
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()
