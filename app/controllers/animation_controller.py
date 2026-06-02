# =========================================================
# IMPORTAÇÕES
# =========================================================

# Biblioteca utilizada para trabalhar com expressões regulares.
# Neste controller, ela é usada para localizar e alterar
# propriedades de estilo (CSS) dos botões.
import re

# ---------------------------------------------------------
# IMPORTAÇÕES DO PySide6.QtCore
# ---------------------------------------------------------

# QRect:
# Classe responsável por representar retângulos.
# É utilizada para controlar posição e tamanho dos widgets
# durante as animações.

# QEasingCurve:
# Define o comportamento da animação ao longo do tempo,
# tornando os movimentos mais suaves e naturais.

# QPropertyAnimation:
# Classe principal utilizada para criar animações em widgets.

# QTimer:
# Permite executar ações após um determinado intervalo de tempo.
from PySide6.QtCore import (
    QRect,
    QEasingCurve,
    QPropertyAnimation,
    QTimer,
)

# ---------------------------------------------------------
# IMPORTAÇÕES DO PySide6.QtWidgets
# ---------------------------------------------------------

# QPushButton:
# Classe dos botões da interface gráfica.

# QWidget:
# Classe base de praticamente todos os componentes visuais.

# QLabel:
# Widget utilizado para exibir textos.

# QGraphicsOpacityEffect:
# Permite controlar efeitos de transparência/opacidade.
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QLabel,
    QGraphicsOpacityEffect,
)


# =========================================================
# CONTROLLER DE ANIMAÇÕES
# =========================================================

class AnimationController:

    # =====================================================
    # MÉTODO CONSTRUTOR
    # =====================================================

    def __init__(self, main):

        # Referência da classe principal do sistema.
        self.main = main

        # Referência direta da janela principal.
        self.window = main.window

        # Lista utilizada para armazenar animações ativas.
        # Isso impede que o Python destrua a animação antes
        # do término de sua execução.
        self.animacoes = []

        # Inicializa as configurações do controller.
        self.setup()

    # =====================================================
    # CONFIGURAÇÃO INICIAL
    # =====================================================

    def setup(self):

        # Percorre automaticamente todos os botões presentes
        # na interface principal.
        for btn in self.window.findChildren(QPushButton):

            # Aplica animação de clique.
            self.aplicar_bounce(btn)

            # Aplica efeito visual de hover.
            self.aplicar_hover(btn)

    # =====================================================
    # ANIMAÇÃO DE CLIQUE (BOUNCE)
    # =====================================================

    def aplicar_bounce(self, botao):

        # Função interna responsável pela animação.
        def animar():

            # Obtém a geometria atual do botão
            # (posição e dimensões).
            geo = botao.geometry()

            # Verifica se já existe uma animação ativa.
            anim_ant = getattr(botao, "_bounce_anim", None)

            if (
                anim_ant
                and anim_ant.state() == QPropertyAnimation.State.Running
            ):

                # Interrompe animações anteriores para evitar
                # conflitos visuais.
                anim_ant.stop()

                # Restaura a geometria original do botão.
                botao.setGeometry(geo)

            # Intensidade do efeito.
            d = 8

            # -------------------------------------------------
            # GEOMETRIA EXPANDIDA
            # -------------------------------------------------

            # Faz o botão aumentar de tamanho.
            grande = QRect(
                geo.x() - d,
                geo.y() - d,
                geo.width() + d * 2,
                geo.height() + d * 2,
            )

            # -------------------------------------------------
            # GEOMETRIA REDUZIDA
            # -------------------------------------------------

            # Faz o botão diminuir levemente de tamanho.
            pequeno = QRect(
                geo.x() + d // 2,
                geo.y() + d // 2,
                geo.width() - d,
                geo.height() - d,
            )

            # -------------------------------------------------
            # GEOMETRIA INTERMEDIÁRIA
            # -------------------------------------------------

            # Utilizada para suavizar o retorno ao tamanho normal.
            suave = QRect(
                geo.x() - d // 3,
                geo.y() - d // 3,
                geo.width() + (d // 3) * 2,
                geo.height() + (d // 3) * 2,
            )

            # -------------------------------------------------
            # CRIAÇÃO DA ANIMAÇÃO
            # -------------------------------------------------

            anim = QPropertyAnimation(botao, b"geometry")

            # Define duração total da animação.
            anim.setDuration(420)

            # Define geometria inicial.
            anim.setStartValue(geo)

            # Define etapas intermediárias da animação.
            anim.setKeyValueAt(0.30, grande)
            anim.setKeyValueAt(0.65, pequeno)
            anim.setKeyValueAt(0.85, suave)

            # Define geometria final.
            anim.setEndValue(geo)

            # Define suavização do movimento.
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)

            # -------------------------------------------------
            # RESTAURAÇÃO FINAL
            # -------------------------------------------------

            # Garante que o botão termine exatamente
            # na posição original.
            geo_final = QRect(geo)

            anim.finished.connect(
                lambda: botao.setGeometry(geo_final)
            )

            # Salva referência da animação no botão.
            botao._bounce_anim = anim

            # Armazena animação na lista de animações ativas.
            self.animacoes.append(anim)

            # Remove animação da lista após o término.
            anim.finished.connect(
                lambda: self.animacoes.remove(anim)
                if anim in self.animacoes else None
            )

            # Inicia a animação.
            anim.start()

        # -----------------------------------------------------
        # CONEXÃO DO EVENTO DE CLIQUE
        # -----------------------------------------------------

        # O QTimer.singleShot(0) executa a animação logo após
        # o clique ser processado pelo sistema, evitando
        # inconsistências de escala e geometria.
        botao.clicked.connect(
            lambda: QTimer.singleShot(0, animar)
        )

    # =====================================================
    # EFEITO HOVER DOS BOTÕES
    # =====================================================

    def aplicar_hover(self, botao: QPushButton):

        # Obtém o stylesheet atual do botão.
        ss = botao.styleSheet()

        # Evita adicionar múltiplos efeitos hover.
        if ":hover" in ss:
            return

        # -------------------------------------------------
        # IDENTIFICA COR DE FUNDO ATUAL
        # -------------------------------------------------

        bg_match = re.search(
            r'background-color\s*:\s*([^;{}\n]+)',
            ss
        )

        bg = bg_match.group(1).strip().lower() if bg_match else ""

        # -------------------------------------------------
        # MAPEAMENTO DE CORES DE HOVER
        # -------------------------------------------------

        hover_map = {
            "#921913": "#b52a22",
            "white":   "#ececec",
            "#ffffff": "#ececec",
            "":        "#cccccc",
        }

        # Seleciona a cor de hover correspondente.
        hover_bg = hover_map.get(bg, "#aaaaaa")

        # Obtém o objectName do botão.
        name = botao.objectName()

        # Define seletor CSS específico.
        selector = (
            f"QPushButton#{name}:hover"
            if name else
            "QPushButton:hover"
        )

        # -------------------------------------------------
        # CSS DE HOVER
        # -------------------------------------------------

        hover_css = (
            f"\n{selector} {{"
            f" background-color: {hover_bg};"
            f" opacity: 0.92;"
            f"}}"
        )

        # Adiciona o hover ao stylesheet atual.
        botao.setStyleSheet(ss + hover_css)

    # =====================================================
    # ANIMAÇÃO FADE IN
    # =====================================================

    def fade_in_widget(self, widget: QWidget, duration: int = 350):

        # Cria efeito de opacidade.
        effect = QGraphicsOpacityEffect(widget)

        # Aplica efeito ao widget.
        widget.setGraphicsEffect(effect)

        # Cria animação da propriedade "opacity".
        anim = QPropertyAnimation(effect, b"opacity")

        # Define duração da animação.
        anim.setDuration(duration)

        # Define opacidade inicial e final.
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)

        # Define suavização do efeito.
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Remove efeito após finalização.
        anim.finished.connect(
            lambda: widget.setGraphicsEffect(None)
        )

        # Armazena animação ativa.
        self.animacoes.append(anim)

        # Remove da lista após finalização.
        anim.finished.connect(
            lambda: self.animacoes.remove(anim)
            if anim in self.animacoes else None
        )

        # Inicia animação.
        anim.start()

    # =====================================================
    # EXIBIÇÃO DE LABEL COM ANIMAÇÃO
    # =====================================================

    def mostrar_label(self, label: QLabel, texto: str = "", cor: str = ""):

        # Atualiza texto da label, caso informado.
        if texto:
            label.setText(texto)

        # Atualiza cor da label, caso informada.
        if cor:

            ss = label.styleSheet()

            # Substitui propriedade de cor existente.
            ss = re.sub(
                r'color\s*:\s*[^;]+;',
                f'color: {cor};',
                ss
            )

            # Caso não exista propriedade de cor,
            # adiciona ao stylesheet.
            if "color" not in ss:
                ss += f"\ncolor: {cor};"

            label.setStyleSheet(ss)

        # Exibe a label.
        label.show()

        # Aplica animação fade in.
        self.fade_in_widget(label)