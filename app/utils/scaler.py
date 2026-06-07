# Redimensiona a interface para o monitor atual.
# O design foi feito em 1920x1080; aqui tudo é escalado proporcionalmente.

import re

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QRect

# Tamanho base usado no design da interface.
DESIGN_W = 1920
DESIGN_H = 1080


def _escalar_fonte(child, ff: float):
    # Escala a fonte do widget tanto pelo pointSize (Qt Designer) quanto pelo
    # "font-size: Npx" do stylesheet; senão o texto não acompanha e estoura a caixa.
    if ff <= 0:
        return

    fonte = child.font()
    ps = fonte.pointSizeF()
    if ps > 0:
        fonte.setPointSizeF(ps * ff)
        child.setFont(fonte)

    ss = child.styleSheet()
    if ss and "font-size" in ss:
        ss = re.sub(
            r"font-size:\s*(\d+)px",
            lambda m: f"font-size: {max(1, round(int(m.group(1)) * ff))}px",
            ss,
        )
        child.setStyleSheet(ss)


def _escalar_widgets(widget: QWidget, fx: float, fy: float):
    # Ajusta posição e tamanho de todos os widgets filhos. fx/fy = fatores horizontal/vertical.
    # ff usa o menor fator para o texto nunca ficar maior que a caixa.
    ff = min(fx, fy)

    for child in widget.findChildren(QWidget):
        geo = child.geometry()
        novo = QRect(
            round(geo.x()      * fx),
            round(geo.y()      * fy),
            round(geo.width()  * fx),
            round(geo.height() * fy),
        )
        child.setGeometry(novo)
        _escalar_fonte(child, ff)


def aplicar_escala(app, window):
    """Detecta a resolução do monitor e redimensiona toda a UI proporcionalmente."""
    screen = app.primaryScreen()
    if screen is None:
        return

    disponivel = screen.availableGeometry()
    mon_w = disponivel.width()
    mon_h = disponivel.height()

    fx = mon_w / DESIGN_W
    fy = mon_h / DESIGN_H

    _escalar_widgets(window, fx, fy)
    window.setMinimumSize(0, 0)
    window.resize(mon_w, mon_h)
