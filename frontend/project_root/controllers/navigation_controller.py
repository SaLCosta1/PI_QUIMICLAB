# =========================================================
# controllers/navigation_controller.py
# =========================================================
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt
 
 
class NavigationController:
    def __init__(self, main):
        self.main = main
        w = main.window
        self._stack = w.stack
        self._conectar()
 
    def ir_para(self, pagina: QWidget):
        self._stack.setCurrentWidget(pagina)
 
    def _btn(self, nome):
        return getattr(self.main.window, nome, None)
 
    def _liga(self, nome_btn, pagina_destino):
        btn = self._btn(nome_btn)
        if btn:
            btn.clicked.connect(lambda: self.ir_para(pagina_destino))
 
    def _conectar(self):
        w = self.main.window
 
        # Início → termos de uso
        self._liga('btn_jogar',           w.page_3)
        self._liga('btn_comojogar',       w.pg_comojogar)
 
        # Termos de uso
        # btn_voltarperfil_2 = Voltar (volta para início)
        self._liga('btn_voltarperfil_2',  w.pg_inicio)
 
        # Ao entrar na page_3, bloqueia checkbox e botão Aceitar
        w.stack.currentChanged.connect(self._on_pagina_mudou)
 
        # btn_voltarperfil_3 = Aceitar (só avança se checkbox marcado)
        btn_aceitar = self._btn('btn_voltarperfil_3')
        if btn_aceitar:
            btn_aceitar.clicked.connect(self._aceitar_termos)
 
        # Scroll dos termos — libera checkbox ao chegar no fim
        scroll = getattr(w, 'txt_comojogar_2', None)
        if scroll:
            scroll.verticalScrollBar().valueChanged.connect(
                self._on_scroll_termos
            )
 
        # Perfil
        self._liga('btn_voltarinicio',    w.pg_inicio)
        self._liga('btn_soualuno',        w.pg_loginaluno)
        self._liga('btn_souprof',         w.pg_loginprof)
 
        # Como jogar → voltar
        self._liga('btn_voltarperfil',    w.pg_perfil)
 
        # Login aluno → voltar
        self._liga('btn_voltarperfil2',   w.pg_perfil)
        self._liga('btn_voltarperfil2_2', w.pg_perfil)
        self._liga('btn_voltarperfil2_3', w.pg_perfil)
        self._liga('btn_voltarperfil3',   w.pg_perfil)
        self._liga('btn_voltarperfil3_2', w.pg_perfil)
        self._liga('btn_voltarperfil4',   w.pg_perfil)
 
        # Login professor
        self._liga('btn_voltarloginprof', w.pg_loginprof)
 
        # Cadastro professor
        self._liga('btn_cadastroaluno',   w.pg_loginaluno)
 
        # Tipo jogo → modos
        self._liga('btn_tradicional',     w.pg_modos)
        self._liga('btn_desafio',         w.pg_modos)
        self._liga('btn_voltar_tipojogo', w.pg_perfil)
 
        # Área professor
        self._liga('btn_editarperguntas', w.pg_editarperguntas)
        self._liga('btn_relatoriogeral',  w.pg_relatoriogeral)
        self._liga('btn_ranking',         w.pg_rankinggeral)
 
        # Editar perguntas
        self._liga('btn_voltarareaprof',          w.pg_areaprof)
        self._liga('btn_voltarareaprof2',         w.pg_areaprof)
        self._liga('btn_voltareaprof2_2',        w.pg_areaprof)
        self._liga('btn_voltareditarperguntas',   w.pg_editarperguntas)
        self._liga('btn_voltareditarperguntas_2', w.pg_editarperguntas)
        self._liga('btn_adicionarpergunta',       w.pg_questao_adicionar)
        self._liga('btn_editarpergunta',          w.pg_editarpergunta_detalhe)
 
        # Ranking
        self._liga('btn_rankingturmas_2',      w.pg_rankingturmas)
        self._liga('btn_rankingalunos_2',      w.pg_ranking_nav)
        self._liga('btn_voltarpararanking',    w.pg_rankinggeral)
        self._liga('btn_voltarpararanking_2',  w.pg_rankinggeral)
        self._liga('btn_voltarpararanking_4',  w.pg_rankinggeral)
        self._liga('btn_voltarpararanking_5',  w.pg_rankinggeral)
        self._liga('btn_voltarpararanking2',   w.pg_ranking)
        self._liga('btn_voltarpararanking2_3', w.pg_ranking)
 
        # Relatório
        self._liga('btn_relatorioalunos',  w.pg_relatorioindividual)
        self._liga('btn_relatorioturmas',  w.pg_relatorioturmas)
 
        # Modos → questão (tratado pelo QuestionController)
        self._liga('btn_voltarmodos3',   w.pg_modos)
        self._liga('btn_voltarmodos3_2', w.pg_modos)
 
        # Gabarito
        self._liga('btn_gabarito',       w.pg_gabarito)
 
    # --------------------------------------------------
    def _on_pagina_mudou(self, index: int):
        """Ao entrar na tela de termos, reseta checkbox e bloqueia botão Aceitar."""
        w = self.main.window
        if w.stack.widget(index) is w.page_3:
            # Desmarca e desabilita checkbox
            w.checkBox.setChecked(False)
            w.checkBox.setEnabled(False)
            # Desabilita botão Aceitar
            btn = self._btn('btn_voltarperfil_3')
            if btn:
                btn.setEnabled(False)
            # Volta scroll para o topo
            scroll = getattr(w, 'txt_comojogar_2', None)
            if scroll:
                scroll.verticalScrollBar().setValue(0)
 
    def _on_scroll_termos(self, value: int):
        """Libera checkbox e botão Aceitar quando o scroll chega ao fim."""
        w = self.main.window
        scrollbar = w.txt_comojogar_2.verticalScrollBar()
        if value >= scrollbar.maximum():
            w.checkBox.setEnabled(True)
            btn = self._btn('btn_voltarperfil_3')
            if btn:
                btn.setEnabled(True)
 
    # --------------------------------------------------
    def _aceitar_termos(self):
        """Avança para pg_perfil somente se o checkbox estiver marcado."""
        w = self.main.window
        if w.checkBox.isChecked():
            self.ir_para(w.pg_perfil)
        else:
            QMessageBox.warning(
                w,
                "Termos de Uso",
                "Você precisa marcar a caixa de confirmação\n"
                "para aceitar os Termos de Uso antes de continuar."
            )