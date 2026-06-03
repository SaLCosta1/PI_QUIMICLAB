# =========================================================
# RANKING CONTROLLER
# Responsável por controlar a navegação entre telas de ranking
# e também a edição das tabelas (adicionar/remover linhas e colunas)
#
# Telas envolvidas:
# - pg_ranking_nav     -> tela principal de escolha
# - pg_rankinggeral    -> ranking de alunos
# - pg_rankingturmas   -> ranking de turmas
# =========================================================

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class RankingController:
    """
    Classe responsável por:
    - Controlar a navegação entre telas de ranking
    - Gerenciar ações de edição das tabelas (linhas e colunas)
    """

    def __init__(self, main):
        # Guarda referência da aplicação principal
        # (permite acessar janelas, botões e funções globais)
        self.main   = main

        # Janela principal da interface
        self.window = main.window

        # Função de navegação entre telas
        self.ir     = main.ir_para

        # Inicializa todas as conexões de botões e eventos
        self.setup()

    # =====================================================
    # SETUP GERAL
    # =====================================================

    def setup(self):
        # Organiza a inicialização em partes menores
        # para facilitar manutenção do código
        self._setup_navegacao()
        self._setup_rankinggeral()
        self._setup_rankingturmas()

    # =====================================================
    # NAVEGAÇÃO ENTRE TELAS DE RANKING
    # =====================================================

    def _setup_navegacao(self):
        w  = self.window  # atalho para a janela
        ir = self.ir      # atalho para função de navegação

        # -------------------------------------------------
        # Botões da tela inicial de ranking
        # -------------------------------------------------

        # Vai para ranking de turmas
        w.btn_rankingturmas_2.clicked.connect(
            lambda: ir(w.pg_rankingturmas)
        )

        # Vai para ranking geral (alunos)
        w.btn_rankingalunos_2.clicked.connect(
            lambda: ir(w.pg_rankinggeral)
        )

        # -------------------------------------------------
        # Botões de voltar para tela de navegação
        # -------------------------------------------------

        w.btn_voltarpararanking2.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

    # =====================================================
    # RANKING GERAL (tabela de alunos)
    # =====================================================

    def _setup_rankinggeral(self):
        w = self.window
        t = w.tbl_rankinggeral  # tabela do ranking geral

        # Botões para editar a tabela:
        # adicionar/remover colunas e linhas

        w.btn_voltarpararanking2_8.clicked.connect(
            lambda: self._adicionar_coluna(t)
        )

        w.btn_voltarpararanking2_9.clicked.connect(
            lambda: self._remover_coluna(t)
        )

        w.btn_voltarpararanking2_10.clicked.connect(
            lambda: self._adicionar_linha(t)
        )

        w.btn_voltarpararanking2_11.clicked.connect(
            lambda: self._remover_linha(t)
        )

    # =====================================================
    # RANKING TURMAS (tabela de turmas)
    # =====================================================

    def _setup_rankingturmas(self):
        w = self.window
        t = w.tabela_rankingturmas  # tabela de turmas

        # Mesma lógica do ranking geral,
        # mas aplicada na tabela de turmas

        w.btn_voltarpararanking2_12.clicked.connect(
            lambda: self._adicionar_coluna(t)
        )

        w.btn_voltarpararanking2_13.clicked.connect(
            lambda: self._remover_coluna(t)
        )

        w.btn_voltarpararanking2_14.clicked.connect(
            lambda: self._adicionar_linha(t)
        )

        w.btn_voltarpararanking2_15.clicked.connect(
            lambda: self._remover_linha(t)
        )

    # =====================================================
    # FUNÇÕES AUXILIARES (MANIPULAÇÃO DA TABELA)
    # =====================================================

    def _adicionar_coluna(self, tabela: QTableWidget):
        """
        Adiciona uma nova coluna no final da tabela
        e cria um título padrão para ela.
        """
        col = tabela.columnCount()
        tabela.insertColumn(col)

        # Define nome da nova coluna
        header = QTableWidgetItem(f"Coluna {col + 1}")
        tabela.setHorizontalHeaderItem(col, header)

    def _remover_coluna(self, tabela: QTableWidget):
        """
        Remove a última coluna da tabela (se existir).
        """
        col = tabela.columnCount()
        if col > 0:
            tabela.removeColumn(col - 1)

    def _adicionar_linha(self, tabela: QTableWidget):
        """
        Adiciona uma nova linha no final da tabela.
        Preenche a primeira célula com texto padrão.
        """
        row = tabela.rowCount()
        tabela.insertRow(row)

        # Texto inicial para indicar nova linha criada
        tabela.setItem(row, 0, QTableWidgetItem("Nova linha"))

    def _remover_linha(self, tabela: QTableWidget):
        """
        Remove linhas selecionadas.
        Se nenhuma linha estiver selecionada,
        remove a última linha da tabela.
        """
        indices = tabela.selectionModel().selectedRows()

        if indices:
            # Remove de baixo para cima para evitar erros de índice
            for idx in sorted(indices, key=lambda i: i.row(), reverse=True):
                tabela.removeRow(idx.row())

        elif tabela.rowCount() > 0:
            tabela.removeRow(tabela.rowCount() - 1)