import base64
import mimetypes
from pathlib import Path

from PySide6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QFileDialog,
    QLabel,
    QPushButton
)

from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt

class EditorController:
    def __init__(self, main):
        self.main = main
        self.window = main.window
        self._imagem_base64_2 = None
        self._imagem_mime_2 = None
        self._imagem_base64_3 = None
        self._imagem_mime_3 = None
        self._alt_correta_2 = "A"
        self._alt_correta_3 = "A"
        self.setup()

    def setup(self):
        self._setup_edicao()
        self._setup_adicao()

    def _setup_edicao(self):
        w = self.window
        container = w.container_questao_2
        self._pergunta_2 = self._criar_edit(
            w.lbl_pergunta_2,
            container
        )
        self._nivel_2 = self._criar_combobox(
            w.lbl_infonivel_2,
            container
        )
        self._dica_2 = self._criar_edit(
            w.txt_dica_2,
            container
        )
        self._altA_2 = self._criar_edit(
            w.btn_altA_2,
            container
        )
        self._altB_2 = self._criar_edit(
            w.btn_altB_2,
            container
        )
        self._altC_2 = self._criar_edit(
            w.btn_altC_2,
            container
        )
        self._altD_2 = self._criar_edit(
            w.btn_altD_2,
            container
        )
        self._btn_img_2 = self._criar_btn_imagem(
            w.lbl_imagem_2,
            container,
            sufixo="_2"
        )
        self._marcadores_2 = self._criar_marcadores_corretas(
            [(self._altA_2, "A"), (self._altB_2, "B"),
             (self._altC_2, "C"), (self._altD_2, "D")],
            container,
            self._marcar_alt_correta_edicao,
        )
        self._atualizar_visual_alt_correta_edicao()
        for widget in (
            w.lbl_pergunta_2,
            w.lbl_infonivel_2,
            w.txt_dica_2,
            w.btn_altA_2,
            w.btn_altB_2,
            w.btn_altC_2,
            w.btn_altD_2,
            w.btn_dicaexp_2,
            w.btn_eliminar_2,
            w.lbl_timer_2,
            w.img_relogio_questao_2,
        ):
            widget.hide()

    def _setup_adicao(self):
        w = self.window
        container = w.container_questao_3
        self._pergunta_3 = self._criar_edit(
            w.lbl_pergunta_3,
            container
        )
        self._nivel_3 = self._criar_combobox(
            w.lbl_infonivel_3,
            container
        )
        self._dica_3 = self._criar_edit(
            w.txt_dica_3,
            container
        )
        self._altA_3 = self._criar_edit(
            w.btn_altA_3,
            container
        )
        self._altB_3 = self._criar_edit(
            w.btn_altB_3,
            container
        )
        self._altC_3 = self._criar_edit(
            w.btn_altC_3,
            container
        )
        self._altD_3 = self._criar_edit(
            w.btn_altD_3,
            container
        )
        self._btn_img_3 = self._criar_btn_imagem(
            w.lbl_imagem_3,
            container,
            sufixo="_3"
        )
        self._pergunta_3.setPlaceholderText(
            "Digite a pergunta..."
        )
        self._dica_3.setPlaceholderText(
            "Digite a dica..."
        )
        self._altA_3.setPlaceholderText(
            "Alternativa A"
        )
        self._altB_3.setPlaceholderText(
            "Alternativa B"
        )
        self._altC_3.setPlaceholderText(
            "Alternativa C"
        )
        self._altD_3.setPlaceholderText(
            "Alternativa D"
        )
        self._marcadores_3 = self._criar_marcadores_corretas(
            [(self._altA_3, "A"), (self._altB_3, "B"),
             (self._altC_3, "C"), (self._altD_3, "D")],
            container,
            self._marcar_alt_correta_adicao,
        )
        self._marcar_alt_correta_adicao("A")
        for widget in (
            w.lbl_pergunta_3,
            w.lbl_infonivel_3,
            w.txt_dica_3,
            w.btn_altA_3,
            w.btn_altB_3,
            w.btn_altC_3,
            w.btn_altD_3,
            w.btn_dicaexp_3,
            w.btn_eliminar_3,
            w.lbl_timer_3,
            w.img_relogio_questao_3,
        ):
            widget.hide()

    def _criar_edit(self, widget_ref, parent):
        edit = QLineEdit(parent)
        edit.setGeometry(
            widget_ref.geometry()
        )
        if hasattr(widget_ref, 'text'):
            edit.setText(
                widget_ref.text()
            )
        edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #921913;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #333333;
            }

            QLineEdit:focus {
                border: 2px solid #d43a31;
            }
        """)
        edit.show()
        return edit

    def _criar_combobox(self, widget_ref, parent):
        combo = QComboBox(parent)
        combo.setGeometry(
            widget_ref.geometry()
        )
        combo.addItems(["Fácil", "Médio", "Difícil"])
        combo.setStyleSheet("""
            QComboBox {
                background-color: #f5f5f5;
                border: 2px solid #921913;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: white;
            }

            QComboBox:focus {
                border: 2px solid #d43a31;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox::down-arrow {
                image: none;
            }
        """)
        combo.show()
        return combo

    def _criar_btn_imagem(
        self,
        lbl_imagem,
        parent,
        sufixo=""
    ):
        btn = QPushButton(
            "📷 Trocar imagem",
            parent
        )
        btn.setGeometry(
            lbl_imagem.geometry()
        )
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
            lambda: self._escolher_imagem(
                lbl_imagem,
                btn
            )
        )
        btn.show()
        return btn

    def _escolher_imagem(
        self,
        lbl_imagem,
        btn
    ):
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
        try:
            with open(caminho, 'rb') as f:
                imagem_bytes = f.read()
                imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
            imagem_mime, _ = mimetypes.guess_type(caminho)
            if not imagem_mime:
                imagem_mime = "image/png"
            if hasattr(lbl_imagem, 'objectName') and '_2' in lbl_imagem.objectName():
                self._imagem_base64_2 = imagem_base64
                self._imagem_mime_2 = imagem_mime
            else:
                self._imagem_base64_3 = imagem_base64
                self._imagem_mime_3 = imagem_mime
        except Exception as e:
            print(f"Erro ao converter imagem para base64: {e}")

    def _carregar_imagem_base64(self, imagem_base64, sufixo):
        """Carrega uma imagem em base64 e exibe no label correspondente."""
        try:
            imagem_bytes = base64.b64decode(imagem_base64)
            pix = QPixmap()
            pix.loadFromData(imagem_bytes)
            if sufixo == '_2':
                lbl_imagem = self.window.lbl_imagem_2
            else:
                lbl_imagem = self.window.lbl_imagem_3
            lbl_imagem.setPixmap(
                pix.scaled(
                    lbl_imagem.width(),
                    lbl_imagem.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            lbl_imagem.show()
        except Exception as e:
            print(f"Erro ao carregar imagem base64: {e}")

    def _converter_nivel_para_id(self, nivel_nome):
        """Converte nome do nível para ID numérico."""
        mapa = {"Fácil": 1, "Médio": 2, "Difícil": 3}
        return mapa.get(nivel_nome, 1)

    def coletar_edicao(self):
        nivel_nome = self._nivel_2.currentText()
        nivel_id = self._converter_nivel_para_id(nivel_nome)
        return {
            "pergunta": self._pergunta_2.text(),
            "nivel": nivel_id,
            "dica": self._dica_2.text(),
            "altA": self._altA_2.text(),
            "altB": self._altB_2.text(),
            "altC": self._altC_2.text(),
            "altD": self._altD_2.text(),
            "alt_correta": self._alt_correta_2,
            "imagem_base64": self._imagem_base64_2,
            "imagem_mime": self._imagem_mime_2,
        }

    def coletar_adicao(self):
        nivel_nome = self._nivel_3.currentText()
        return {
            "pergunta": self._pergunta_3.text(),
            "nivel": nivel_nome,
            "dica": self._dica_3.text(),
            "altA": self._altA_3.text(),
            "altB": self._altB_3.text(),
            "altC": self._altC_3.text(),
            "altD": self._altD_3.text(),
            "alt_correta": self._alt_correta_3,
            "imagem_base64": self._imagem_base64_3,
            "imagem_mime": self._imagem_mime_3,
        }

    def preencher_edicao(self, pergunta_dados):
        """Preenche os campos de edição com os dados da pergunta."""
        if not pergunta_dados:
            return
        self._pergunta_2.setText(pergunta_dados.get('enunciado', ''))
        nivel_map = {1: 'Fácil', 2: 'Médio', 3: 'Difícil'}
        nivel_nome = nivel_map.get(pergunta_dados.get('id_nivel'), 'Fácil')
        self._nivel_2.setCurrentText(nivel_nome)
        alternativas = pergunta_dados.get('alternativas', [])
        letras = ['A', 'B', 'C', 'D']
        for i, alt in enumerate(alternativas):
            texto = alt.get('texto', '')
            correta = alt.get('correta', 0)
            if i == 0:
                self._altA_2.setText(texto)
            elif i == 1:
                self._altB_2.setText(texto)
            elif i == 2:
                self._altC_2.setText(texto)
            elif i == 3:
                self._altD_2.setText(texto)
            if correta in (1, True):
                self._alt_correta_2 = letras[i]
        dicas = pergunta_dados.get('dicas', [])
        if dicas:
            dica_texto = next((d for d in dicas if d.get('tipo') == 'texto'), None)
            if dica_texto:
                self._dica_2.setText(dica_texto.get('conteudo', ''))
            else:
                self._dica_2.setText('')
        else:
            self._dica_2.setText('')
        imagem_base64 = pergunta_dados.get('imagem_base64')
        if imagem_base64:
            self._imagem_base64_2 = imagem_base64
            self._imagem_mime_2 = pergunta_dados.get('imagem_mime')
            self._carregar_imagem_base64(imagem_base64, '_2')
        else:
            self._imagem_base64_2 = None
            self._imagem_mime_2 = None
        self._atualizar_visual_alt_correta_edicao()

    def limpar_campos_adicao(self):
        """Limpa todos os campos da tela de adição de pergunta."""
        self._pergunta_3.setText('')
        self._nivel_3.setCurrentIndex(0)
        self._dica_3.setText('')
        self._altA_3.setText('')
        self._altB_3.setText('')
        self._altC_3.setText('')
        self._altD_3.setText('')
        self._imagem_base64_3 = None
        self._imagem_mime_3 = None
        if hasattr(self.window, 'lbl_imagem_3'):
            self.window.lbl_imagem_3.setPixmap(QPixmap())
        self._marcar_alt_correta_adicao("A")

    def _criar_marcadores_corretas(self, alt_edits, parent, callback):
        """Cria um botão 'Correta' no canto direito de cada alternativa.

        Clicar marca aquela alternativa como a correta (fica verde). O campo de
        texto é encolhido para abrir espaço para o botão.
        """
        marcadores = {}
        larg_btn = 150
        for edit, letra in alt_edits:
            g = edit.geometry()
            edit.setGeometry(g.x(), g.y(), max(g.width() - larg_btn - 10, 50), g.height())
            btn = QPushButton("Correta", parent)
            btn.setGeometry(g.x() + g.width() - larg_btn, g.y(), larg_btn, g.height())
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _checked=False, l=letra: callback(l))
            btn.show()
            marcadores[letra] = btn
        return marcadores

    def _atualizar_marcadores(self, marcadores, letra_correta):
        """Reflete visualmente qual alternativa está marcada como correta."""
        ativo = """
            QPushButton { background-color: #4caf50; color: white;
                border: none; border-radius: 10px; font-size: 16px; font-weight: bold; }
        """
        inativo = """
            QPushButton { background-color: white; color: #921913;
                border: 2px solid #921913; border-radius: 10px; font-size: 16px; }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        for letra, btn in marcadores.items():
            sel = (letra == letra_correta)
            btn.setChecked(sel)
            btn.setText("✓ Correta" if sel else "Correta")
            btn.setStyleSheet(ativo if sel else inativo)

    def _marcar_alt_correta_edicao(self, letra):
        """Marca uma alternativa como correta na tela de edição."""
        self._alt_correta_2 = letra
        self._atualizar_visual_alt_correta_edicao()

    def _marcar_alt_correta_adicao(self, letra):
        """Marca uma alternativa como correta na tela de adição."""
        self._alt_correta_3 = letra
        self._atualizar_visual_alt_correta_adicao()

    def _atualizar_visual_alt_correta_edicao(self):
        """Atualiza visual dos botões de alternativa (edição)."""
        style_normal = """
            QLineEdit {
                background-color: white;
                border: 2px solid #921913;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #333333;
            }
        """
        style_correta = """
            QLineEdit {
                background-color: #e8f5e9;
                border: 3px solid #4caf50;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #1b5e20;
                font-weight: bold;
            }
        """
        for edit, letra in [
            (self._altA_2, "A"),
            (self._altB_2, "B"),
            (self._altC_2, "C"),
            (self._altD_2, "D"),
        ]:
            if letra == self._alt_correta_2:
                edit.setStyleSheet(style_correta)
            else:
                edit.setStyleSheet(style_normal)
        self._atualizar_marcadores(getattr(self, "_marcadores_2", {}), self._alt_correta_2)

    def _atualizar_visual_alt_correta_adicao(self):
        """Atualiza visual dos botões de alternativa (adição)."""
        style_normal = """
            QLineEdit {
                background-color: white;
                border: 2px solid #921913;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #333333;
            }
        """
        style_correta = """
            QLineEdit {
                background-color: #e8f5e9;
                border: 3px solid #4caf50;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 20px;
                color: #1b5e20;
                font-weight: bold;
            }
        """
        for edit, letra in [
            (self._altA_3, "A"),
            (self._altB_3, "B"),
            (self._altC_3, "C"),
            (self._altD_3, "D"),
        ]:
            if letra == self._alt_correta_3:
                edit.setStyleSheet(style_correta)
            else:
                edit.setStyleSheet(style_normal)
        self._atualizar_marcadores(getattr(self, "_marcadores_3", {}), self._alt_correta_3)
