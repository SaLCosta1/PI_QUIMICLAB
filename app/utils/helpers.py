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


def configurar_tabela(tabela):
    """Aplica o visual e o comportamento padrão (tema vermelho/branco) a uma QTableWidget."""
    tabela.setAlternatingRowColors(True)
    tabela.setEditTriggers(
        QAbstractItemView.EditTrigger.NoEditTriggers
    )
    tabela.setSelectionBehavior(
        QAbstractItemView.SelectionBehavior.SelectRows
    )
    tabela.setShowGrid(True)
    tabela.verticalHeader().setDefaultSectionSize(55)
    tabela.verticalHeader().setVisible(False)
    tabela.horizontalHeader().setDefaultSectionSize(120)
    tabela.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
    )
    tabela.horizontalHeader().setMinimumSectionSize(80)
    tabela.horizontalHeader().setDefaultAlignment(
        Qt.AlignmentFlag.AlignCenter
    )
    tabela.setHorizontalScrollMode(
        QAbstractItemView.ScrollMode.ScrollPerPixel
    )
    tabela.setVerticalScrollMode(
        QAbstractItemView.ScrollMode.ScrollPerPixel
    )
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
    """Destaca o valor de uma estatística (texto grande, negrito, centralizado, tema vermelho)."""
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
    """Aplica o estilo padrão (tema vermelho/branco) a um QListWidget."""
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


def criar_item_tabela(valor):
    """Cria uma célula de tabela já com o texto centralizado."""
    item = QTableWidgetItem(str(valor))
    item.setTextAlignment(
        Qt.AlignmentFlag.AlignCenter
    )
    return item


def fade_in_widget(widget: QWidget, duration=350):
    """Anima a opacidade do widget de 0 a 1 (efeito de aparecer suavemente)."""
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(
        QEasingCurve.Type.InOutQuad
    )
    # Remove o efeito ao terminar para não deixar resíduo visual.
    anim.finished.connect(
        lambda: widget.setGraphicsEffect(None)
    )
    anim.start()
    return anim


def mostrar_label(label: QLabel, texto="", cor=""):
    """Mostra um label com texto/cor opcionais e animação de entrada."""
    if texto:
        label.setText(texto)

    if cor:
        ss = label.styleSheet()
        ss = re.sub(
            r'color\s*:\s*[^;]+;',
            f'color: {cor};',
            ss
        )
        if 'color' not in ss:
            ss += f'\ncolor: {cor};'
        label.setStyleSheet(ss)

    label.show()
    anim = fade_in_widget(label)
    # Mantém referência à animação no label para o Python não coletá-la antes da hora.
    label._fade_anim = anim


def aplicar_cursor(botao: QPushButton):
    """Define cursor de mão (hover clicável) no botão."""
    botao.setCursor(
        Qt.CursorShape.PointingHandCursor
    )


def aplicar_hover(botao: QPushButton):
    """Adiciona regra CSS de hover ao botão, sem sobrescrever uma já existente."""
    ss = botao.styleSheet()
    if ":hover" in ss:
        return

    bg_match = re.search(
        r'background-color\s*:\s*([^;{}\n]+)',
        ss
    )
    bg = (
        bg_match.group(1).strip().lower()
        if bg_match else ""
    )

    hover_map = {
        "#921913": "#b52a22",
        "white": "#ececec",
        "#ffffff": "#ececec",
        "": "#cccccc",
    }
    hover_bg = hover_map.get(bg, "#aaaaaa")

    name = botao.objectName()
    if name:
        selector = f"QPushButton#{name}:hover"
    else:
        selector = "QPushButton:hover"

    hover_css = (
        f"\n{selector} {{"
        f" background-color: {hover_bg};"
        f" opacity: 0.92;"
        f"}}"
    )
    botao.setStyleSheet(ss + hover_css)
