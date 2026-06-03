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


# =========================================================
# CONFIGURAÇÃO DE FUNDOS ESPECIAIS
# =========================================================
# Alguns elementos de fundo não seguem o padrão normal da UI
# e precisam de ajuste manual de posição/tamanho.
# =========================================================

_FUNDOS_EXTRAS = {
    "fundo2_relatorio"
}


# =========================================================
# CORRIGE LAYOUT PRINCIPAL DA JANELA
# =========================================================
# O Qt pode carregar a UI sem layout correto em alguns casos.
# Essa função garante que o QStackedWidget fique encaixado
# corretamente na janela principal.
# =========================================================

def _corrigir_layout(window):
    """
    Garante que o layout principal da janela esteja correto.
    """

    # Widget central da janela (base da interface)
    cw = window.centralWidget()

    if cw is None:
        return

    # Stack de telas (cada página do sistema)
    stack = window.findChild(QStackedWidget, "stack")

    if stack is None:
        return

    # Cria layout vertical para organizar a UI
    layout = QVBoxLayout(cw)

    # Remove margens para ocupar tela inteira
    layout.setContentsMargins(0, 0, 0, 0)

    # Remove espaçamento entre elementos
    layout.setSpacing(0)

    # Adiciona o stack dentro do layout
    layout.addWidget(stack)


# =========================================================
# AJUSTE DE FUNDOS DAS TELAS
# =========================================================
# Garante que os elementos de fundo ocupem toda a tela
# independentemente do layout interno do Qt Designer.
# =========================================================

def _corrigir_fundos(window):
    """
    Força os backgrounds das telas a ocuparem toda a janela.
    """

    stack = window.findChild(QStackedWidget, "stack")

    if stack is None:
        return

    # Percorre todas as páginas do sistema (stacked widget)
    for i in range(stack.count()):

        page = stack.widget(i)

        # Procura todos os widgets dentro da página
        for child in page.findChildren(QWidget):

            name = child.objectName()

            # Identifica elementos de fundo
            if (
                name.startswith("fundo_")
                or name in _FUNDOS_EXTRAS
            ):
                # Força ocupar toda a tela (design fixo 1920x1080)
                child.setGeometry(0, 0, 1920, 1080)


# =========================================================
# RECARREGAMENTO DE IMAGENS (QLabel)
# =========================================================
# Essa função garante que todas as imagens sejam carregadas
# corretamente a partir da pasta assets/images.
# =========================================================

def _recarregar_pixmaps(window, images_dir: Path):
    """
    Atualiza imagens de labels após carregar a UI.
    """

    # Mapeia nome do QLabel → arquivo de imagem
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

        # (silencioso) evita prints em produção

        if not caminho.exists():
            continue

        # Procura QLabel pelo nome no Qt Designer
        widget = window.findChild(QLabel, name)

        if widget is None:
            continue

        pix = QPixmap(str(caminho))

        if pix.isNull():
            continue

        # Redimensiona imagem para caber no label
        widget.setPixmap(
            pix.scaled(
                widget.width() or pix.width(),
                widget.height() or pix.height(),
            )
        )


# =========================================================
# RECARREGAMENTO DE ÍCONES DOS BOTÕES
# =========================================================
# Aplica ícones em QPushButtons definidos no Qt Designer.
# =========================================================

def _recarregar_icones_botoes(window, images_dir: Path):
    """
    Define ícones dos botões dinamicamente.
    """

    mapa = {
        "btn_dicaexp":  "icone_dica.png",
        "btn_eliminar": "icone_lixo.png",
    }

    for name, filename in mapa.items():

        caminho = images_dir / filename

        # silencioso: não logar caminhos sensíveis

        if not caminho.exists():
            continue

        botao = window.findChild(QPushButton, name)

        if botao is None:
            continue

        # Remove texto do botão (fica só o ícone)
        botao.setText("")

        # Define ícone
        botao.setIcon(QIcon(str(caminho)))

        # Ajusta tamanho do ícone ao tamanho do botão
        botao.setIconSize(botao.size())


# =========================================================
# CARREGAMENTO PRINCIPAL DA INTERFACE (.ui)
# =========================================================
# Essa função é o "boot" da interface gráfica.
# Ela carrega o arquivo .ui e aplica correções necessárias.
# =========================================================

def carregar_ui(base_dir: Path):
    """
    Carrega a interface principal do sistema a partir do .ui.
    """

    # Caminho do arquivo de interface do Qt Designer
    ui_path = (
        base_dir
        / "app"
        / "ui"
        / "screens"
        / "front_viewer.ui"
    )

    # ui_path carregado a partir de base_dir

    # Guarda diretório atual (evita efeitos colaterais)
    cwd_original = os.getcwd()

    # Qt precisa estar no diretório da UI para carregar corretamente
    os.chdir(ui_path.parent)

    # Loader do Qt Designer (.ui → Python)
    loader = QUiLoader()

    # Carrega interface
    window = loader.load(str(ui_path))

    # Volta para diretório original
    os.chdir(cwd_original)

    # Se falhar, interrompe execução
    if window is None:
        raise RuntimeError("Erro ao carregar interface.")

    # Corrige estrutura da janela
    _corrigir_layout(window)

    # Ajusta fundos das telas
    _corrigir_fundos(window)

    # Caminho das imagens
    images_dir = base_dir / "app" / "assets" / "images"

    # Recarrega imagens dos labels
    _recarregar_pixmaps(window, images_dir)

    # Recarrega ícones dos botões
    _recarregar_icones_botoes(window, images_dir)

    return window


# =========================================================
# ÍCONE DA JANELA PRINCIPAL
# =========================================================
# Define o ícone que aparece na barra da janela.
# =========================================================

def aplicar_icone(window, base_dir: Path):
    """
    Define o ícone da aplicação (janela principal).
    """

    icone = base_dir / "app" / "assets" / "images" / "logoetec.png"

    if icone.exists():
        window.setWindowIcon(QIcon(str(icone)))