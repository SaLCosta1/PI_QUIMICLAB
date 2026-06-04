import re

from PySide6.QtCore import (
    QRect,
    QEasingCurve,
    QPropertyAnimation,
    QTimer,
)

from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QLabel,
    QGraphicsOpacityEffect,
)

class AnimationController:
    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.animacoes = []
        self.setup()

    def setup(self):
        for btn in self.window.findChildren(QPushButton):
            self.aplicar_bounce(btn)
            self.aplicar_hover(btn)

    def aplicar_bounce(self, botao):
        def animar():
            geo = botao.geometry()
            anim_ant = getattr(botao, "_bounce_anim", None)
            if (
                anim_ant
                and anim_ant.state() == QPropertyAnimation.State.Running
            ):
                anim_ant.stop()
                botao.setGeometry(geo)
            d = 8
            grande = QRect(
                geo.x() - d,
                geo.y() - d,
                geo.width() + d * 2,
                geo.height() + d * 2,
            )
            pequeno = QRect(
                geo.x() + d // 2,
                geo.y() + d // 2,
                geo.width() - d,
                geo.height() - d,
            )
            suave = QRect(
                geo.x() - d // 3,
                geo.y() - d // 3,
                geo.width() + (d // 3) * 2,
                geo.height() + (d // 3) * 2,
            )
            anim = QPropertyAnimation(botao, b"geometry")
            anim.setDuration(420)
            anim.setStartValue(geo)
            anim.setKeyValueAt(0.30, grande)
            anim.setKeyValueAt(0.65, pequeno)
            anim.setKeyValueAt(0.85, suave)
            anim.setEndValue(geo)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            geo_final = QRect(geo)
            anim.finished.connect(
                lambda: botao.setGeometry(geo_final)
            )
            botao._bounce_anim = anim
            self.animacoes.append(anim)
            anim.finished.connect(
                lambda: self.animacoes.remove(anim)
                if anim in self.animacoes else None
            )
            anim.start()
        botao.clicked.connect(
            lambda: QTimer.singleShot(0, animar)
        )

    def aplicar_hover(self, botao: QPushButton):
        ss = botao.styleSheet()
        if ":hover" in ss:
            return
        bg_match = re.search(
            r'background-color\s*:\s*([^;{}\n]+)',
            ss
        )
        bg = bg_match.group(1).strip().lower() if bg_match else ""
        hover_map = {
            "#921913": "#d43a31",
            "white": "#f0f0f0",
            "#ffffff": "#f0f0f0",
            "": "#e0e0e0",
        }
        hover_bg = hover_map.get(bg, "#e0e0e0")
        name = botao.objectName()
        selector = (
            f"QPushButton#{name}:hover"
            if name else
            "QPushButton:hover"
        )
        hover_css = (
            f"\n{selector} {{"
            f" background-color: {hover_bg};"
            f" opacity: 0.92;"
            f"}}"
        )
        botao.setStyleSheet(ss + hover_css)

    def fade_in_widget(self, widget: QWidget, duration: int = 350):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.finished.connect(
            lambda: widget.setGraphicsEffect(None)
        )
        self.animacoes.append(anim)
        anim.finished.connect(
            lambda: self.animacoes.remove(anim)
            if anim in self.animacoes else None
        )
        anim.start()

    def mostrar_label(self, label: QLabel, texto: str = "", cor: str = ""):
        if texto:
            label.setText(texto)
        if cor:
            ss = label.styleSheet()
            ss = re.sub(
                r'color\s*:\s*[^;]+;',
                f'color: {cor};',
                ss
            )
            if "color" not in ss:
                ss += f"\ncolor: {cor};"
            label.setStyleSheet(ss)
        label.show()
        self.fade_in_widget(label)
