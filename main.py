# =========================================================
# main.py  —  QuimicLab
# Ponto de entrada: carrega o .ui, instancia todos os
# controllers e abre a janela.
# =========================================================
import sys
from pathlib import Path
 
from PySide6.QtWidgets import QApplication
 
from utils.ui_loader import carregar_ui, aplicar_icone
from utils.scaler import aplicar_escala
from controllers.navigation_controller import NavigationController
from controllers.auth_controller import AuthController
from controllers.question_controller import QuestionController
from controllers.professor_controller import ProfessorController
from controllers.ranking_controller import RankingController
 
 
class Main:
    def __init__(self, window):
        self.window = window
        self.stack = window.stack
        self.usuario_logado: dict | None = None   # preenchido pelo AuthController
 
        # ---- Controllers (ordem importa: navigation primeiro) ----
        self.navigation         = NavigationController(self)
        self.ir_para            = self.navigation.ir_para   # atalho global
 
        self.auth_controller    = AuthController(self)
        self.question_controller = QuestionController(self)
        self.professor_controller = ProfessorController(self)
        self.ranking_controller = RankingController(self)
 
        # ---- Botão jogar na tela de início ----
        window.btn_jogar.clicked.connect(lambda: self.ir_para(window.pg_perfil))
 
        # ---- Tela inicial ----
        self.ir_para(window.pg_inicio)
 
 
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
 
    base_dir = Path(__file__).parent
    window   = carregar_ui(base_dir)
    aplicar_icone(window, base_dir)
 
    controller = Main(window)
 
    aplicar_escala(app, window)
    window.showMaximized()
    sys.exit(app.exec())
