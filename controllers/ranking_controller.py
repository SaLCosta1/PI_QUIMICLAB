# =========================================================
# ranking_controller.py
# =========================================================

from PySide6.QtWidgets import (
    QPushButton,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QWidget,
)

from PySide6.QtCore import Qt

from data.rankings import (
    ranking_alunos,
    ranking_turmas,
)


class RankingController:

    def __init__(self, main):

        self.main = main
        self.window = main.window

        self.setup()  # <- estava faltando

    # =====================================================
    # SETUP
    # =====================================================

    def setup(self):

        self._setup_ranking_geral()
        self._setup_ranking_turmas()
        self._setup_tabelas()

    # =====================================================
    # TELAS
    # =====================================================

    def _setup_ranking_geral(self):

        w = self.window

        w.btn_voltarpararanking.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

        w.btn_voltarpararanking2.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

    def _setup_ranking_turmas(self):

        w = self.window

        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: self.main.ir_para(w.pg_ranking)
        )

    # =====================================================
    # CONFIGURAÇÃO DAS TABELAS
    # =====================================================

    def _setup_tabelas(self):

        w = self.window

        # ==========================================
        # TABELA ALUNOS
        # ==========================================

        tabela_a = w.tabela_rankingalunos

        tabela_a.setColumnCount(4)

        headers = ["Posição", "Nome", "Acertos", "Pontos"]

        for col, titulo in enumerate(headers):

            item = tabela_a.horizontalHeaderItem(col)

            if item is None:
                item = QTableWidgetItem(titulo)
                tabela_a.setHorizontalHeaderItem(col, item)
            else:
                item.setText(titulo)

        self._config_tabela(tabela_a)

        self._criar_botoes_tabela(
            tabela_a,
            w.findChild(QWidget, "container_rankinggeral"),
            920, 830, 621,
        )

        # ==========================================
        # TABELA TURMAS
        # ==========================================

        tabela_t = w.tabela_rankingturmas

        tabela_t.setColumnCount(5)

        headers = ["Posição", "Turma", "Acertos", "Pontos", "Média"]

        for col, titulo in enumerate(headers):

            item = tabela_t.horizontalHeaderItem(col)

            if item is None:
                item = QTableWidgetItem(titulo)
                tabela_t.setHorizontalHeaderItem(col, item)
            else:
                item.setText(titulo)

        self._config_tabela(tabela_t)

        self._criar_botoes_tabela(
            tabela_t,
            w.findChild(QWidget, "container_rankingturmas"),
            390, 820, 1041,
        )

        self._preencher_tabela_alunos()
        self._preencher_tabela_turmas()

    # =====================================================
    # CONFIG TABELA
    # =====================================================

    def _config_tabela(self, tabela):

        tabela.setAlternatingRowColors(True)

        tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        tabela.setShowGrid(True)

        tabela.verticalHeader().setVisible(False)

        tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        tabela.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

    # =====================================================
    # BOTÕES
    # =====================================================

    def _criar_botoes_tabela(self, tabela, container, x, y, largura):

        if container is None:
            return

        STYLE = """
        QPushButton {
            background-color: #921913;
            color: white;
            border-radius: 10px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #b52a22;
        }
        """

        btn_linha = QPushButton("+ Linha", container)
        btn_linha.setGeometry(x, y, largura // 2 - 5, 40)
        btn_linha.setStyleSheet(STYLE)
        btn_linha.clicked.connect(lambda: self._adicionar_linha(tabela))
        btn_linha.show()

        btn_col = QPushButton("+ Coluna", container)
        btn_col.setGeometry(x + largura // 2 + 5, y, largura // 2 - 5, 40)
        btn_col.setStyleSheet(STYLE)
        btn_col.clicked.connect(lambda: self._adicionar_coluna(tabela))
        btn_col.show()

    # =====================================================
    # ADICIONAR LINHA
    # =====================================================

    def _adicionar_linha(self, tabela):

        tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
        )

        row = tabela.rowCount()
        tabela.insertRow(row)

        for col in range(tabela.columnCount()):
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabela.setItem(row, col, item)

    # =====================================================
    # ADICIONAR COLUNA
    # =====================================================

    def _adicionar_coluna(self, tabela):

        tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
        )

        col = tabela.columnCount()
        tabela.insertColumn(col)
        tabela.setHorizontalHeaderItem(
            col, QTableWidgetItem(f"Campo {col + 1}")
        )

    # =====================================================
    # PREENCHER TABELAS
    # =====================================================

    def _preencher_tabela_alunos(self):

        tabela = self.window.tabela_rankingalunos
        tabela.setRowCount(len(ranking_alunos))

        for i, d in enumerate(ranking_alunos):

            valores = [str(i + 1), d["nome"], str(d["acertos"]), str(d["pontos"])]

            for col, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(i, col, item)

    def _preencher_tabela_turmas(self):

        tabela = self.window.tabela_rankingturmas
        tabela.setRowCount(len(ranking_turmas))

        for i, d in enumerate(ranking_turmas):

            valores = [
                str(i + 1), d["turma"],
                str(d["acertos"]), str(d["pontos"]), str(d["media"]),
            ]

            for col, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(i, col, item)
