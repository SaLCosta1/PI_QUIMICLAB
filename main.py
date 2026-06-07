import sys
from pathlib import Path

import PySide6
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from app.utils.ui_loader import carregar_ui, aplicar_icone
from app.utils.scaler import aplicar_escala

from app.controllers.navigation_controller import NavigationController
from app.controllers.auth_controller import AuthController
from app.controllers.question_controller import QuestionController
from app.controllers.professor_controller import ProfessorController
from app.controllers.ranking_controller import RankingController
from app.controllers.animation_controller import AnimationController
from app.controllers.editor_controller import EditorController


class Main:
    """Centro do sistema: guarda a janela, o estado global e cria os controllers."""

    def __init__(self, window):
        self.window = window
        self.stack = window.stack
        self.usuario_logado: dict | None = None

        # NavigationController vem primeiro: os outros usam self.ir_para().
        self.navigation = NavigationController(self)
        self.ir_para = self.navigation.ir_para

        self.auth_controller = AuthController(self)
        self.question_controller = QuestionController(self)
        self.professor_controller = ProfessorController(self)
        self.ranking_controller = RankingController(self)
        self.editor_controller = EditorController(self)
        # AnimationController por último: ele varre todos os botões já criados.
        self.animation_controller = AnimationController(self)

        self.ir_para(window.pg_inicio)


if __name__ == "__main__":
    # Aponta o Qt para os plugins do próprio PySide6 (evita paths locais quebrados).
    plugin_dir = Path(PySide6.__file__).resolve().parent / "plugins"
    if plugin_dir.exists():
        QCoreApplication.setLibraryPaths([str(plugin_dir)])

    app = QApplication(sys.argv)
    base_dir = Path(__file__).resolve().parent

    window = carregar_ui(base_dir)
    aplicar_icone(window, base_dir)
    controller = Main(window)
    aplicar_escala(app, window)
    window.showMaximized()
    sys.exit(app.exec())
