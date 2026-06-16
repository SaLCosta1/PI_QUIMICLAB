import base64

from Back.Conectar_Banco import conectar_banco


def _imagem_para_blob(dados: dict) -> tuple[bytes | None, str | None]:
    """Converte imagem_base64 (UI) para bytes + MIME do schema."""
    b64 = dados.get("imagem_base64")
    if not b64:
        return None, None
    mime = dados.get("imagem_mime") or "image/png"
    try:
        return base64.b64decode(b64), mime
    except Exception:
        return None, None


def _blob_para_base64(imagem, mime: str | None = None) -> str | None:
    """Converte BLOB do banco para base64 (UI)."""
    if not imagem:
        return None
    if isinstance(imagem, (bytes, bytearray)):
        return base64.b64encode(imagem).decode("utf-8")
    return None


def _nivel_para_id(nivel_str) -> int:
    if nivel_str is None or nivel_str == "":
        return 1
    s = str(nivel_str).strip().lower()
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
    """Cria pergunta + alternativas + dica. Retorna (True, None) ou (False, erro).

    dados: pergunta, nivel, dica, altA..altD, alt_correta (A-D), imagem_base64, imagem_mime.
    """
    enunciado = dados.get("pergunta", "").strip()
    if not enunciado:
        return False, "Enunciado vazio."

    id_nivel = _nivel_para_id(dados.get("nivel", ""))
    imagem_bytes, imagem_mime = _imagem_para_blob(dados)
    
    # Determinar qual alternativa é correta
    alt_correta = dados.get("alt_correta", "A").upper()
    if alt_correta not in ("A", "B", "C", "D"):
        alt_correta = "A"
    
    # Mapa: letra -> índice (0=A, 1=B, 2=C, 3=D)
    idx_correta = ord(alt_correta) - ord("A")

    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pergunta (id_nivel, id_criador, enunciado, imagem, imagem_mime, ativa) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_nivel, criador_id, enunciado, imagem_bytes, imagem_mime, 1),
        )
        conn.commit()
        pid = cursor.lastrowid

        # Alternativas: marca a escolhida como correta
        alternativas = [
            (dados.get("altA", "").strip(), None, 1 if idx_correta == 0 else 0),
            (dados.get("altB", "").strip(), None, 1 if idx_correta == 1 else 0),
            (dados.get("altC", "").strip(), None, 1 if idx_correta == 2 else 0),
            (dados.get("altD", "").strip(), None, 1 if idx_correta == 3 else 0),
        ]

        for texto, imagem, correta in alternativas:
            if not texto:
                continue
            cursor.execute(
                "INSERT INTO alternativa (id_pergunta, texto, imagem, imagem_mime, correta) VALUES (%s, %s, %s, %s, %s)",
                (pid, texto, imagem, None, correta),
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


def listar_perguntas(id_nivel: int | None = None) -> list[dict]:
    """Lista as perguntas ativas (opcionalmente filtradas por nível)."""
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    try:
        if id_nivel:
            cursor.execute(
                """
                SELECT p.id_pergunta, p.enunciado, p.id_nivel, n.nome as nome_nivel
                FROM pergunta p
                JOIN nivel n ON p.id_nivel = n.id_nivel
                WHERE p.id_nivel = %s AND p.ativa = 1
                ORDER BY p.id_pergunta
                """,
                (id_nivel,)
            )
        else:
            cursor.execute(
                """
                SELECT p.id_pergunta, p.enunciado, p.id_nivel, n.nome as nome_nivel
                FROM pergunta p
                JOIN nivel n ON p.id_nivel = n.id_nivel
                WHERE p.ativa = 1
                ORDER BY p.id_nivel, p.id_pergunta
                """
            )
        
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obter_pergunta(id_pergunta: int) -> dict | None:
    """Obtém uma pergunta completa (enunciado, imagem, alternativas e dicas) ou None."""
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT p.id_pergunta, p.enunciado, p.id_nivel, p.imagem, p.imagem_mime,
                   n.nome as nome_nivel
            FROM pergunta p
            JOIN nivel n ON p.id_nivel = n.id_nivel
            WHERE p.id_pergunta = %s AND p.ativa = 1
            """,
            (id_pergunta,)
        )
        
        pergunta = cursor.fetchone()
        if not pergunta:
            return None

        pergunta["imagem_base64"] = _blob_para_base64(
            pergunta.pop("imagem", None),
            pergunta.get("imagem_mime"),
        )
        
        # Buscar alternativas
        cursor.execute(
            "SELECT id_alternativa, texto, correta FROM alternativa WHERE id_pergunta = %s",
            (id_pergunta,)
        )
        pergunta['alternativas'] = cursor.fetchall()
        
        # Buscar dicas
        cursor.execute(
            "SELECT id_dica, tipo, conteudo FROM dica WHERE id_pergunta = %s",
            (id_pergunta,)
        )
        pergunta['dicas'] = cursor.fetchall()
        
        return pergunta
    finally:
        cursor.close()
        conn.close()


def atualizar_pergunta(id_pergunta: int, dados: dict) -> tuple[bool, str | None]:
    """Atualiza pergunta + alternativas + dica. Mesmo formato de `dados` de criar_pergunta.

    Retorna (True, None) ou (False, erro).
    """
    enunciado = dados.get("pergunta", "").strip()
    if not enunciado:
        return False, "Enunciado vazio."

    id_nivel = _nivel_para_id(dados.get("nivel", ""))
    imagem_bytes, imagem_mime = _imagem_para_blob(dados)

    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        if imagem_bytes is not None:
            cursor.execute(
                "UPDATE pergunta SET id_nivel = %s, enunciado = %s, imagem = %s, imagem_mime = %s WHERE id_pergunta = %s",
                (id_nivel, enunciado, imagem_bytes, imagem_mime, id_pergunta),
            )
        else:
            cursor.execute(
                "UPDATE pergunta SET id_nivel = %s, enunciado = %s WHERE id_pergunta = %s",
                (id_nivel, enunciado, id_pergunta),
            )

        # Determinar qual alternativa é correta
        alt_correta = dados.get("alt_correta", "A").upper()
        if alt_correta not in ("A", "B", "C", "D"):
            alt_correta = "A"
        
        # Mapa: letra -> índice (0=A, 1=B, 2=C, 3=D)
        idx_correta = ord(alt_correta) - ord("A")

        # Atualizar apenas o campo 'correta' das alternativas existentes
        # em vez de deletar e recriar (para evitar violação de FK)
        alternativas_novas = [
            (dados.get("altA", "").strip(), None, 1 if idx_correta == 0 else 0),
            (dados.get("altB", "").strip(), None, 1 if idx_correta == 1 else 0),
            (dados.get("altC", "").strip(), None, 1 if idx_correta == 2 else 0),
            (dados.get("altD", "").strip(), None, 1 if idx_correta == 3 else 0),
        ]

        # Buscar alternativas existentes
        cursor.execute(
            "SELECT id_alternativa FROM alternativa WHERE id_pergunta = %s ORDER BY id_alternativa",
            (id_pergunta,)
        )
        ids_existentes = [row[0] for row in cursor.fetchall()]

        # Atualizar ou inserir alternativas
        for i, (texto, imagem, correta) in enumerate(alternativas_novas):
            if not texto:
                # Se não há texto, deletar essa alternativa se existir
                if i < len(ids_existentes):
                    cursor.execute(
                        "DELETE FROM alternativa WHERE id_alternativa = %s",
                        (ids_existentes[i],)
                    )
                continue
            
            if i < len(ids_existentes):
                # Alternativa existe: atualizar
                cursor.execute(
                    "UPDATE alternativa SET texto = %s, correta = %s WHERE id_alternativa = %s",
                    (texto, correta, ids_existentes[i]),
                )
            else:
                # Alternativa não existe: criar
                cursor.execute(
                    "INSERT INTO alternativa (id_pergunta, texto, imagem, imagem_mime, correta) VALUES (%s, %s, %s, %s, %s)",
                    (id_pergunta, texto, imagem, None, correta),
                )

        # Atualizar dica SEM deletar a linha: se um aluno já usou a dica, existe
        # um registro em uso_dica apontando para id_dica (FK fk_uso_dica_ref), e o
        # DELETE quebraria com erro 1451. Então atualizamos a dica existente no lugar.
        cursor.execute(
            "SELECT id_dica FROM dica WHERE id_pergunta = %s ORDER BY id_dica",
            (id_pergunta,),
        )
        ids_dica = [row[0] for row in cursor.fetchall()]

        dica = dados.get("dica", "").strip()
        if dica:
            if ids_dica:
                # Reaproveita a primeira dica (mantém id_dica e a FK de uso_dica).
                cursor.execute(
                    "UPDATE dica SET tipo = %s, conteudo = %s, penalizacao_pontos = %s WHERE id_dica = %s",
                    ('texto', dica, 0, ids_dica[0]),
                )
                extras = ids_dica[1:]
            else:
                cursor.execute(
                    "INSERT INTO dica (id_pergunta, tipo, conteudo, penalizacao_pontos) VALUES (%s, %s, %s, %s)",
                    (id_pergunta, 'texto', dica, 0),
                )
                extras = []
        else:
            extras = ids_dica

        # Remove dicas sobrando apenas se nenhum aluno as tiver usado (FK segura).
        for id_dica in extras:
            cursor.execute("SELECT 1 FROM uso_dica WHERE id_dica = %s LIMIT 1", (id_dica,))
            if cursor.fetchone() is None:
                cursor.execute("DELETE FROM dica WHERE id_dica = %s", (id_dica,))

        conn.commit()
        return True, None
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def deletar_pergunta(id_pergunta: int) -> tuple[bool, str | None]:
    """Exclusão lógica: marca a pergunta como inativa. Retorna (True, None) ou (False, erro)."""
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE pergunta SET ativa = 0 WHERE id_pergunta = %s",
            (id_pergunta,)
        )
        conn.commit()
        return True, None
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()
