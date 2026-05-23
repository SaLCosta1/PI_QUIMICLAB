from PySide6.QtWidgets import QWidget, QStackedWidget


def _escalar_widgets(parent, scale: float):
    for child in parent.findChildren(QWidget):
        if child.parent() is not parent:
            continue

        g = child.geometry()
        child.setGeometry(
            round(g.x() * scale),
            round(g.y() * scale),
            max(1, round(g.width()  * scale)),
            max(1, round(g.height() * scale)),
        )

        font = child.font()
        if font.pointSize() > 0:
            font.setPointSize(max(6, round(font.pointSize() * scale)))
            child.setFont(font)

        _escalar_widgets(child, scale)


def aplicar_escala(app, window, design_w=1920, design_h=1080):
    screen = app.primaryScreen().availableGeometry()
    scale  = min(screen.width() / design_w, screen.height() / design_h)

    if scale < 0.999:
        stack = window.findChild(QStackedWidget, "stack")
        if stack:
            stack.setFixedSize(round(design_w * scale), round(design_h * scale))
            for i in range(stack.count()):
                _escalar_widgets(stack.widget(i), scale)