# =========================================================
# services/jogo_service.py
# Lógica do jogo: carregar perguntas, registrar respostas,
# atualizar ranking.  Baseado em Jogo.py e Perguntas.py
# do Arthur — sem nenhum print/input, pronto para o front.
# =========================================================
import random
from dataclasses import dataclass, field
from typing import Optional
from services.db import conectar


# ---------------------------------------------------------
# Modelos de dados
# ---------------------------------------------------------

@dataclass
class Alternativa:
    id_alternativa: int
    texto: str
    imagem_url: Optional[str]
    correta: bool


@dataclass
class Dica:
    id_dica: int
    tipo: str          # 'eliminacao' | 'texto'
    conteudo: str
    penalizacao_pontos: int


@dataclass
class Pergunta:
    id_pergunta: int
    enunciado: str
    id_nivel: int
    imagem_url: Optional[str]
    alternativas: list[Alternativa] = field(default_factory=list)
    dicas: list[Dica] = field(default_factory=list)

    def alternativa_correta(self) -> Optional[Alternativa]:
        for a in self.alternativas:
            if a.correta:
                return a
        return None

    def alternativa_por_indice(self, idx: int) -> Optional[Alternativa]:
        """idx 0-3 correspondendo a A-D."""
        if 0 <= idx < len(self.alternativas):
            return self.alternativas[idx]
        return None

    def dica_eliminacao(self) -> Optional[Dica]:
        for d in self.dicas:
            if d.tipo == "eliminacao":
                return d
        return None

    def dica_texto(self) -> Optional[Dica]:
        for d in self.dicas:
            if d.tipo == "texto":
                return d
        return None


# ---------------------------------------------------------
# Mapa de dificuldade → id_nivel
# ---------------------------------------------------------
NIVEL = {"facil": 1, "medio": 2, "dificil": 3}


# ---------------------------------------------------------
# Carregamento de perguntas
# ---------------------------------------------------------

def carregar_perguntas(dificuldade: str) -> list[Pergunta]:
    """
    dificuldade: 'facil' | 'medio' | 'dificil' | 'aleatorio' | 'milhao'
    Retorna lista de Pergunta já com alternativas e dicas populadas.
    """
    conn = conectar()
    if not conn:
        return []

    try:
        cur = conn.cursor(dictionary=True, buffered=True)

        if dificuldade in NIVEL:
            cur.execute(
                "SELECT * FROM pergunta WHERE id_nivel=%s AND ativa=1",
                (NIVEL[dificuldade],),
            )
        elif dificuldade == "aleatorio":
            cur.execute("SELECT * FROM pergunta WHERE ativa=1")
        elif dificuldade == "milhao":
            cur.execute(
                "SELECT * FROM pergunta WHERE ativa=1 ORDER BY id_nivel ASC"
            )
        else:
            return []

        rows = cur.fetchall()

        if dificuldade == "milhao":
            rows = rows[:30]

        if dificuldade != "milhao":
            random.shuffle(rows)

        perguntas = []
        for row in rows:
            cur.execute(
                "SELECT * FROM alternativa WHERE id_pergunta=%s",
                (row["id_pergunta"],),
            )
            alts = [
                Alternativa(
                    id_alternativa=a["id_alternativa"],
                    texto=a["texto"] or "",
                    imagem_url=a.get("imagem_url"),
                    correta=bool(a["correta"]),
                )
                for a in cur.fetchall()
            ]

            cur.execute(
                "SELECT * FROM dica WHERE id_pergunta=%s",
                (row["id_pergunta"],),
            )
            dicas = [
                Dica(
                    id_dica=d["id_dica"],
                    tipo=d["tipo"],
                    conteudo=d["conteudo"],
                    penalizacao_pontos=d["penalizacao_pontos"],
                )
                for d in cur.fetchall()
            ]

            perguntas.append(
                Pergunta(
                    id_pergunta=row["id_pergunta"],
                    enunciado=row["enunciado"],
                    id_nivel=row["id_nivel"],
                    imagem_url=row.get("imagem_url"),
                    alternativas=alts,
                    dicas=dicas,
                )
            )

        return perguntas
    finally:
        conn.close()


# ---------------------------------------------------------
# Sessão de jogo
# ---------------------------------------------------------

def criar_sessao(id_usuario: int, id_nivel: int) -> Optional[int]:
    """Insere uma nova sessão e retorna o id_sessao."""
    conn = conectar()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessao_jogo (id_usuario, id_nivel) VALUES (%s, %s)",
            (id_usuario, id_nivel),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def registrar_resposta(
    id_sessao: int,
    pergunta: Pergunta,
    alternativa: Alternativa,
    correta: bool,
    tempo_seg: int,
):
    conn = conectar()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO resposta
               (id_sessao, id_pergunta, id_alternativa_escolhida, correta, tempo_resposta_seg)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_sessao, pergunta.id_pergunta, alternativa.id_alternativa, correta, tempo_seg),
        )
        conn.commit()
    finally:
        conn.close()


def registrar_uso_dica(id_sessao: int, pergunta: Pergunta, dica: Dica):
    conn = conectar()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO uso_dica (id_sessao, id_pergunta, id_dica) VALUES (%s, %s, %s)",
            (id_sessao, pergunta.id_pergunta, dica.id_dica),
        )
        conn.commit()
    finally:
        conn.close()


def finalizar_sessao(id_sessao: int, pontuacao: int):
    conn = conectar()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE sessao_jogo SET pontuacao=%s, concluida=1, finalizado_em=NOW() WHERE id_sessao=%s",
            (pontuacao, id_sessao),
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------
# Ranking
# ---------------------------------------------------------

def atualizar_ranking(id_usuario: int, id_nivel: int, pontuacao: int):
    conn = conectar()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            "SELECT * FROM ranking WHERE id_usuario=%s AND id_nivel=%s",
            (id_usuario, id_nivel),
        )
        existente = cur.fetchone()
        if existente:
            nova = max(existente["melhor_pontuacao"], pontuacao)
            cur.execute(
                """UPDATE ranking SET melhor_pontuacao=%s,
                   total_tentativas=total_tentativas+1
                   WHERE id_usuario=%s AND id_nivel=%s""",
                (nova, id_usuario, id_nivel),
            )
        else:
            cur.execute(
                "INSERT INTO ranking (id_usuario, id_nivel, melhor_pontuacao, total_tentativas) VALUES (%s,%s,%s,1)",
                (id_usuario, id_nivel, pontuacao),
            )
        conn.commit()
    finally:
        conn.close()


def buscar_ranking(id_nivel: int, limite: int = 10) -> list[dict]:
    """Retorna lista de {'nome', 'turma', 'melhor_pontuacao'}."""
    conn = conectar()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            """SELECT u.nome, u.turma, r.melhor_pontuacao
               FROM ranking r
               JOIN usuario u ON u.id_usuario = r.id_usuario
               WHERE r.id_nivel=%s
               ORDER BY r.melhor_pontuacao DESC
               LIMIT %s""",
            (id_nivel, limite),
        )
        return cur.fetchall()
    finally:
        conn.close()


def buscar_ranking_geral(limite: int = 10) -> list[dict]:
    """Ranking somando melhor pontuação de todos os níveis."""
    conn = conectar()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            """SELECT u.nome, u.turma, SUM(r.melhor_pontuacao) AS pontuacao_total
               FROM ranking r
               JOIN usuario u ON u.id_usuario = r.id_usuario
               GROUP BY r.id_usuario
               ORDER BY pontuacao_total DESC
               LIMIT %s""",
            (limite,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ---------------------------------------------------------
# Desempenho (relatório do professor)
# ---------------------------------------------------------

def buscar_desempenho_geral() -> list[dict]:
    conn = conectar()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT * FROM vw_desempenho ORDER BY taxa_acerto_pct DESC")
        return cur.fetchall()
    finally:
        conn.close()


def buscar_desempenho_aluno(id_usuario: int) -> list[dict]:
    conn = conectar()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True, buffered=True)
        cur.execute(
            "SELECT * FROM vw_desempenho WHERE id_usuario=%s", (id_usuario,)
        )
        return cur.fetchall()
    finally:
        conn.close()
