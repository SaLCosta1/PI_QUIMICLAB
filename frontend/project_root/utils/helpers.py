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
# CONFIGURAR TABELA
# =========================================================

def configurar_tabela(tabela):

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


# =========================================================
# CENTRALIZAR ITEM DE TABELA
# =========================================================

def criar_item_tabela(valor):

    item = QTableWidgetItem(str(valor))

    item.setTextAlignment(
        Qt.AlignmentFlag.AlignCenter
    )

    return item


# =========================================================
# FADE IN
# =========================================================

def fade_in_widget(widget: QWidget, duration=350):

    effect = QGraphicsOpacityEffect(widget)

    widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")

    anim.setDuration(duration)

    anim.setStartValue(0.0)

    anim.setEndValue(1.0)

    anim.setEasingCurve(
        QEasingCurve.Type.InOutQuad
    )

    anim.finished.connect(
        lambda: widget.setGraphicsEffect(None)
    )

    anim.start()

    return anim


# =========================================================
# MOSTRAR LABEL
# =========================================================

def mostrar_label(label: QLabel, texto="", cor=""):

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

    fade_in_widget(label)


# =========================================================
# APLICAR CURSOR
# =========================================================

def aplicar_cursor(botao: QPushButton):

    botao.setCursor(
        Qt.CursorShape.PointingHandCursor
    )


# =========================================================
# APLICAR HOVER
# =========================================================

def aplicar_hover(botao: QPushButton):

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