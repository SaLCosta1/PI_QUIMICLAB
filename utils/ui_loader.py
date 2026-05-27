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
 
 
def _corrigir_fundos(window):
    """
    O QUiLoader não propaga tamanho para widgets filhos sem layout.
    Força todos os fundo_* a ocuparem 1920x1080, igual ao design.
    """
    stack = window.findChild(type(window).__mro__[0], "stack")
    if stack is None:
        # findChild com tipo genérico
        from PySide6.QtWidgets import QStackedWidget
        stack = window.findChild(QStackedWidget, "stack")
    if stack is None:
        return
 
    from PySide6.QtWidgets import QWidget
    for i in range(stack.count()):
        page = stack.widget(i)
        for child in page.findChildren(QWidget):
            name = child.objectName()
            if name.startswith("fundo_"):
                child.setGeometry(0, 0, 1920, 1080)
                break  # só um fundo por página
 
 
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
 
    _corrigir_fundos(window)
 
    return window
 
 
def aplicar_icone(window, base_dir: Path):
 
    icone = base_dir / "images" / "icone.png"
 
    if icone.exists():
        window.setWindowIcon(QIcon(str(icone)))