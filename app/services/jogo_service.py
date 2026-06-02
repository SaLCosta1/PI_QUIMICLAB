# =========================================================
# frontend/services/jogo_service.py  — STUB (sem banco)
#
# O que é este arquivo?
# ---------------------
# Este arquivo é uma versão FALSA (stub) do serviço de jogo.
# Ele permite que o frontend funcione SEM banco de dados.
#
# Ou seja:
# - Não busca perguntas reais
# - Não salva respostas no banco
# - Não atualiza ranking de verdade
# - Apenas SIMULA o comportamento do sistema completo
#
# Isso permite que o frontend seja desenvolvido antes do backend.
#
# =========================================================

import random
from dataclasses import dataclass, field
from typing import Optional

from Back import Jogo as backend_jogo


# ---------------------------------------------------------
# MODELOS DE DADOS (DATA CLASSES)
# ---------------------------------------------------------
# Essas classes representam os "objetos reais" do sistema.
# Elas são iguais às que existirão na versão com banco.
#
# Importante:
# - Controllers dependem exatamente desses campos
# - Na integração, o backend deve retornar os mesmos formatos
# ---------------------------------------------------------

@dataclass
class Alternativa:
    """
    Representa uma alternativa de resposta de uma pergunta.

    Exemplo:
    "H2O", "CO2", etc.
    """
    id_alternativa: int
    texto: str
    imagem_url: Optional[str]
    correta: bool  # True = resposta certa


@dataclass
class Dica:
    """
    Representa uma dica que pode ser usada durante o jogo.

    Tipos possíveis:
    - eliminacao → remove alternativas erradas
    - texto      → mostra uma dica explicativa
    """
    id_dica: int
    tipo: str
    conteudo: str
    penalizacao_pontos: int  # pontos perdidos ao usar a dica


@dataclass
class Pergunta:
    """
    Representa uma pergunta completa do jogo.

    Contém:
    - enunciado
    - alternativas
    - dicas
    """

    id_pergunta: int
    enunciado: str
    id_nivel: int
    imagem_url: Optional[str]
    alternativas: list[Alternativa] = field(default_factory=list)
    dicas: list[Dica] = field(default_factory=list)

    # -----------------------------------------------------
    # MÉTODOS AUXILIARES
    # -----------------------------------------------------
    # Esses métodos facilitam o uso da pergunta no frontend
    # sem precisar ficar filtrando listas manualmente.
    # -----------------------------------------------------

    def alternativa_correta(self) -> Optional[Alternativa]:
        """Retorna a alternativa correta da pergunta."""
        for a in self.alternativas:
            if a.correta:
                return a
        return None

    def alternativa_por_indice(self, idx: int) -> Optional[Alternativa]:
        """
        Retorna alternativa pela posição (0 a 3).

        Ex:
        0 = A
        1 = B
        2 = C
        3 = D
        """
        if 0 <= idx < len(self.alternativas):
            return self.alternativas[idx]
        return None

    def dica_eliminacao(self) -> Optional[Dica]:
        """Retorna a dica de eliminação, se existir."""
        for d in self.dicas:
            if d.tipo == "eliminacao":
                return d
        return None

    def dica_texto(self) -> Optional[Dica]:
        """Retorna a dica textual, se existir."""
        for d in self.dicas:
            if d.tipo == "texto":
                return d
        return None


# ---------------------------------------------------------
# MAPEAMENTO DE DIFICULDADE
# ---------------------------------------------------------
# Converte nomes usados no frontend para IDs do banco.
# ---------------------------------------------------------

NIVEL = {"facil": 1, "medio": 2, "dificil": 3}


# ---------------------------------------------------------
# GERADOR DE PERGUNTAS FALSAS (STUB)
# ---------------------------------------------------------
# Aqui simulamos perguntas reais de banco de dados.
# Isso permite testar o jogo sem backend.
# ---------------------------------------------------------

def _gerar_perguntas(id_nivel: int, quantidade: int) -> list[Pergunta]:
    """
    Cria perguntas fictícias para testes do jogo.
    """

    banco = [
        Pergunta(
            id_pergunta=1,
            enunciado="Qual é a fórmula química da água?",
            id_nivel=id_nivel,
            imagem_url=None,
            alternativas=[
                Alternativa(1, "H2O", None, True),
                Alternativa(2, "CO2", None, False),
                Alternativa(3, "NaCl", None, False),
                Alternativa(4, "O2", None, False),
            ],
            dicas=[
                Dica(1, "eliminacao", "Elimina duas alternativas erradas.", 10),
                Dica(2, "texto", "É formada por hidrogênio e oxigênio.", 5),
            ],
        ),
        Pergunta(
            id_pergunta=2,
            enunciado="Qual é o símbolo químico do ouro?",
            id_nivel=id_nivel,
            imagem_url=None,
            alternativas=[
                Alternativa(5, "Au", None, True),
                Alternativa(6, "Ag", None, False),
                Alternativa(7, "Fe", None, False),
                Alternativa(8, "Cu", None, False),
            ],
            dicas=[
                Dica(3, "eliminacao", "Elimina duas alternativas erradas.", 10),
                Dica(4, "texto", "Vem do latim Aurum.", 5),
            ],
        ),
        Pergunta(
            id_pergunta=3,
            enunciado="Quantos elétrons tem um átomo neutro de carbono?",
            id_nivel=id_nivel,
            imagem_url=None,
            alternativas=[
                Alternativa(9, "6", None, True),
                Alternativa(10, "12", None, False),
                Alternativa(11, "4", None, False),
                Alternativa(12, "8", None, False),
            ],
            dicas=[
                Dica(5, "eliminacao", "Elimina duas alternativas erradas.", 10),
                Dica(6, "texto", "O número atômico do carbono é 6.", 5),
            ],
        ),
    ]

    # Embaralha perguntas para simular banco real
    random.shuffle(banco)

    return banco[:quantidade]


# ---------------------------------------------------------
# CARREGAMENTO DE PERGUNTAS
# ---------------------------------------------------------

def carregar_perguntas(dificuldade: str) -> list[Pergunta]:
    """
    Busca perguntas para iniciar uma partida.

    Fluxo no sistema:
    1. Controller chama essa função
    2. Recebe lista de perguntas
    3. Mostra no jogo uma por uma

    Tipos de dificuldade:
    - facil
    - medio
    - dificil
    - aleatorio
    - milhao (modo especial com muitas perguntas)
    """

    if dificuldade in NIVEL:
        return backend_jogo.carregar_perguntas(str(NIVEL[dificuldade]))

    elif dificuldade == "aleatorio":
        return backend_jogo.carregar_perguntas("4")

    elif dificuldade == "milhao":
        return backend_jogo.carregar_perguntas("5")

    return []


# ---------------------------------------------------------
# SESSÃO DE JOGO
# ---------------------------------------------------------
# Uma sessão representa uma partida completa do aluno.
# Tudo que acontece no jogo é registrado dentro dela.
# ---------------------------------------------------------

def criar_sessao(id_usuario: int, id_nivel: int) -> Optional[int]:
    """Cria uma nova partida no banco."""
    backend_jogo.cursor.execute(
        "INSERT INTO sessao_jogo (id_usuario, id_nivel) VALUES (%s, %s)",
        (id_usuario, id_nivel),
    )
    backend_jogo.conexao.commit()
    return backend_jogo.cursor.lastrowid


def registrar_resposta(id_sessao, pergunta, alternativa, correta, tempo_seg):
    """
    Salva a resposta do aluno no banco.
    """
    backend_jogo.registrar_resposta(id_sessao, pergunta, alternativa, correta, tempo_seg)


def registrar_uso_dica(id_sessao, pergunta, dica):
    """
    Registra uso de dica durante a partida.
    """
    if dica is None:
        return

    id_dica = dica.get("id_dica") if isinstance(dica, dict) else getattr(dica, "id_dica", None)
    if id_dica is None:
        return

    backend_jogo.cursor.execute(
        "INSERT INTO uso_dica (id_sessao, id_pergunta, id_dica) VALUES (%s, %s, %s)",
        (id_sessao, pergunta.id_pergunta, id_dica),
    )
    backend_jogo.conexao.commit()


def finalizar_sessao(id_sessao: int, pontuacao: int):
    """
    Finaliza a partida e salva pontuação final.
    """
    backend_jogo.cursor.execute(
        "UPDATE sessao_jogo SET pontuacao = %s, concluida = 1, finalizado_em = NOW() WHERE id_sessao = %s",
        (pontuacao, id_sessao),
    )
    backend_jogo.conexao.commit()


# ---------------------------------------------------------
# RANKING
# ---------------------------------------------------------

def atualizar_ranking(id_usuario: int, id_nivel: int, pontuacao: int):
    """
    Atualiza ranking do aluno após a partida.
    """
    backend_jogo.atualizar_ranking(id_usuario, id_nivel, pontuacao)


def buscar_ranking(id_nivel: int, limite: int = 10) -> list[dict]:
    """
    Retorna ranking de um nível específico.
    """
    return [
        {"nome": "Ana Lima", "turma": "3INFO1", "melhor_pontuacao": 980},
        {"nome": "Bruno Melo", "turma": "2QUI2", "melhor_pontuacao": 850},
        {"nome": "Carla Dias", "turma": "3INFO1", "melhor_pontuacao": 720},
    ]


def buscar_ranking_geral(limite: int = 10) -> list[dict]:
    """
    Ranking geral somando todos os níveis.
    """
    return [
        {"nome": "Ana Lima", "turma": "3INFO1", "pontuacao_total": 2500},
        {"nome": "Carla Dias", "turma": "3INFO1", "pontuacao_total": 2100},
        {"nome": "Bruno Melo", "turma": "2QUI2", "pontuacao_total": 1900},
    ]


# ---------------------------------------------------------
# DESEMPENHO (RELATÓRIO DO PROFESSOR)
# ---------------------------------------------------------

def buscar_desempenho_geral() -> list[dict]:
    """Retorna estatísticas gerais das perguntas."""
    return [
        {
            "id_pergunta": 1,
            "enunciado": "Qual é a fórmula da água?",
            "id_nivel": 1,
            "total_respostas": 40,
            "total_acertos": 38,
            "taxa_acerto_pct": 95.0,
        }
    ]


def buscar_desempenho_aluno(id_usuario: int) -> list[dict]:
    """Retorna desempenho de um aluno específico."""
    return [
        {
            "id_pergunta": 1,
            "enunciado": "Qual é a fórmula da água?",
            "id_nivel": 1,
            "total_respostas": 3,
            "total_acertos": 3,
            "taxa_acerto_pct": 100.0,
        }
    ]


# ---------------------------------------------------------
# FUNÇÕES UTILITÁRIAS
# ---------------------------------------------------------

def ordenar_ranking_alunos(ranking_alunos: list[dict]) -> list[dict]:
    """Ordena alunos por pontuação (maior primeiro)."""
    return sorted(ranking_alunos, key=lambda x: x["pontos"], reverse=True)


def ordenar_ranking_turmas(ranking_turmas: list[dict]) -> list[dict]:
    """Ordena turmas por pontuação (maior primeiro)."""
    return sorted(ranking_turmas, key=lambda x: x["pontos"], reverse=True)


def calcular_media(acertos: int, total: int) -> float:
    """Calcula taxa de acerto (0 a 1)."""
    if total == 0:
        return 0
    return round(acertos / total, 2)


def adicionar_pontos(aluno: dict, pontos: int):
    """Adiciona pontos ao aluno (modifica o próprio dicionário)."""
    aluno["pontos"] += pontos


def filtrar_por_turma(ranking_alunos: list[dict], turma: str) -> list[dict]:
    """Filtra alunos por turma."""
    return [a for a in ranking_alunos if a["turma"] == turma]