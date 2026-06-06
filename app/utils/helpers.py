from PySide6.QtWidgets import (
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QWidget,
    QPushButton,
    QGraphicsOpacityEffect,
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
)

import re


# =========================================================
# CONFIGURAÇÃO DE TABELA (QTableWidget)
# =========================================================
# Essa função padroniza o comportamento visual e interativo
# de todas as tabelas do sistema.
#
# Em vez de configurar manualmente em cada tela, o projeto
# centraliza isso aqui.
# =========================================================

def configurar_tabela(tabela):
    """
    Aplica um padrão visual e de comportamento para tabelas.

    Isso garante que TODAS as tabelas do sistema fiquem iguais.
    """

    # Alterna cores entre linhas (melhora leitura visual)
    tabela.setAlternatingRowColors(True)

    # Impede edição direta das células pelo usuário
    tabela.setEditTriggers(
        QAbstractItemView.EditTrigger.NoEditTriggers
    )

    # Define que a seleção é por LINHA inteira (não célula)
    tabela.setSelectionBehavior(
        QAbstractItemView.SelectionBehavior.SelectRows
    )

    # Mostra grade da tabela
    tabela.setShowGrid(True)

    # Altura padrão de cada linha
    tabela.verticalHeader().setDefaultSectionSize(55)

    # Esconde numeração lateral (1,2,3...)
    tabela.verticalHeader().setVisible(False)

    # Largura padrão das colunas
    tabela.horizontalHeader().setDefaultSectionSize(120)

    # Faz colunas se ajustarem automaticamente ao espaço
    tabela.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
    )

    # Define largura mínima para colunas
    tabela.horizontalHeader().setMinimumSectionSize(80)

    # Centraliza texto dos cabeçalhos
    tabela.horizontalHeader().setDefaultAlignment(
        Qt.AlignmentFlag.AlignCenter
    )

    # Rolagem suave horizontal
    tabela.setHorizontalScrollMode(
        QAbstractItemView.ScrollMode.ScrollPerPixel
    )

    # Rolagem suave vertical
    tabela.setVerticalScrollMode(
        QAbstractItemView.ScrollMode.ScrollPerPixel
    )

    # Estilo padrão (tema vermelho/branco) das tabelas
    tabela.setStyleSheet("""
        QTableWidget {
            background-color: white;
            alternate-background-color: #f7eeed;
            border: 2px solid #921913;
            border-radius: 12px;
            gridline-color: #e6d2d0;
            font-size: 18px;
        }
        QTableWidget::item {
            padding: 6px;
            color: #333333;
        }
        QTableWidget::item:selected {
            background-color: #f0cfcc;
            color: #921913;
        }
        QHeaderView::section {
            background-color: #921913;
            color: white;
            font-weight: bold;
            font-size: 18px;
            border: none;
            padding: 8px;
        }
    """)


def estilo_valor(label):
    """
    Destaca o VALOR de uma estatística nos relatórios: texto grande, em
    negrito, centralizado, no tema vermelho/branco. Deixa os números das
    caixas ("acertos", "média", etc.) com bem mais destaque.
    """
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setWordWrap(True)
    label.setStyleSheet("""
        QLabel {
            background-color: white;
            border: 2px solid #921913;
            border-radius: 16px;
            color: #921913;
            font-size: 28px;
            font-weight: bold;
            padding: 4px 12px;
        }
    """)


def configurar_lista(lista):
    """
    Aplica o estilo padrão (tema vermelho/branco) a um QListWidget.
    Usado nas telas de relatório para deixá-las mais agradáveis.
    """
    lista.setStyleSheet("""
        QListWidget {
            background-color: white;
            border: 2px solid #921913;
            border-radius: 12px;
            font-size: 18px;
            padding: 6px;
        }
        QListWidget::item {
            padding: 10px;
            border-bottom: 1px solid #f0e2e1;
            color: #333333;
        }
        QListWidget::item:selected {
            background-color: #921913;
            color: white;
            border-radius: 8px;
        }
        QListWidget::item:hover {
            background-color: #f3d9d7;
        }
    """)


# =========================================================
# CRIA ITEM PADRONIZADO PARA TABELA
# =========================================================
# Essa função evita repetição de código ao criar células.
# Sempre centraliza o texto automaticamente.
# =========================================================

def criar_item_tabela(valor):
    """
    Cria um item de tabela já formatado (centralizado).
    """

    item = QTableWidgetItem(str(valor))

    # Centraliza o conteúdo dentro da célula
    item.setTextAlignment(
        Qt.AlignmentFlag.AlignCenter
    )

    return item


# =========================================================
# ANIMAÇÃO: FADE IN
# =========================================================
# Cria um efeito de "aparecer suavemente" em widgets.
# Usado para melhorar a experiência visual da interface.
# =========================================================

def fade_in_widget(widget: QWidget, duration=350):
    """
    Aplica animação de fade-in (opacidade de 0 → 1).
    """

    # Cria efeito de transparência no widget
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    # Define animação da propriedade "opacity"
    anim = QPropertyAnimation(effect, b"opacity")

    anim.setDuration(duration)  # duração da animação

    anim.setStartValue(0.0)     # começa invisível
    anim.setEndValue(1.0)       # termina totalmente visível

    # Curva de animação (suavidade)
    anim.setEasingCurve(
        QEasingCurve.Type.InOutQuad
    )

    # Remove o efeito após terminar (evita impacto visual/bug)
    anim.finished.connect(
        lambda: widget.setGraphicsEffect(None)
    )

    anim.start()

    return anim


# =========================================================
# MOSTRAR LABEL COM ANIMAÇÃO
# =========================================================
# Mostra texto em um QLabel com fade-in e opção de cor.
# =========================================================

def mostrar_label(label: QLabel, texto="", cor=""):
    """
    Exibe um label com texto e animação de entrada.

    Também permite alterar a cor via CSS.
    """

    # Atualiza texto se fornecido
    if texto:
        label.setText(texto)

    # Se uma cor foi passada, altera no styleSheet
    if cor:

        ss = label.styleSheet()

        # Substitui cor existente se houver
        ss = re.sub(
            r'color\s*:\s*[^;]+;',
            f'color: {cor};',
            ss
        )

        # Se não existir cor definida, adiciona
        if 'color' not in ss:
            ss += f'\ncolor: {cor};'

        label.setStyleSheet(ss)

    # Torna o label visível
    label.show()

    # Aplica animação de fade-in
    anim = fade_in_widget(label)

    # IMPORTANTE:
    # Mantém referência da animação no próprio label
    # para evitar que o Python "limpe" o objeto antes da hora
    label._fade_anim = anim


# =========================================================
# CURSOR PADRÃO PARA BOTÕES
# =========================================================
# Melhora UX: transforma cursor em "mão" ao passar no botão
# =========================================================

def aplicar_cursor(botao: QPushButton):
    """
    Define cursor de mão (hover clicável).
    """

    botao.setCursor(
        Qt.CursorShape.PointingHandCursor
    )


# =========================================================
# HOVER VISUAL PARA BOTÕES
# =========================================================
# Adiciona efeito visual quando o mouse passa sobre o botão.
# =========================================================

def aplicar_hover(botao: QPushButton):
    """
    Adiciona estilo CSS de hover automaticamente.
    Evita duplicar regras manualmente em cada botão.
    """

    ss = botao.styleSheet()

    # Se já tem hover definido, não sobrescreve
    if ":hover" in ss:
        return

    # Tenta identificar cor de fundo atual do botão
    bg_match = re.search(
        r'background-color\s*:\s*([^;{}\n]+)',
        ss
    )

    bg = (
        bg_match.group(1).strip().lower()
        if bg_match else ""
    )

    # Mapeia cores base → hover correspondente
    hover_map = {
        "#921913": "#b52a22",
        "white": "#ececec",
        "#ffffff": "#ececec",
        "": "#cccccc",
    }

    hover_bg = hover_map.get(bg, "#aaaaaa")

    # Permite estilizar botão específico ou geral
    name = botao.objectName()

    if name:
        selector = f"QPushButton#{name}:hover"
    else:
        selector = "QPushButton:hover"

    # CSS final do hover
    hover_css = (
        f"\n{selector} {{"
        f" background-color: {hover_bg};"
        f" opacity: 0.92;"
        f"}}"
    )

    # Aplica novo estilo sem remover o antigo
    botao.setStyleSheet(ss + hover_css)