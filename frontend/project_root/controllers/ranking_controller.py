# =========================================================
# controllers/ranking_controller.py
# Popula as telas de ranking com dados do banco.
# =========================================================
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from services.jogo_service import buscar_ranking, buscar_ranking_geral, NIVEL
 
class RankingController:
    def __init__(self, main):
        self.main = main
        w = main.window
        # Recarregar ranking ao entrar nas páginas
        w.stack.currentChanged.connect(self._on_pagina_mudou)
 
    def _on_pagina_mudou(self, index: int):
        w = self.main.window
        pagina_atual = w.stack.widget(index)
        if pagina_atual is w.pg_rankinggeral:
            self._popular_ranking_geral()
        elif pagina_atual is w.pg_ranking_nav:
            self._popular_ranking_nav()
 
    # --------------------------------------------------
    def _popular_ranking_geral(self):
        w = self.main.window
        dados = buscar_ranking_geral(limite=10)
        # tabela_rankingalunos é o QTableWidget da pg_rankinggeral
        self._preencher_tabela(
            getattr(w, "tabela_rankingalunos", None), dados,
            colunas=["#", "Nome", "Turma", "Pontos"],
            campos=["nome", "turma", "pontuacao_total"],
        )
 
    def _popular_ranking_nav(self):
        w = self.main.window
        # Ranking por nível (fácil=1 por padrão; adapte se houver seletor)
        dados = buscar_ranking(id_nivel=1, limite=10)
        # tabela_rankingturmas é o QTableWidget da pg_ranking_nav
        self._preencher_tabela(
            getattr(w, "tabela_rankingturmas", None), dados,
            colunas=["#", "Nome", "Turma", "Pontos"],
            campos=["nome", "turma", "melhor_pontuacao"],
        )
 
    # --------------------------------------------------
    @staticmethod
    def _preencher_tabela(tabela: QTableWidget, dados: list[dict],
                          colunas: list[str], campos: list[str]):
        if tabela is None or not dados:
            return
        tabela.setRowCount(len(dados))
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        for row, item in enumerate(dados):
            tabela.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            for col, campo in enumerate(campos, start=1):
                valor = str(item.get(campo, ""))
                cell = QTableWidgetItem(valor)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(row, col, cell)