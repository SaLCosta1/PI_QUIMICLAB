import re
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader


def corrigir_caminhos_ui(ui_path: Path, base_dir: Path) -> str:

    content = ui_path.read_text(encoding="utf-8")

    images_dir = (base_dir / "images").resolve()

    def fix(match):
        novo = images_dir / Path(match.group(2)).name
        return f"{match.group(1)}{novo.as_posix()}{match.group(3)}"

    patterns = [
        r'(<pixmap>)(.*?\.(?:png|jpg|jpeg|ico))(</pixmap>)',
        r'(<string>)(.*?\.(?:png|jpg|jpeg|ico))(</string>)',
        r'(<normaloff>)(.*?)(</normaloff>)',
    ]

    for pattern in patterns:
        content = re.sub(pattern, fix, content, flags=re.IGNORECASE)

    return content


def carregar_ui(base_dir: Path):

    ui_path = base_dir / "app" / "ui" / "front_viewer.ui"

    ui_corrigido = corrigir_caminhos_ui(ui_path, base_dir)

    ui_temp = base_dir / "_temp_ui.ui"
    ui_temp.write_text(ui_corrigido, encoding="utf-8")

    loader = QUiLoader()
    window = loader.load(str(ui_temp))

    if ui_temp.exists():
        ui_temp.unlink()

    if window is None:
        raise RuntimeError("Erro ao carregar a interface.")

    return window


def aplicar_icone(window, base_dir: Path):

    icone = base_dir / "images" / "icone.png"

    if icone.exists():
        window.setWindowIcon(QIcon(str(icone)))