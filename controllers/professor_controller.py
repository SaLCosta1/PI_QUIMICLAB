# =========================================================
# controllers/professor_controller.py
# Popula relatórios de desempenho na área do professor.
# =========================================================
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from services.jogo_service import buscar_desempenho_geral, buscar_desempenho_aluno


class ProfessorController:
    def __init__(self, main):
        self.main = main
        w = main.window
        w.stack.currentChanged.connect(self._on_pagina_mudou)

    def _on_pagina_mudou(self, index: int):
        w = self.main.window
        pagina_atual = w.stack.widget(index)

        if pagina_atual is w.pg_relatoriogeral:
            self._popular_relatorio_geral()
        elif pagina_atual is w.pg_relatorioindividual:
            self._popular_relatorio_individual()

    # --------------------------------------------------
    def _popular_relatorio_geral(self):
        w = self.main.window
        dados = buscar_desempenho_geral()
        tabela = getattr(w, "tbl_relatoriogeral", None)
        if tabela is None or not dados:
            return

        colunas = ["Nome", "Turma", "Nível", "Respostas", "Acertos", "Taxa %", "Tempo Médio"]
        campos  = ["nome", "turma", "nivel", "total_respostas", "acertos", "taxa_acerto_pct", "tempo_medio_seg"]
        self._preencher_tabela(tabela, dados, colunas, campos)

    def _popular_relatorio_individual(self):
        w = self.main.window
        if not self.main.usuario_logado:
            return
        dados = buscar_desempenho_aluno(self.main.usuario_logado["id_usuario"])
        tabela = getattr(w, "tbl_relatorioindividual", None)
        if tabela is None or not dados:
            return

        colunas = ["Nível", "Respostas", "Acertos", "Erros", "Taxa %", "Tempo Médio"]
        campos  = ["nivel", "total_respostas", "acertos", "erros", "taxa_acerto_pct", "tempo_medio_seg"]
        self._preencher_tabela(tabela, dados, colunas, campos)

    # --------------------------------------------------
    @staticmethod
    def _preencher_tabela(tabela: QTableWidget, dados: list[dict],
                          colunas: list[str], campos: list[str]):
        tabela.setRowCount(len(dados))
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for row, item in enumerate(dados):
            for col, campo in enumerate(campos):
                valor = str(item.get(campo, ""))
                cell = QTableWidgetItem(valor)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(row, col, cell)
