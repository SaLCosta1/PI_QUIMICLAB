# =========================================================
# PROFESSOR CONTROLLER
# =========================================================
# Controller responsável pela área do professor.
#
# Esta classe controla funcionalidades relacionadas a:
# - edição de perguntas
# - criação de perguntas
# - exclusão de perguntas
# - relatórios
# - rankings
# - manipulação de tabelas
#
# Atualmente o sistema funciona apenas no FRONT-END,
# ou seja, ainda não existe integração com banco de dados
# ou backend real.
#
# O objetivo deste controller é controlar o comportamento
# visual e a navegação entre as telas da área do professor.
# =========================================================

from PySide6.QtWidgets import (
    QMessageBox,
    QListWidgetItem,
    QTableWidgetItem,
    QTableWidget,
)

from PySide6.QtCore import Qt

from app.utils.helpers import (
    configurar_tabela,
    criar_item_tabela,
)


class ProfessorController:

    # =====================================================
    # CONSTRUTOR
    # =====================================================
    # Recebe a instância principal da aplicação.
    #
    # Aqui são definidos:
    # - os atalhos para a janela
    # - os eventos de clique dos botões
    # - as conexões entre telas
    # =====================================================

    def __init__(self, main):

        self.main = main

        # Atalho para acessar widgets da interface
        w = main.window

        # Atalho para o método de navegação
        ir = main.ir_para

        # Variável utilizada para armazenar
        # a pergunta atualmente selecionada.
        self._pergunta_selecionada = None

        # =================================================
        # pg_areaprof
        # =================================================
        # Tela principal da área do professor.
        # =================================================

        w.btn_voltarloginprof.clicked.connect(
            self._sair_prof
        )

        w.btn_editarperguntas.clicked.connect(
            lambda: self._abrir_editar_perguntas()
        )

        w.btn_relatoriogeral.clicked.connect(
            lambda: self._abrir_relatorio_geral()
        )

        w.btn_ranking.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        # =================================================
        # pg_editarperguntas
        # =================================================
        # Tela responsável pela listagem e gerenciamento
        # das perguntas cadastradas.
        # =================================================

        w.btn_voltarareaprof.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_adicionarpergunta.clicked.connect(
            lambda: self._abrir_adicionar()
        )

        w.btn_editarpergunta.clicked.connect(
            lambda: self._abrir_detalhe_pergunta()
        )

        # =================================================
        # pg_editarpergunta_detalhe
        # =================================================
        # Tela de detalhes da pergunta selecionada.
        # =================================================

        w.btn_voltarpararanking_4.clicked.connect(
            lambda: ir(w.pg_editarperguntas)
        )

        w.btn_editar.clicked.connect(
            lambda: self._abrir_edicao()
        )

        w.btn_excluir.clicked.connect(
            self._confirmar_exclusao
        )

        w.btn_confirmar_exclusao.clicked.connect(
            self._excluir_pergunta
        )

        w.btn_negar_exclusao.clicked.connect(
            self._cancelar_exclusao
        )

        # Detecta alterações no filtro de dificuldade
        w.comboBox_turma3_2.currentIndexChanged.connect(
            self._filtrar_detalhe
        )

        # Detecta seleção de pergunta na lista
        w.lista_alunos3_2.itemClicked.connect(
            self._selecionar_pergunta
        )

        # =================================================
        # pg_questao_edicao
        # =================================================
        # Tela utilizada para editar perguntas.
        # =================================================

        w.btn_voltareditarperguntas.clicked.connect(
            lambda: ir(w.pg_editarpergunta_detalhe)
        )

        w.btn_confirmaredicao.clicked.connect(
            self._confirmar_edicao
        )

        # =================================================
        # pg_questao_adicionar
        # =================================================
        # Tela utilizada para adicionar perguntas.
        # =================================================

        w.btn_voltareditarperguntas_2.clicked.connect(
            lambda: ir(w.pg_editarperguntas)
        )

        w.btn_confirmaradicao.clicked.connect(
            self._confirmar_adicao
        )

        # =================================================
        # pg_ranking
        # =================================================
        # Tela principal dos relatórios.
        # =================================================

        w.btn_voltarareaprof2.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_relatorioturmas.clicked.connect(
            lambda: self._abrir_relatorio_turmas()
        )

        w.btn_relatorioalunos.clicked.connect(
            lambda: self._abrir_relatorio_individual()
        )

        # =================================================
        # pg_ranking_nav
        # =================================================
        # Tela de navegação entre rankings.
        # =================================================

        w.btn_voltarareaprof2_2.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_rankingturmas_2.clicked.connect(
            lambda: self._abrir_ranking_turmas()
        )

        w.btn_rankingalunos_2.clicked.connect(
            lambda: self._abrir_ranking_geral()
        )

        # =================================================
        # pg_relatoriogeral
        # =================================================
        # Tela de relatório geral dos alunos.
        # =================================================

        w.btn_voltarpararanking_2.clicked.connect(
            lambda: ir(w.pg_ranking)
        )

        w.btn_verificar.clicked.connect(
            lambda: ir(w.pg_relatorioindividual)
        )

        w.comboBox_turma2.currentIndexChanged.connect(
            self._filtrar_relatorio_geral
        )

        w.comboBox_modo2.currentIndexChanged.connect(
            self._filtrar_relatorio_geral
        )

        # =================================================
        # pg_relatorioturmas
        # =================================================
        # Tela de relatório por turmas.
        # =================================================

        w.btn_voltarpararanking.clicked.connect(
            lambda: ir(w.pg_ranking)
        )

        w.comboBox_turma3.currentIndexChanged.connect(
            self._filtrar_relatorio_turmas
        )

        w.comboBox_modo2_2.currentIndexChanged.connect(
            self._filtrar_relatorio_turmas
        )

        # =================================================
        # pg_rankinggeral
        # =================================================
        # Tela de ranking geral dos alunos.
        # =================================================

        w.btn_voltarpararanking2.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        w.comboBox_turmas.currentIndexChanged.connect(
            self._filtrar_ranking_geral
        )

        # =================================================
        # BOTÕES DE EDIÇÃO DA TABELA
        # Ranking geral
        # =================================================

        w.btn_voltarpararanking2_8.clicked.connect(
            lambda: self._adicionar_coluna(
                w.tbl_rankinggeral
            )
        )

        w.btn_voltarpararanking2_9.clicked.connect(
            lambda: self._remover_coluna(
                w.tbl_rankinggeral
            )
        )

        w.btn_voltarpararanking2_10.clicked.connect(
            lambda: self._adicionar_linha(
                w.tbl_rankinggeral
            )
        )

        w.btn_voltarpararanking2_11.clicked.connect(
            lambda: self._remover_linha(
                w.tbl_rankinggeral
            )
        )

        # =================================================
        # pg_rankingturmas
        # =================================================

        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        # =================================================
        # BOTÕES DE EDIÇÃO DA TABELA
        # Ranking por turmas
        # =================================================

        w.btn_voltarpararanking2_12.clicked.connect(
            lambda: self._adicionar_coluna(
                w.tabela_rankingturmas
            )
        )

        w.btn_voltarpararanking2_13.clicked.connect(
            lambda: self._remover_coluna(
                w.tabela_rankingturmas
            )
        )

        w.btn_voltarpararanking2_14.clicked.connect(
            lambda: self._adicionar_linha(
                w.tabela_rankingturmas
            )
        )

        w.btn_voltarpararanking2_15.clicked.connect(
            lambda: self._remover_linha(
                w.tabela_rankingturmas
            )
        )

        # =================================================
        # pg_relatorioindividual
        # =================================================

        w.btn_voltarpararanking_5.clicked.connect(
            lambda: ir(w.pg_relatoriogeral)
        )

        # =================================================
        # CONFIGURAÇÃO INICIAL DAS TABELAS
        # =================================================
        # Aplica estilo e comportamento padrão.
        # =================================================

        configurar_tabela(w.tbl_rankinggeral)
        configurar_tabela(w.tabela_rankingturmas)

    # =====================================================
    # EDITAR PERGUNTAS
    # =====================================================

    def _abrir_editar_perguntas(self):
        """
        Abre a tela de edição de perguntas.
        """

        self.main.ir_para(
            self.main.window.pg_editarperguntas
        )

    def _abrir_detalhe_pergunta(self):
        """
        Abre a tela de detalhes da pergunta.

        Também limpa os filtros e a lista visual.
        """

        w = self.main.window

        # Evita disparar sinais durante atualização
        w.comboBox_turma3_2.blockSignals(True)

        w.comboBox_turma3_2.clear()

        # Adiciona filtros disponíveis
        w.comboBox_turma3_2.addItems([
            "Todas",
            "Fácil",
            "Médio",
            "Difícil"
        ])

        w.comboBox_turma3_2.blockSignals(False)

        # Limpa lista de perguntas
        w.lista_alunos3_2.clear()

        # Esconde botões de exclusão
        self._esconder_botoes_exclusao()

        self.main.ir_para(
            w.pg_editarpergunta_detalhe
        )

    def _filtrar_detalhe(self):
        """
        Método reservado para futura integração
        com backend.

        Será responsável por filtrar perguntas
        conforme a dificuldade selecionada.
        """
        pass