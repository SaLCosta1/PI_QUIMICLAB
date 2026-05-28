# =========================================================
# editor_controller.py
# Torna pg_questao_edicao e pg_questao_adicionar editáveis
# Campos editáveis: pergunta, nível, dica, alternativas, imagem
# =========================================================

from PySide6.QtWidgets import (
    QLineEdit, QFileDialog, QLabel, QPushButton
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class EditorController:

    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.setup()

    # =====================================================
    # SETUP
    # =====================================================

    def setup(self):
        self._setup_edicao()
        self._setup_adicao()

    # =====================================================
    # EDIÇÃO
    # =====================================================

    def _setup_edicao(self):
        w = self.window
        container = w.container_questao_2  # <- parent correto

        self._pergunta_2 = self._criar_edit(w.lbl_pergunta_2,  container)
        self._nivel_2    = self._criar_edit(w.lbl_infonivel_2, container)
        self._dica_2     = self._criar_edit(w.txt_dica_2,      container)
        self._altA_2     = self._criar_edit(w.btn_altA_2,      container)
        self._altB_2     = self._criar_edit(w.btn_altB_2,      container)
        self._altC_2     = self._criar_edit(w.btn_altC_2,      container)
        self._altD_2     = self._criar_edit(w.btn_altD_2,      container)

        self._btn_img_2 = self._criar_btn_imagem(w.lbl_imagem_2, container, sufixo="_2")

        for widget in (
            w.lbl_pergunta_2, w.lbl_infonivel_2, w.txt_dica_2,
            w.btn_altA_2, w.btn_altB_2, w.btn_altC_2, w.btn_altD_2,
            w.btn_dicaexp_2, w.btn_eliminar_2,
            w.lbl_timer_2, w.img_relogio_questao_2,
        ):
            widget.hide()

    # =====================================================
    # ADIÇÃO
    # =====================================================

    def _setup_adicao(self):
        w = self.window
        container = w.container_questao_3  # <- parent correto

        self._pergunta_3 = self._criar_edit(w.lbl_pergunta_3,  container)
        self._nivel_3    = self._criar_edit(w.lbl_infonivel_3, container)
        self._dica_3     = self._criar_edit(w.txt_dica_3,      container)
        self._altA_3     = self._criar_edit(w.btn_altA_3,      container)
        self._altB_3     = self._criar_edit(w.btn_altB_3,      container)
        self._altC_3     = self._criar_edit(w.btn_altC_3,      container)
        self._altD_3     = self._criar_edit(w.btn_altD_3,      container)

        self._btn_img_3 = self._criar_btn_imagem(w.lbl_imagem_3, container, sufixo="_3")

        self._pergunta_3.setPlaceholderText("Digite a pergunta...")
        self._nivel_3.setPlaceholderText("Ex: Fácil")
        self._dica_3.setPlaceholderText("Digite a dica...")
        self._altA_3.setPlaceholderText("Alternativa A")
        self._altB_3.setPlaceholderText("Alternativa B")
        self._altC_3.setPlaceholderText("Alternativa C")
        self._altD_3.setPlaceholderText("Alternativa D")

        for widget in (
            w.lbl_pergunta_3, w.lbl_infonivel_3, w.txt_dica_3,
            w.btn_altA_3, w.btn_altB_3, w.btn_altC_3, w.btn_altD_3,
            w.btn_dicaexp_3, w.btn_eliminar_3,
            w.lbl_timer_3, w.img_relogio_questao_3,
        ):
            widget.hide()
    # =====================================================
    # HELPERS
    # =====================================================

    def _criar_edit(self, widget_ref, parent):
        """Cria um QLineEdit no mesmo lugar e tamanho do widget original."""

        edit = QLineEdit(parent)
        edit.setGeometry(widget_ref.geometry())

        # Copia texto do widget original
        if hasattr(widget_ref, 'text'):
            edit.setText(widget_ref.text())

        edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #921913;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #1a1a1a;
            }
            QLineEdit:focus {
                border: 2px solid #b52a22;
            }
        """)

        edit.show()
        return edit

    def _criar_btn_imagem(self, lbl_imagem, parent, sufixo=""):
        """Cria um botão clicável sobre o label de imagem para trocar a imagem."""

        btn = QPushButton("📷 Trocar imagem", parent)
        btn.setGeometry(lbl_imagem.geometry())
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(146, 25, 19, 180);
                color: white;
                border-radius: 10px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: rgba(181, 42, 34, 220);
            }
        """)

        btn.clicked.connect(
            lambda: self._escolher_imagem(lbl_imagem, btn)
        )

        btn.show()
        return btn

    def _escolher_imagem(self, lbl_imagem, btn):
        """Abre o seletor de arquivo e aplica a imagem no label."""

        caminho, _ = QFileDialog.getOpenFileName(
            self.window,
            "Escolher imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if not caminho:
            return

        pix = QPixmap(caminho)

        lbl_imagem.setPixmap(
            pix.scaled(
                lbl_imagem.width(),
                lbl_imagem.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        lbl_imagem.show()

    # =====================================================
    # COLETAR DADOS (chamado pelo question_controller ao confirmar)
    # =====================================================

    def coletar_edicao(self):
        return {
            "pergunta":  self._pergunta_2.text(),
            "nivel":     self._nivel_2.text(),
            "dica":      self._dica_2.text(),
            "altA":      self._altA_2.text(),
            "altB":      self._altB_2.text(),
            "altC":      self._altC_2.text(),
            "altD":      self._altD_2.text(),
        }

    def coletar_adicao(self):
        return {
            "pergunta":  self._pergunta_3.text(),
            "nivel":     self._nivel_3.text(),
            "dica":      self._dica_3.text(),
            "altA":      self._altA_3.text(),
            "altB":      self._altB_3.text(),
            "altC":      self._altC_3.text(),
            "altD":      self._altD_3.text(),
        }
