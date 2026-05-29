# -*- coding: utf-8 -*-
# =========================================================
# EDITOR CONTROLLER
# =========================================================
#
# Responsável por transformar as telas:
# • pg_questao_edicao
# • pg_questao_adicionar
#
# em telas totalmente editáveis.
#
# Funcionalidades:
# • edição de pergunta
# • edição de alternativas
# • edição de dica
# • edição de nível
# • troca de imagem da questão
#
# O controller substitui os widgets visuais originais
# por campos de entrada (QLineEdit), permitindo
# edição dinâmica diretamente pela interface.
# =========================================================

from PySide6.QtWidgets import (
    QLineEdit,
    QFileDialog,
    QLabel,
    QPushButton
)

from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt


class EditorController:

    # =====================================================
    # CONSTRUTOR
    # =====================================================
    #
    # Recebe a instância principal da aplicação
    # e inicia a configuração das telas editáveis.
    # =====================================================

    def __init__(self, main):

        self.main = main
        self.window = main.window

        self.setup()

    # =====================================================
    # SETUP GERAL
    # =====================================================
    #
    # Inicializa:
    # • tela de edição
    # • tela de adição
    # =====================================================

    def setup(self):

        self._setup_edicao()
        self._setup_adicao()

    # =====================================================
    # CONFIGURAÇÃO DA TELA DE EDIÇÃO
    # =====================================================
    #
    # Cria campos editáveis sobre os widgets
    # da tela de edição de questões.
    #
    # Os widgets originais são ocultados
    # após a criação dos campos.
    # =====================================================

    def _setup_edicao(self):

        w = self.window

        # Container principal da questão
        container = w.container_questao_2

        # =================================================
        # CAMPOS EDITÁVEIS
        # =================================================

        self._pergunta_2 = self._criar_edit(
            w.lbl_pergunta_2,
            container
        )

        self._nivel_2 = self._criar_edit(
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

        # =================================================
        # BOTÃO DE TROCA DE IMAGEM
        # =================================================

        self._btn_img_2 = self._criar_btn_imagem(
            w.lbl_imagem_2,
            container,
            sufixo="_2"
        )

        # =================================================
        # OCULTA OS WIDGETS ORIGINAIS
        # =================================================
        #
        # Os widgets originais permanecem na tela,
        # porém escondidos.
        #
        # Os novos campos editáveis ocupam o lugar deles.
        # =================================================

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

    # =====================================================
    # CONFIGURAÇÃO DA TELA DE ADIÇÃO
    # =====================================================
    #
    # Cria campos vazios para inserção de
    # novas questões no sistema.
    # =====================================================

    def _setup_adicao(self):

        w = self.window

        # Container principal da questão
        container = w.container_questao_3

        # =================================================
        # CAMPOS EDITÁVEIS
        # =================================================

        self._pergunta_3 = self._criar_edit(
            w.lbl_pergunta_3,
            container
        )

        self._nivel_3 = self._criar_edit(
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

        # =================================================
        # BOTÃO DE TROCA DE IMAGEM
        # =================================================

        self._btn_img_3 = self._criar_btn_imagem(
            w.lbl_imagem_3,
            container,
            sufixo="_3"
        )

        # =================================================
        # PLACEHOLDERS
        # =================================================
        #
        # Textos auxiliares exibidos nos campos
        # antes do preenchimento pelo usuário.
        # =================================================

        self._pergunta_3.setPlaceholderText(
            "Digite a pergunta..."
        )

        self._nivel_3.setPlaceholderText(
            "Ex: Fácil"
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

        # =================================================
        # OCULTA WIDGETS ORIGINAIS
        # =================================================

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

    # =====================================================
    # CRIAR CAMPO EDITÁVEL
    # =====================================================
    #
    # Cria um QLineEdit exatamente na posição
    # e tamanho do widget original.
    #
    # Também copia o texto original do widget.
    # =====================================================

    def _criar_edit(self, widget_ref, parent):

        edit = QLineEdit(parent)

        # Copia posição e tamanho
        edit.setGeometry(
            widget_ref.geometry()
        )

        # =================================================
        # COPIA TEXTO ORIGINAL
        # =================================================

        if hasattr(widget_ref, 'text'):

            edit.setText(
                widget_ref.text()
            )

        # =================================================
        # ESTILO VISUAL DO CAMPO
        # =================================================

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

    # =====================================================
    # CRIAR BOTÃO DE IMAGEM
    # =====================================================
    #
    # Cria um botão clicável sobre o label da imagem,
    # permitindo selecionar uma nova imagem
    # para a questão.
    # =====================================================

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

        # Usa a mesma posição do label original
        btn.setGeometry(
            lbl_imagem.geometry()
        )

        # =================================================
        # ESTILO VISUAL DO BOTÃO
        # =================================================

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

        # =================================================
        # EVENTO DE CLIQUE
        # =================================================

        btn.clicked.connect(
            lambda: self._escolher_imagem(
                lbl_imagem,
                btn
            )
        )

        btn.show()

        return btn

    # =====================================================
    # ESCOLHER IMAGEM
    # =====================================================
    #
    # Abre o explorador de arquivos para que
    # o usuário selecione uma imagem.
    #
    # Após seleção:
    # • a imagem é carregada
    # • redimensionada
    # • aplicada no QLabel correspondente
    # =====================================================

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

        # Usuário cancelou seleção
        if not caminho:
            return

        # =================================================
        # CARREGA IMAGEM
        # =================================================

        pix = QPixmap(caminho)

        # =================================================
        # REDIMENSIONA IMAGEM
        # =================================================

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
    # COLETAR DADOS DA EDIÇÃO
    # =====================================================
    #
    # Retorna os dados preenchidos na tela
    # de edição em formato de dicionário.
    # =====================================================

    def coletar_edicao(self):

        return {

            "pergunta": self._pergunta_2.text(),

            "nivel": self._nivel_2.text(),

            "dica": self._dica_2.text(),

            "altA": self._altA_2.text(),

            "altB": self._altB_2.text(),

            "altC": self._altC_2.text(),

            "altD": self._altD_2.text(),
        }

    # =====================================================
    # COLETAR DADOS DA ADIÇÃO
    # =====================================================
    #
    # Retorna os dados preenchidos na tela
    # de criação de nova questão.
    # =====================================================

    def coletar_adicao(self):

        return {

            "pergunta": self._pergunta_3.text(),

            "nivel": self._nivel_3.text(),

            "dica": self._dica_3.text(),

            "altA": self._altA_3.text(),

            "altB": self._altB_3.text(),

            "altC": self._altC_3.text(),

            "altD": self._altD_3.text(),
        }