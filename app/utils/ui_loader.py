import os
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


# Fundos que não seguem o padrão e precisam ser forçados a ocupar a tela toda.
_FUNDOS_EXTRAS = {
    "fundo2_relatorio"
}


def _corrigir_layout(window):
    # Encaixa o QStackedWidget no widget central (a UI nem sempre vem com layout).
    cw = window.centralWidget()
    if cw is None:
        return

    stack = window.findChild(QStackedWidget, "stack")
    if stack is None:
        return

    layout = QVBoxLayout(cw)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(stack)


def _corrigir_fundos(window):
    # Força os widgets de fundo a ocuparem a tela inteira (design fixo 1920x1080).
    stack = window.findChild(QStackedWidget, "stack")
    if stack is None:
        return

    for i in range(stack.count()):
        page = stack.widget(i)
        for child in page.findChildren(QWidget):
            name = child.objectName()
            if (
                name.startswith("fundo_")
                or name in _FUNDOS_EXTRAS
            ):
                child.setGeometry(0, 0, 1920, 1080)


def _recarregar_pixmaps(window, images_dir: Path):
    # Reaplica as imagens dos QLabel a partir da pasta assets/images.
    mapa = {
        "img_logoetec":        "logoetec.png",
        "img_logocps":         "logocps.png",
        "img_logoetec_2":      "logoetec.png",
        "img_logocps_2":       "logocps.png",
        "img_logoetec_3":      "logoetec.png",
        "img_logocps_3":       "logocps.png",
        "img_iconecursor":     "iconecursor.png",
        "img_relogio_questao": "iconerelogio.png",
    }

    for name, filename in mapa.items():
        caminho = images_dir / filename
        if not caminho.exists():
            continue

        widget = window.findChild(QLabel, name)
        if widget is None:
            continue

        pix = QPixmap(str(caminho))
        if pix.isNull():
            continue

        widget.setPixmap(
            pix.scaled(
                widget.width() or pix.width(),
                widget.height() or pix.height(),
            )
        )


def _recarregar_icones_botoes(window, images_dir: Path):
    # Aplica os ícones (sem texto) nos botões de dica e eliminar.
    mapa = {
        "btn_dicaexp":  "icone_dica.png",
        "btn_eliminar": "icone_lixo.png",
    }

    for name, filename in mapa.items():
        caminho = images_dir / filename
        if not caminho.exists():
            continue

        botao = window.findChild(QPushButton, name)
        if botao is None:
            continue

        botao.setText("")
        botao.setIcon(QIcon(str(caminho)))
        botao.setIconSize(botao.size())


def carregar_ui(base_dir: Path):
    """Carrega a interface do .ui (Qt Designer) e aplica as correções de layout/imagens."""
    ui_path = (
        base_dir
        / "app"
        / "ui"
        / "screens"
        / "front_viewer.ui"
    )

    # O Qt precisa estar no diretório da UI para resolver os caminhos relativos dela.
    cwd_original = os.getcwd()
    os.chdir(ui_path.parent)

    loader = QUiLoader()
    window = loader.load(str(ui_path))

    os.chdir(cwd_original)

    if window is None:
        raise RuntimeError("Erro ao carregar interface.")

    _corrigir_layout(window)
    _corrigir_fundos(window)

    images_dir = base_dir / "app" / "assets" / "images"
    _recarregar_pixmaps(window, images_dir)
    _recarregar_icones_botoes(window, images_dir)

    return window


def aplicar_icone(window, base_dir: Path):
    """Define o ícone da janela principal."""
    icone = base_dir / "app" / "assets" / "images" / "logoetec.png"
    if icone.exists():
        window.setWindowIcon(QIcon(str(icone)))
