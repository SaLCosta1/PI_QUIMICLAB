from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

class RankingController:
    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.ir = main.ir_para
        self.setup()

    def setup(self):
        self._setup_navegacao()
        self._setup_rankinggeral()
        self._setup_rankingturmas()

    def _setup_navegacao(self):
        w = self.window
        ir = self.ir
        w.btn_rankingturmas_2.clicked.connect(
            lambda: ir(w.pg_rankingturmas)
        )
        w.btn_rankingalunos_2.clicked.connect(
            lambda: ir(w.pg_rankinggeral)
        )
        w.btn_voltarpararanking2.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )
        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

    def _setup_rankinggeral(self):
        w = self.window
        t = w.tbl_rankinggeral
        if hasattr(w, 'btn_voltarpararanking2_8'):
            w.btn_voltarpararanking2_8.clicked.connect(
                lambda: self._adicionar_coluna(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_9'):
            w.btn_voltarpararanking2_9.clicked.connect(
                lambda: self._remover_coluna(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_10'):
            w.btn_voltarpararanking2_10.clicked.connect(
                lambda: self._adicionar_linha(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_11'):
            w.btn_voltarpararanking2_11.clicked.connect(
                lambda: self._remover_linha(t)
            )

    def _setup_rankingturmas(self):
        w = self.window
        t = w.tabela_rankingturmas
        if hasattr(w, 'btn_voltarpararanking2_12'):
            w.btn_voltarpararanking2_12.clicked.connect(
                lambda: self._adicionar_coluna(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_13'):
            w.btn_voltarpararanking2_13.clicked.connect(
                lambda: self._remover_coluna(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_14'):
            w.btn_voltarpararanking2_14.clicked.connect(
                lambda: self._adicionar_linha(t)
            )
        if hasattr(w, 'btn_voltarpararanking2_15'):
            w.btn_voltarpararanking2_15.clicked.connect(
                lambda: self._remover_linha(t)
            )

    def _adicionar_coluna(self, tabela: QTableWidget):
        col = tabela.columnCount()
        tabela.insertColumn(col)
        header = QTableWidgetItem(f"Coluna {col + 1}")
        tabela.setHorizontalHeaderItem(col, header)

    def _remover_coluna(self, tabela: QTableWidget):
        col = tabela.columnCount()
        if col > 0:
            tabela.removeColumn(col - 1)

    def _adicionar_linha(self, tabela: QTableWidget):
        row = tabela.rowCount()
        tabela.insertRow(row)
        tabela.setItem(row, 0, QTableWidgetItem("Nova linha"))

    def _remover_linha(self, tabela: QTableWidget):
        indices = tabela.selectionModel().selectedRows()
        if indices:
            for idx in sorted(indices, key=lambda i: i.row(), reverse=True):
                tabela.removeRow(idx.row())
        elif tabela.rowCount() > 0:
            tabela.removeRow(tabela.rowCount() - 1)
