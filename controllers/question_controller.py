# =========================================================
# question_controller.py
# =========================================================

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QLineEdit


class QuestionController:

    def __init__(self, main):
        self.main = main
        self.window = main.window

        self.tempo = 120
        self.dica_visivel = False
        self.ajuda_usada = False

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick_timer)

        self.setup()

    # =====================================================
    # SETUP
    # =====================================================

    def setup(self):

        w = self.window

        # Telas de questão (jogo)
        telas = [
            (
                w.txt_dica,
                w.btn_altA, w.btn_altB, w.btn_altC, w.btn_altD,
                w.lbl_timer,
                w.btn_dicaexp,
                w.btn_eliminar,
            ),
        ]

        for (txt_dica, altA, altB, altC, altD, lbl_timer, btn_dica, btn_elim) in telas:

            txt_dica.hide()

            btn_dica.clicked.connect(
                lambda checked=False, td=txt_dica: self.toggle_dica(td)
            )

            btn_elim.clicked.connect(
                lambda checked=False, a=altA, d=altD: self.eliminar_alternativas(a, d)
            )

            for alt in (altA, altB, altC, altD):
                alt.clicked.connect(self.responder)

        # Feedback
        w.btn_gabarito.clicked.connect(
            lambda: self.main.ir_para(w.pg_gabarito)
        )

        # Gabarito
        w.btn_voltarmodos3.clicked.connect(
            lambda: self.main.ir_para(w.pg_modos)
        )

        # Editar pergunta detalhe
        w.btn_excluir.clicked.connect(self._confirmar_exclusao)
        w.btn_confirmar_exclusao.clicked.connect(self._executar_exclusao)
        w.btn_negar_exclusao.clicked.connect(self._cancelar_exclusao)
        w.btn_editar.clicked.connect(
            lambda: self.main.ir_para(w.pg_questao_edicao)
        )

        # Esconde confirmação de exclusão inicialmente
        w.btn_confirmar_exclusao.hide()
        w.btn_negar_exclusao.hide()
        w.lbl_alt1_editarpergunta_3.hide()

        # Questão edição
        w.btn_confirmaredicao.clicked.connect(self._confirmar_edicao)

        # Questão adição
        w.btn_confirmaradicao.clicked.connect(self._confirmar_adicao)


    # =====================================================
    # ABRIR QUESTÃO
    # =====================================================

    def abrir_questao(self, pagina, txt_dica, altA, altB, altC, altD, lbl_timer):

        self.timer.stop()

        self.tempo = 120
        self.dica_visivel = False
        self.ajuda_usada = False

        lbl_timer.setText(str(self.tempo))
        txt_dica.hide()

        for alt in (altA, altB, altC, altD):
            alt.show()
            alt.setEnabled(True)

        self._lbl_timer_ativo = lbl_timer
        self.timer.start(1000)
        self.main.ir_para(pagina)

    # =====================================================
    # TIMER
    # =====================================================

    def _tick_timer(self):

        self.tempo -= 1
        self._lbl_timer_ativo.setText(str(self.tempo))

        if self.tempo <= 0:
            self.timer.stop()
            QMessageBox.information(self.window, "Tempo esgotado", "O tempo acabou!")
            self.main.ir_para(self.window.pg_feedback)

    # =====================================================
    # DICA
    # =====================================================

    def toggle_dica(self, txt_dica):
        self.dica_visivel = not self.dica_visivel
        txt_dica.setVisible(self.dica_visivel)

    # =====================================================
    # ELIMINAR
    # =====================================================

    def eliminar_alternativas(self, altA, altD):
        if self.ajuda_usada:
            return
        altA.hide()
        altD.hide()
        self.ajuda_usada = True

    # =====================================================
    # RESPONDER
    # =====================================================

    def responder(self):
        self.timer.stop()
        self.main.ir_para(self.window.pg_feedback)

    # =====================================================
    # CONFIRMAR EXCLUSÃO
    # =====================================================

    def _confirmar_exclusao(self):
        w = self.window
        w.lbl_alt1_editarpergunta_3.show()
        w.btn_confirmar_exclusao.show()
        w.btn_negar_exclusao.show()

    def _executar_exclusao(self):
        w = self.window
        w.lbl_alt1_editarpergunta_3.hide()
        w.btn_confirmar_exclusao.hide()
        w.btn_negar_exclusao.hide()
        QMessageBox.information(w, "Excluído", "Pergunta excluída com sucesso!")
        self.main.ir_para(w.pg_editarperguntas)

    def _cancelar_exclusao(self):
        w = self.window
        w.lbl_alt1_editarpergunta_3.hide()
        w.btn_confirmar_exclusao.hide()
        w.btn_negar_exclusao.hide()

    # =====================================================
    # CONFIRMAR EDIÇÃO
    # =====================================================

    def _confirmar_edicao(self):
        QMessageBox.information(
            self.window,
            "Sucesso",
            "Pergunta editada com sucesso!"
        )
        self.main.ir_para(self.window.pg_editarperguntas)

    # =====================================================
    # CONFIRMAR ADIÇÃO
    # =====================================================

    def _confirmar_adicao(self):
        QMessageBox.information(
            self.window,
            "Sucesso",
            "Pergunta adicionada com sucesso!"
        )
        self.main.ir_para(self.window.pg_editarperguntas)
