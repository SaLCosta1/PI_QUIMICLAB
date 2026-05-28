# =========================================================
# controllers/professor_controller.py
# Popula relatórios de desempenho na área do professor.
# Adaptado para usar os widgets reais do front_viewer.ui.
# =========================================================
from services.jogo_service import buscar_desempenho_geral, buscar_desempenho_aluno
 
 
class ProfessorController:
    def __init__(self, main):
        self.main = main
        w = main.window
 
        # Recarrega ao entrar nas páginas
        w.stack.currentChanged.connect(self._on_pagina_mudou)
 
        # Botão Verificar: carrega resultado do aluno selecionado na lista
        w.btn_verificar.clicked.connect(self._verificar_aluno)
 
        # Quando mudar turma ou modo, recarrega lista de alunos
        w.comboBox_turma2.currentIndexChanged.connect(self._recarregar_lista)
        w.comboBox_modo2.currentIndexChanged.connect(self._recarregar_lista)
 
    # --------------------------------------------------
    def _on_pagina_mudou(self, index: int):
        w = self.main.window
        pagina_atual = w.stack.widget(index)
        if pagina_atual is w.pg_relatoriogeral:
            self._carregar_filtros()
        elif pagina_atual is w.pg_relatorioindividual:
            self._popular_relatorio_individual()
 
    # --------------------------------------------------
    # pg_relatoriogeral
    # --------------------------------------------------
    def _carregar_filtros(self):
        """Preenche os ComboBoxes de turma e nível e carrega a lista de alunos."""
        w = self.main.window
        dados = buscar_desempenho_geral()
        if not dados:
            return
 
        # Turmas únicas
        turmas = sorted({d["turma"] for d in dados if d.get("turma")})
        w.comboBox_turma2.blockSignals(True)
        w.comboBox_turma2.clear()
        w.comboBox_turma2.addItem("Todas")
        w.comboBox_turma2.addItems(turmas)
        w.comboBox_turma2.blockSignals(False)
 
        # Níveis únicos
        niveis = sorted({d["nivel"] for d in dados if d.get("nivel")})
        w.comboBox_modo2.blockSignals(True)
        w.comboBox_modo2.clear()
        w.comboBox_modo2.addItem("Todos")
        w.comboBox_modo2.addItems(niveis)
        w.comboBox_modo2.blockSignals(False)
 
        self._recarregar_lista()
 
    def _recarregar_lista(self):
        """Filtra e preenche lista_alunos2 conforme turma/nível selecionados."""
        w = self.main.window
        dados = buscar_desempenho_geral()
        if not dados:
            return
 
        turma_sel = w.comboBox_turma2.currentText()
        nivel_sel = w.comboBox_modo2.currentText()
 
        filtrados = [
            d for d in dados
            if (turma_sel == "Todas" or d.get("turma") == turma_sel)
            and (nivel_sel == "Todos" or d.get("nivel") == nivel_sel)
        ]
 
        w.lista_alunos2.clear()
        for d in filtrados:
            # Guarda o id_usuario como dado oculto via UserRole
            from PySide6.QtWidgets import QListWidgetItem
            from PySide6.QtCore import Qt
            item = QListWidgetItem(f"{d['nome']}  —  {d['turma']}")
            item.setData(Qt.ItemDataRole.UserRole, d["id_usuario"])
            w.lista_alunos2.addItem(item)
 
        # Limpa resultado anterior
        self._limpar_card2()
 
    def _verificar_aluno(self):
        """Carrega no card2 os dados do aluno selecionado em lista_alunos2."""
        w = self.main.window
        from PySide6.QtCore import Qt
 
        item = w.lista_alunos2.currentItem()
        if item is None:
            return
 
        id_usuario = item.data(Qt.ItemDataRole.UserRole)
        dados = buscar_desempenho_aluno(id_usuario)
        if not dados:
            self._limpar_card2()
            return
 
        # Agrega métricas de todos os níveis do aluno
        total_respostas = sum(d.get("total_respostas", 0) for d in dados)
        total_acertos   = sum(d.get("acertos", 0) for d in dados)
        taxa            = round(total_acertos / total_respostas * 100, 1) if total_respostas else 0
        media_geral     = buscar_desempenho_geral()  # para calcular comparação
 
        media_taxa = 0
        if media_geral:
            tr = sum(d.get("total_respostas", 0) for d in media_geral)
            ta = sum(d.get("acertos", 0) for d in media_geral)
            media_taxa = round(ta / tr * 100, 1) if tr else 0
 
        comparacao = round(taxa - media_taxa, 1)
        sinal = "+" if comparacao >= 0 else ""
 
        w.lbl_acertos2.setText(f"{total_acertos} acerto(s) de {total_respostas}")
        w.lbl_comparacaomedia.setText(f"{sinal}{comparacao}% em relação à média geral")
        w.lbl_mediaturma.setText(f"Média geral da turma: {media_taxa}%")
 
    def _limpar_card2(self):
        w = self.main.window
        w.lbl_acertos2.setText("")
        w.lbl_comparacaomedia.setText("")
        w.lbl_mediaturma.setText("")
 
    # --------------------------------------------------
    # pg_relatorioindividual — dados do aluno logado
    # --------------------------------------------------
    def _popular_relatorio_individual(self):
        """Preenche a tela de relatório individual com dados do aluno logado."""
        w = self.main.window
        if not self.main.usuario_logado:
            return
 
        id_usuario = self.main.usuario_logado["id_usuario"]
        nome       = self.main.usuario_logado.get("nome", "")
        dados      = buscar_desempenho_aluno(id_usuario)
 
        # Nome do aluno no título
        w.lbl_titulo_gabarito_2.setText(f"Nome: {nome}")
 
        if not dados:
            w.lbl_nivel2_2.setText("—")
            w.lbl_suaresposta_2.setText("—")
            w.lbl_gabarito_2.setText("—")
            w.lbl_nivel2_3.setText("—")
            w.lbl_nivel2_4.setText("—")
            return
 
        # Agrega métricas de todos os níveis
        total_respostas = sum(d.get("total_respostas", 0) for d in dados)
        total_acertos   = sum(d.get("acertos", 0) for d in dados)
        pontuacao       = sum(d.get("pontuacao_total", 0) for d in dados)
        taxa            = round(total_acertos / total_respostas * 100, 1) if total_respostas else 0
 
        tempos = [d.get("tempo_medio_seg", 0) for d in dados if d.get("tempo_medio_seg")]
        tempo_medio = round(sum(tempos) / len(tempos), 1) if tempos else 0
 
        dicas = [d.get("taxa_dicas_pct", 0) for d in dados if d.get("taxa_dicas_pct") is not None]
        taxa_dicas = round(sum(dicas) / len(dicas), 1) if dicas else 0
 
        # Nível mais alto desbloqueado
        ordem = {"facil": 1, "medio": 2, "dificil": 3}
        niveis_jogados = [d["nivel"] for d in dados if d.get("nivel")]
        nivel_max = max(niveis_jogados, key=lambda n: ordem.get(n, 0)) if niveis_jogados else "—"
 
        # Preenche os labels
        w.lbl_nivel2_2.setText(nivel_max.capitalize())      # Nível Máximo Desbloqueado
        w.lbl_suaresposta_2.setText(f"{taxa}%")             # % de Acertos
        w.lbl_gabarito_2.setText(str(pontuacao))            # Pontuação Total
        w.lbl_nivel2_3.setText(f"{tempo_medio}s")          # Tempo Médio de Resposta
        w.lbl_nivel2_4.setText(f"{taxa_dicas}%")           # % de Uso de Dicas