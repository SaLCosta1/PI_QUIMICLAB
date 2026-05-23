# =========================================================
# main.py
# =========================================================
 
import sys
from pathlib import Path
 
from PySide6.QtWidgets import QApplication
 
from utils.ui_loader import carregar_ui, aplicar_icone
from utils.scaler import aplicar_escala
 
from controllers.navigation_controller import NavigationController
from controllers.animation_controller import AnimationController
from controllers.auth_controller import AuthController
from controllers.question_controller import QuestionController
from controllers.professor_controller import ProfessorController
from controllers.ranking_controller import RankingController
from controllers.editor_controller import EditorController
 
 
class Main:
 
    def __init__(self, window):
 
        self.window = window
        self.stack = window.stack
        self.usuario_logado = None
 
        self.navigation = NavigationController(self)
        self.ir_para = self.navigation.ir_para
 
        self.animation_controller = AnimationController(self)
        self.auth_controller      = AuthController(self)
        self.question_controller  = QuestionController(self)
        self.professor_controller = ProfessorController(self)
        self.ranking_controller   = RankingController(self)
        self.editor_controller    = EditorController(self)
 
        self.setup_inicio()
        self._aplicar_icones()
 
        self.ir_para(self.window.pg_inicio)
 
    # =====================================================
    # ÍCONES
    # =====================================================
 
    def _aplicar_icones(self):
 
        from PySide6.QtGui import QIcon, QPixmap
        from PySide6.QtWidgets import QPushButton, QLabel
        from PySide6.QtCore import Qt, QSize
 
        w = self.window
        base = Path(__file__).parent / "images"
 
        botoes = {
            "btn_dicaexp":    ("icone dica.png",  QSize(500, 500)),
            "btn_eliminar":   ("icone lixo.png",  QSize(700, 700)),
        }
 
        for nome, (arquivo, tamanho) in botoes.items():
            widget = getattr(w, nome, None)
            if widget is None:
                continue
            widget.setIcon(QIcon(str(base / arquivo)))
            widget.setIconSize(tamanho)
 
        labels = {
            "img_relogio_questao": "icone relogio.png",
        }
 
        for nome, arquivo in labels.items():
            widget = getattr(w, nome, None)
            if widget is None:
                continue
            pix = QPixmap(str(base / arquivo))
            widget.setPixmap(
                pix.scaled(
                    widget.width(), widget.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
 
    # =====================================================
    # INÍCIO
    # =====================================================
 
    def setup_inicio(self):
 
        w = self.window
 
        w.btn_jogar.clicked.connect(lambda: self.ir_para(w.pg_perfil))
        w.btn_comojogar.clicked.connect(lambda: self.ir_para(w.pg_comojogar))
        w.btn_voltarinicio.clicked.connect(lambda: self.ir_para(w.pg_inicio))
        w.btn_soualuno.clicked.connect(lambda: self.ir_para(w.pg_loginaluno))
        w.btn_souprof.clicked.connect(lambda: self.ir_para(w.pg_loginprof))
        w.btn_voltarperfil.clicked.connect(lambda: self.ir_para(w.pg_perfil))
        w.btn_voltarperfil4.clicked.connect(lambda: self.ir_para(w.pg_perfil))
 
        # Modos — todos usam pg_questao
        for btn in (w.btn_facil, w.btn_medio, w.btn_dificil, w.btn_shuffle):
            btn.clicked.connect(
                lambda: self.question_controller.abrir_questao(
                    w.pg_questao,
                    w.txt_dica,
                    w.btn_altA, w.btn_altB, w.btn_altC, w.btn_altD,
                    w.lbl_timer,
                )
            )
 
 
# =========================================================
# EXECUÇÃO
# =========================================================
 
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    base_dir = Path(__file__).parent
 
    window = carregar_ui(base_dir)
    aplicar_icone(window, base_dir)
 
    controller = Main(window)
 
    aplicar_escala(app, window)
    window.showMaximized()
    sys.exit(app.exec())