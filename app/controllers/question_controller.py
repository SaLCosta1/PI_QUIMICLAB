# =========================================================
# QUESTION CONTROLLER
# =========================================================
#
# Responsável pelo fluxo principal do jogo:
# tipo de jogo → seleção de modo → perguntas →
# feedback → gabarito.
#
# Atualmente este controller funciona apenas
# no FRONT-END (visual da aplicação), sem integração
# com banco de dados ou backend real.
#
# Principais responsabilidades:
# - Controlar navegação entre páginas do jogo
# - Exibir perguntas e alternativas
# - Controlar timer da questão
# - Registrar respostas do usuário
# - Mostrar feedback visual
# - Exibir gabarito ao final
# - Gerenciar ajudas (dica e eliminar alternativas)
#
# =========================================================

import random
from pathlib import Path

from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox


# =========================================================
# CONFIGURAÇÃO GLOBAL
# =========================================================

# Tempo padrão de cada questão em segundos
TEMPO_POR_QUESTAO = 120


# =========================================================
# ESTILO PADRÃO DAS ALTERNATIVAS
# =========================================================
#
# Utilizado para restaurar o visual original
# dos botões após mudanças de estado.
#
# =========================================================

_STYLE_ALT = """
QPushButton{
    background-color: white;
    border: 2px solid #921913;
    border-radius: 25px;
    color: black;
}

QPushButton:hover{
    background-color: #6f6f6f;
}
"""


# =========================================================
# CLASSE PRINCIPAL
# =========================================================

class QuestionController:

    def __init__(self, main):

        # -------------------------------------------------
        # Referência principal da aplicação
        # -------------------------------------------------

        self.main = main

        # Atalho para janela principal
        w = main.window

        # Método responsável por trocar páginas
        ir = main.ir_para

        # =================================================
        # CARREGAMENTO DE ÍCONES
        # =================================================
        #
        # Define caminhos das imagens utilizadas
        # nos botões de dica e eliminar.
        #
        # =================================================

        base = Path(__file__).resolve().parent.parent

        icone_dica = str(
            base / "assets" / "images" / "icone_dica.png"
        )

        icone_lixo = str(
            base / "assets" / "images" / "icone_lixo.png"
        )

        # =================================================
        # ESTADO DA PARTIDA
        # =================================================
        #
        # Variáveis utilizadas para controlar
        # o andamento do jogo.
        #
        # =================================================

        # Tipo de jogo atual
        self._modo = "tradicional"

        # Dificuldade atual
        self._dificuldade = "medio"

        # Lista de perguntas da partida
        self._perguntas = []

        # Índice da pergunta atual
        self._indice = 0

        # Quantidade de acertos
        self._acertos = 0

        # Histórico de respostas
        self._respostas = []

        # Alternativas eliminadas
        self._eliminadas = []

        # Estado da dica
        self._dica_visivel = False

        # Controle de uso da ajuda
        self._ajuda_usada = False

        # Timer principal da questão
        self._timer = QTimer()

        # Tempo restante da questão atual
        self._tempo_restante = TEMPO_POR_QUESTAO

        # =================================================
        # CONFIGURAÇÃO DOS BOTÕES
        # =================================================
        #
        # Conecta ações dos botões aos métodos
        # correspondentes do controller.
        #
        # =================================================

        # -------------------------------------------------
        # PÁGINA: TIPO DE JOGO
        # -------------------------------------------------

        w.btn_voltar_tipojogo.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )

        w.btn_tradicional.clicked.connect(
            lambda: self._escolher_modo("tradicional")
        )

        w.btn_desafio.clicked.connect(
            lambda: self._iniciar_jogo("desafio")
        )

        # -------------------------------------------------
        # PÁGINA: MODOS
        # -------------------------------------------------

        w.btn_voltarperfil4.clicked.connect(
            lambda: ir(w.pg_tipo_jogo)
        )

        w.btn_facil.clicked.connect(
            lambda: self._iniciar_jogo("facil")
        )

        w.btn_medio.clicked.connect(
            lambda: self._iniciar_jogo("medio")
        )

        w.btn_dificil.clicked.connect(
            lambda: self._iniciar_jogo("dificil")
        )

        # -------------------------------------------------
        # PÁGINA: QUESTÃO
        # -------------------------------------------------

        # Alternativas de resposta
        w.btn_altA.clicked.connect(
            lambda: self._responder("A")
        )

        w.btn_altB.clicked.connect(
            lambda: self._responder("B")
        )

        w.btn_altC.clicked.connect(
            lambda: self._responder("C")
        )

        w.btn_altD.clicked.connect(
            lambda: self._responder("D")
        )

        # Botão de eliminar alternativas
        w.btn_eliminar.clicked.connect(
            self._eliminar_alternativa
        )

        # Botão de dica
        w.btn_dicaexp.clicked.connect(
            self._mostrar_dica
        )

        # -------------------------------------------------
        # PÁGINA: FEEDBACK
        # -------------------------------------------------

        w.btn_gabarito.clicked.connect(
            self._ir_gabarito
        )

        # -------------------------------------------------
        # PÁGINA: GABARITO
        # -------------------------------------------------

        w.btn_voltarmodos3_2.clicked.connect(
            self._voltar_ao_inicio_pos_jogo
        )

        w.comboBox_escolherpergunta_2.currentIndexChanged.connect(
            self._mostrar_gabarito_questao
        )

        # =================================================
        # CONFIGURAÇÃO DO TIMER
        # =================================================

        self._timer.timeout.connect(
            self._tick_timer
        )

    # =========================================================
    # CONTROLE DE FLUXO
    # =========================================================

    def _escolher_modo(self, modo):
        """
        Salva o modo escolhido e envia o usuário
        para a tela de seleção de dificuldade.
        """

        self._modo = modo

        self.main.ir_para(
            self.main.window.pg_modos
        )

    def _iniciar_jogo(self, dificuldade):
        """
        Inicializa uma nova partida.

        Responsabilidades:
        - Define modo e dificuldade
        - Reseta variáveis da partida
        - Abre a tela inicial de questão
        """

        # ---------------------------------------------
        # MODO DESAFIO
        # ---------------------------------------------

        if dificuldade == "desafio":

            self._modo = "desafio"
            self._dificuldade = "desafio"

        # ---------------------------------------------
        # MODO TRADICIONAL
        # ---------------------------------------------

        else:

            self._modo = "tradicional"
            self._dificuldade = dificuldade

        # Reinicia variáveis da sessão
        self._perguntas = []
        self._indice = 0
        self._acertos = 0
        self._respostas = []

        self._mostrar_tela_questao_vazia()

    def _mostrar_tela_questao_vazia(self):
        """
        Exibe a tela de questão sem conteúdo.

        Utilizado atualmente enquanto não há
        integração com backend real.
        """

        w = self.main.window

        # Reinicia estados auxiliares
        self._eliminadas = []
        self._dica_visivel = False
        self._ajuda_usada = False

        # Esconde dica
        w.txt_dica.hide()

        # Limpa textos principais
        w.lbl_pergunta.setText("")

        # Limpa alternativas
        w.btn_altA.setText("")
        w.btn_altB.setText("")
        w.btn_altC.setText("")
        w.btn_altD.setText("")

        # Limpa informações de nível
        w.lbl_infonivel.setText("")

        # Restaura visual original dos botões
        for btn in (
            w.btn_altA,
            w.btn_altB,
            w.btn_altC,
            w.btn_altD
        ):
            btn.setEnabled(True)
            btn.setStyleSheet(_STYLE_ALT)

        # Exibe botões auxiliares
        w.btn_dicaexp.show()
        w.btn_eliminar.show()

        # Reinicia timer
        self._tempo_restante = TEMPO_POR_QUESTAO

        w.lbl_timer.setText(
            str(self._tempo_restante)
        )

        self._timer.start(1000)

        # Navega para página da questão
        self.main.ir_para(w.pg_questao)