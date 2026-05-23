# =========================================================
# professor_controller.py
# =========================================================

from PySide6.QtWidgets import QMessageBox


class ProfessorController:

    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.setup()

    def setup(self):

        w = self.window

        # =================================================
        # ÁREA PROFESSOR
        # =================================================

        w.btn_voltarloginprof.clicked.connect(
            lambda: self.main.ir_para(w.pg_loginprof)
        )
        w.btn_editarperguntas.clicked.connect(
            lambda: self.main.ir_para(w.pg_editarperguntas)
        )
        w.btn_relatoriogeral.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )
        w.btn_ranking.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

        # =================================================
        # PG_RANKING — tela intermediária
        # =================================================

        # Seção ranking
        w.btn_voltarareaprof2.clicked.connect(
            lambda: self.main.ir_para(w.pg_areaprof)
        )
        w.btn_rankingalunos_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_rankinggeral)
        )
        w.btn_rankingturmas_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_rankingturmas)
        )

        # Seção relatório
        w.btn_voltarareaprof2_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_areaprof)
        )
        w.btn_relatorioalunos.clicked.connect(
            lambda: self.main.ir_para(w.pg_relatoriogeral)
        )
        w.btn_relatorioturmas.clicked.connect(
            lambda: self.main.ir_para(w.pg_relatorioturmas)
        )

        # =================================================
        # EDITAR PERGUNTAS
        # =================================================

        w.btn_voltarareaprof.clicked.connect(
            lambda: self.main.ir_para(w.pg_areaprof)
        )
        w.btn_editarpergunta.clicked.connect(
            lambda: self.main.ir_para(w.pg_editarpergunta_detalhe)
        )
        w.btn_adicionarpergunta.clicked.connect(
            lambda: self.main.ir_para(w.pg_questao_adicionar)
        )

        # =================================================
        # EDITAR PERGUNTA DETALHE
        # =================================================

        w.btn_voltarpararanking_4.clicked.connect(
            lambda: self.main.ir_para(w.pg_editarperguntas)
        )

        # =================================================
        # QUESTÃO EDIÇÃO
        # =================================================

        w.btn_voltareditarperguntas.clicked.connect(
            lambda: self.main.ir_para(w.pg_editarperguntas)
        )

        # =================================================
        # QUESTÃO ADIÇÃO
        # =================================================

        w.btn_voltareditarperguntas_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_editarperguntas)
        )

        # =================================================
        # RANKING GERAL
        # =================================================

        w.btn_voltarpararanking2.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

        # =================================================
        # RANKING TURMAS
        # =================================================

        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

        # =================================================
        # RELATÓRIO INDIVIDUAL
        # =================================================

        w.btn_voltarpararanking_5.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

        # =================================================
        # RELATÓRIO GERAL
        # =================================================

        w.btn_voltarpararanking_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )
        w.btn_verificar.clicked.connect(
            lambda: self.main.ir_para(w.pg_relatorioindividual)
        )

        # =================================================
        # RELATÓRIO TURMAS
        # =================================================

        w.btn_voltarpararanking.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

    # =====================================================
    # FILTRO RELATÓRIO
    # =====================================================

    
