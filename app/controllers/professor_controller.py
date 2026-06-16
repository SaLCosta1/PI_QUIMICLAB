from PySide6.QtWidgets import (
    QMessageBox,
    QListWidgetItem,
    QTableWidgetItem,
    QTableWidget,
)

from PySide6.QtCore import Qt

from app.utils.helpers import (
    configurar_tabela,
    configurar_lista,
    estilo_valor,
    criar_item_tabela,
)

from app.services.pergunta_service import criar_pergunta, listar_perguntas, atualizar_pergunta, deletar_pergunta, obter_pergunta

class ProfessorController:

    def __init__(self, main):
        self.main = main
        w = main.window
        ir = main.ir_para
        self._pergunta_selecionada = None

        w.btn_voltarloginprof.clicked.connect(
            self._sair_prof
        )

        w.btn_editarperguntas.clicked.connect(
            lambda: self._abrir_editar_perguntas()
        )

        w.btn_relatoriogeral.clicked.connect(
            lambda: ir(w.pg_ranking)
        )

        w.btn_ranking.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        w.btn_voltarareaprof.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_adicionarpergunta.clicked.connect(
            lambda: self._abrir_adicionar()
        )

        w.btn_editarpergunta.clicked.connect(
            lambda: self._abrir_detalhe_pergunta()
        )

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

        w.comboBox_turma3_2.currentIndexChanged.connect(
            self._filtrar_detalhe
        )

        w.lista_alunos3_2.itemClicked.connect(
            self._selecionar_pergunta
        )

        w.btn_voltareditarperguntas.clicked.connect(
            lambda: ir(w.pg_editarpergunta_detalhe)
        )

        w.btn_confirmaredicao.clicked.connect(
            self._confirmar_edicao
        )

        w.btn_voltareditarperguntas_2.clicked.connect(
            lambda: ir(w.pg_editarperguntas)
        )

        w.btn_confirmaradicao.clicked.connect(
            self._confirmar_adicao
        )

        w.btn_voltarareaprof2.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_relatorioturmas.clicked.connect(
            lambda: self._abrir_relatorio_turmas()
        )

        w.btn_voltarareaprof2_2.clicked.connect(
            lambda: ir(w.pg_areaprof)
        )

        w.btn_rankingturmas_2.clicked.connect(
            lambda: self._abrir_ranking_turmas()
        )

        w.btn_rankingalunos_2.clicked.connect(
            lambda: self._abrir_ranking_geral()
        )

        w.btn_voltarpararanking.clicked.connect(
            lambda: ir(w.pg_ranking)
        )

        w.comboBox_turma3.currentIndexChanged.connect(
            self._filtrar_relatorio_turmas
        )

        w.comboBox_modo2_2.currentIndexChanged.connect(
            self._filtrar_relatorio_turmas
        )

        # Ao clicar num aluno da lista, o painel troca da visão "turma" para "aluno".
        w.lista_alunos3.itemClicked.connect(
            self._mostrar_aluno_turma
        )

        w.btn_voltarpararanking2.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        w.comboBox_turmas.currentIndexChanged.connect(
            self._filtrar_ranking_geral
        )

        w.btn_voltarpararanking2_3.clicked.connect(
            lambda: ir(w.pg_ranking_nav)
        )

        # Botões inúteis de adicionar/remover linha/coluna (resíduo): escondidos.
        for _nome in (
            'btn_voltarpararanking2_8', 'btn_voltarpararanking2_9',
            'btn_voltarpararanking2_10', 'btn_voltarpararanking2_11',
            'btn_voltarpararanking2_12', 'btn_voltarpararanking2_13',
            'btn_voltarpararanking2_14', 'btn_voltarpararanking2_15',
        ):
            if hasattr(w, _nome):
                getattr(w, _nome).hide()

        w.btn_voltarpararanking_5.clicked.connect(
            lambda: ir(w.pg_ranking)
        )

        configurar_tabela(w.tbl_rankinggeral)
        configurar_tabela(w.tabela_rankingturmas)

        for _lst in (
            'lista_alunos3',
            'lista_perguntascommenosacerto', 'lista_alunos3_2',
        ):
            if hasattr(w, _lst):
                configurar_lista(getattr(w, _lst))

        for _val in (
            'lbl_mediaturma2', 'lbl_menornota', 'lbl_maiornota',
            'lbl_acertos_aluno', 'lbl_comparacao_aluno', 'lbl_mediaturma_aluno',
        ):
            if hasattr(w, _val):
                estilo_valor(getattr(w, _val))

    def _abrir_editar_perguntas(self):

        self.main.ir_para(
            self.main.window.pg_editarperguntas
        )

    def _abrir_detalhe_pergunta(self):

        w = self.main.window

        w.comboBox_turma3_2.blockSignals(True)

        w.comboBox_turma3_2.clear()

        w.comboBox_turma3_2.addItems([
            "Todas",
            "Fácil",
            "Médio",
            "Difícil"
        ])

        w.comboBox_turma3_2.blockSignals(False)

        w.lista_alunos3_2.clear()

        perguntas = listar_perguntas()
        for pergunta in perguntas:
            item_text = f"[{pergunta['nome_nivel']}] {pergunta['enunciado']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, pergunta['id_pergunta'])
            w.lista_alunos3_2.addItem(item)

        self._esconder_botoes_exclusao()

        self.main.ir_para(
            w.pg_editarpergunta_detalhe
        )

    def _sair_prof(self):
        # Sai da área do professor direto para a escolha aluno/professor.
        self.main.usuario_logado = None
        self.main.ir_para(self.main.window.pg_perfil)

    # Widgets do painel direito da tela de turmas, separados por visão.
    _WIDGETS_TURMA = (
        'lbl_dado1c_relatorio', 'lbl_mediaturma2',
        'lbl_dado2c_relatorio', 'lbl_menornota',
        'lbl_rodape2_relatorio', 'lbl_maiornota',
        'lbl_dado3c_relatorio', 'lista_perguntascommenosacerto',
    )
    _WIDGETS_ALUNO = (
        'lbl_alunoview_titulo',
        'lbl_alunoview_h1', 'lbl_acertos_aluno',
        'lbl_alunoview_h2', 'lbl_comparacao_aluno',
        'lbl_alunoview_h3', 'lbl_mediaturma_aluno',
    )

    def _mostrar_grupo(self, nomes, visivel):
        w = self.main.window
        for n in nomes:
            if hasattr(w, n):
                getattr(w, n).setVisible(visivel)

    def _ver_painel_turma(self):
        """Volta o painel da direita para a visão da turma."""
        self._mostrar_grupo(self._WIDGETS_ALUNO, False)
        self._mostrar_grupo(self._WIDGETS_TURMA, True)

    def _mostrar_aluno_turma(self, *args):
        """Troca o painel da direita para os dados do aluno clicado na lista."""
        from app.services.jogo_service import (
            contar_acertos_nivel_aluno,
            buscar_alunos_por_turma,
        )

        w = self.main.window
        item = w.lista_alunos3.currentItem() if hasattr(w, 'lista_alunos3') else None
        if not item:
            return

        aluno = item.data(1000)
        id_nivel = item.data(1001) or 1
        if not aluno:
            return

        id_usuario = aluno.get('id_usuario')
        turma = aluno.get('turma')
        nome = aluno.get('nome', 'N/A')

        acertos = contar_acertos_nivel_aluno(id_usuario, id_nivel)

        # Média da turma no mesmo nível (perguntas distintas acertadas)
        media = 0.0
        if turma:
            colegas = buscar_alunos_por_turma(turma)
            valores = [contar_acertos_nivel_aluno(c.get('id_usuario'), id_nivel) for c in colegas]
            if valores:
                media = sum(valores) / len(valores)

        if hasattr(w, 'lbl_alunoview_titulo'):
            w.lbl_alunoview_titulo.setText(f"Aluno: {nome}")
        if hasattr(w, 'lbl_acertos_aluno'):
            w.lbl_acertos_aluno.setText(str(acertos))
        if hasattr(w, 'lbl_mediaturma_aluno'):
            w.lbl_mediaturma_aluno.setText(f"{media:.1f}")
        if hasattr(w, 'lbl_comparacao_aluno'):
            if acertos > media:
                w.lbl_comparacao_aluno.setText("Acima da média")
            elif acertos < media:
                w.lbl_comparacao_aluno.setText("Abaixo da média")
            else:
                w.lbl_comparacao_aluno.setText("Na média")

        # Troca a visão: esconde os cards da turma, mostra os do aluno.
        self._mostrar_grupo(self._WIDGETS_TURMA, False)
        self._mostrar_grupo(self._WIDGETS_ALUNO, True)

    def _abrir_relatorio_turmas(self):
        try:
            from app.services.jogo_service import buscar_turmas

            w = self.main.window

            turmas = buscar_turmas()

            if hasattr(w, 'comboBox_turma3'):
                w.comboBox_turma3.blockSignals(True)
                w.comboBox_turma3.clear()
                w.comboBox_turma3.addItem("Todas")
                for turma in turmas:
                    w.comboBox_turma3.addItem(turma)
                w.comboBox_turma3.blockSignals(False)
                w.comboBox_turma3.setCurrentIndex(0)

            if hasattr(w, 'comboBox_modo2_2'):
                w.comboBox_modo2_2.blockSignals(True)
                w.comboBox_modo2_2.clear()
                w.comboBox_modo2_2.addItems(["Fácil", "Médio", "Difícil"])
                w.comboBox_modo2_2.blockSignals(False)
                w.comboBox_modo2_2.setCurrentIndex(0)

            self._filtrar_relatorio_turmas()
            self.main.ir_para(w.pg_relatorioturmas)

        except Exception as exc:
            print(f"[ProfessorController] Erro ao abrir relatório de turmas: {exc}")

    def _abrir_relatorio_individual(self):
        w = self.main.window

        if not hasattr(w, 'lista_alunos3') or not w.lista_alunos3.currentItem():
            QMessageBox.warning(w, 'Erro', 'Selecione um aluno para ver o relatório.')
            return

        item_selecionado = w.lista_alunos3.currentItem()
        dados_aluno = item_selecionado.data(1000)
        id_nivel = item_selecionado.data(1001)

        if not dados_aluno:
            QMessageBox.warning(w, 'Erro', 'Não foi possível obter dados do aluno.')
            return

        # Adiciona id_nivel aos dados do aluno para usar em _preencher_relatorio_individual
        if id_nivel:
            dados_aluno['id_nivel'] = id_nivel
            
            # Busca pontuação no ranking para comparação com média geral
            try:
                from app.services.jogo_service import buscar_ranking
                ranking = buscar_ranking(id_nivel, limite=500)
                id_usuario = dados_aluno.get('id_usuario')
                for r in ranking:
                    if r.get('id_usuario') == id_usuario:
                        dados_aluno['melhor_pontuacao'] = r.get('melhor_pontuacao', 0)
                        break
                else:
                    dados_aluno['melhor_pontuacao'] = 0
            except Exception as e:
                print(f"[ProfessorController] Erro ao buscar ranking para pontuação: {e}")
                dados_aluno['melhor_pontuacao'] = 0

        self._aluno_selecionado = dados_aluno

        try:
            self._preencher_relatorio_individual(dados_aluno)
        except Exception as exc:
            QMessageBox.warning(w, 'Erro', f'Erro ao carregar relatório: {exc}')
            return

        self.main.ir_para(w.pg_relatorioindividual)

    def _abrir_ranking_turmas(self):
        try:
            self._preencher_ranking_turmas()
            self.main.ir_para(self.main.window.pg_rankingturmas)
        except Exception as exc:
            print(f"[ProfessorController] Erro ao abrir ranking de turmas: {exc}")

    def _preencher_ranking_turmas(self):
        from app.services.jogo_service import buscar_ranking_turmas

        w = self.main.window
        if not hasattr(w, 'tabela_rankingturmas'):
            return

        dados = buscar_ranking_turmas()
        tabela = w.tabela_rankingturmas
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(
            ["Posição", "Turma", "Pontuação média", "Nº de alunos"]
        )
        tabela.horizontalHeader().setVisible(True)
        tabela.setRowCount(0)
        for idx, t in enumerate(dados):
            tabela.insertRow(idx)
            tabela.setItem(idx, 0, criar_item_tabela(idx + 1))
            tabela.setItem(idx, 1, criar_item_tabela(t.get('turma') or '-'))
            tabela.setItem(idx, 2, criar_item_tabela(t.get('media', 0)))
            tabela.setItem(idx, 3, criar_item_tabela(t.get('n_alunos', 0)))

    def _abrir_ranking_geral(self):
        try:
            w = self.main.window

            from app.services.jogo_service import buscar_turmas

            if hasattr(w, 'comboBox_turmas'):
                w.comboBox_turmas.blockSignals(True)
                w.comboBox_turmas.clear()
                w.comboBox_turmas.addItem("Todas")
                for turma in buscar_turmas():
                    w.comboBox_turmas.addItem(turma)
                w.comboBox_turmas.blockSignals(False)
                w.comboBox_turmas.setCurrentIndex(0)

            self._filtrar_ranking_geral()
            self.main.ir_para(w.pg_rankinggeral)

        except Exception as exc:
            print(f"[ProfessorController] Erro ao abrir ranking geral: {exc}")

    def _abrir_edicao(self):
        if not hasattr(self, '_pergunta_id') or not self._pergunta_id:
            QMessageBox.warning(self.main.window, 'Erro', 'Nenhuma pergunta selecionada.')
            return

        pergunta_dados = obter_pergunta(self._pergunta_id)
        if not pergunta_dados:
            QMessageBox.warning(self.main.window, 'Erro', 'Pergunta não encontrada.')
            return

        self.main.editor_controller.preencher_edicao(pergunta_dados)

        self.main.ir_para(self.main.window.pg_questao_edicao)

    def _abrir_adicionar(self):
        self.main.editor_controller.limpar_campos_adicao()

        self.main.ir_para(self.main.window.pg_questao_adicionar)

    def _confirmar_exclusao(self):
        w = self.main.window

        if hasattr(w, 'btn_editar'):
            w.btn_editar.setVisible(False)
        if hasattr(w, 'btn_excluir'):
            w.btn_excluir.setVisible(False)

        if hasattr(w, 'btn_confirmar_exclusao'):
            w.btn_confirmar_exclusao.setVisible(True)
        if hasattr(w, 'btn_negar_exclusao'):
            w.btn_negar_exclusao.setVisible(True)
        if hasattr(w, 'lbl_alt1_editarpergunta_3'):
            w.lbl_alt1_editarpergunta_3.setVisible(True)

    def _cancelar_exclusao(self):

        w = self.main.window

        if hasattr(w, 'btn_editar'):
            w.btn_editar.setVisible(True)
        if hasattr(w, 'btn_excluir'):
            w.btn_excluir.setVisible(True)

        if hasattr(w, 'btn_confirmar_exclusao'):
            w.btn_confirmar_exclusao.setVisible(False)
        if hasattr(w, 'btn_negar_exclusao'):
            w.btn_negar_exclusao.setVisible(False)
        if hasattr(w, 'lbl_alt1_editarpergunta_3'):
            w.lbl_alt1_editarpergunta_3.setVisible(False)

    def _excluir_pergunta(self):

        if not hasattr(self, '_pergunta_id') or not self._pergunta_id:
            QMessageBox.warning(self.main.window, 'Erro', 'Nenhuma pergunta selecionada.')
            return

        ok, erro = deletar_pergunta(self._pergunta_id)
        if not ok:
            QMessageBox.warning(self.main.window, 'Erro', f'Falha ao excluir pergunta: {erro}')
            return

        QMessageBox.information(self.main.window, 'Sucesso', 'Pergunta excluída com sucesso.')
        self.main.ir_para(self.main.window.pg_editarperguntas)

    def _confirmar_edicao(self):

        if not hasattr(self, '_pergunta_id') or not self._pergunta_id:
            QMessageBox.warning(self.main.window, 'Erro', 'Nenhuma pergunta selecionada.')
            return

        dados = None
        try:
            dados = self.main.editor_controller.coletar_edicao()
        except Exception as e:
            QMessageBox.warning(self.main.window, 'Erro', f'Erro ao coletar dados: {str(e)}')
            return

        if not dados:
            self.main.ir_para(self.main.window.pg_editarpergunta_detalhe)
            return

        ok, erro = atualizar_pergunta(self._pergunta_id, dados)
        if not ok:
            QMessageBox.warning(self.main.window, 'Erro', f'Falha ao atualizar pergunta: {erro}')
            return

        QMessageBox.information(self.main.window, 'Sucesso', 'Pergunta atualizada com sucesso.')
        self.main.ir_para(self.main.window.pg_editarpergunta_detalhe)

    def _confirmar_adicao(self):
        dados = None
        try:
            dados = self.main.editor_controller.coletar_adicao()
        except Exception:
            pass

        if not dados:
            self.main.ir_para(self.main.window.pg_editarperguntas)
            return

        criador = self.main.usuario_logado.get('id_usuario') if self.main.usuario_logado else None

        ok, erro = criar_pergunta(dados, criador)
        if not ok:
            QMessageBox.warning(self.main.window, 'Erro', f'Falha ao criar pergunta: {erro}')
            return

        QMessageBox.information(self.main.window, 'Sucesso', 'Pergunta adicionada com sucesso.')
        self.main.ir_para(self.main.window.pg_editarperguntas)

    def _selecionar_pergunta(self, item):

        self._pergunta_selecionada = item.text()
        self._pergunta_id = item.data(Qt.UserRole)

        self._mostrar_botoes_acao()

    def _esconder_botoes_exclusao(self):

        w = self.main.window

        if hasattr(w, 'btn_editar'):
            w.btn_editar.setVisible(False)
        if hasattr(w, 'btn_excluir'):
            w.btn_excluir.setVisible(False)

        if hasattr(w, 'btn_confirmar_exclusao'):
            w.btn_confirmar_exclusao.setVisible(False)
        if hasattr(w, 'btn_negar_exclusao'):
            w.btn_negar_exclusao.setVisible(False)
        if hasattr(w, 'lbl_alt1_editarpergunta_3'):
            w.lbl_alt1_editarpergunta_3.setVisible(False)

    def _mostrar_botoes_acao(self):
        w = self.main.window

        if hasattr(w, 'btn_editar'):
            w.btn_editar.setVisible(True)
        if hasattr(w, 'btn_excluir'):
            w.btn_excluir.setVisible(True)

        if hasattr(w, 'btn_confirmar_exclusao'):
            w.btn_confirmar_exclusao.setVisible(False)
        if hasattr(w, 'btn_negar_exclusao'):
            w.btn_negar_exclusao.setVisible(False)
        if hasattr(w, 'lbl_alt1_editarpergunta_3'):
            w.lbl_alt1_editarpergunta_3.setVisible(False)

    def _filtrar_detalhe(self):
        w = self.main.window

        filtro = w.comboBox_turma3_2.currentText()

        filtro_map = {
            "Todas": None,
            "Fácil": 1,
            "Médio": 2,
            "Difícil": 3
        }

        id_nivel = filtro_map.get(filtro)

        w.lista_alunos3_2.clear()

        perguntas = listar_perguntas(id_nivel)

        for pergunta in perguntas:
            item_text = f"[{pergunta['nome_nivel']}] {pergunta['enunciado']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, pergunta['id_pergunta'])
            w.lista_alunos3_2.addItem(item)

        self._esconder_botoes_exclusao()

    def _filtrar_relatorio_turmas(self):
        try:
            from app.services.jogo_service import buscar_desempenho_geral, buscar_ranking, buscar_alunos_por_turma, contar_acertos_nivel_aluno

            w = self.main.window

            # Mudar turma/nível volta o painel para a visão da turma.
            self._ver_painel_turma()
            if hasattr(w, 'lista_alunos3'):
                w.lista_alunos3.clearSelection()

            turma_selecionada = w.comboBox_turma3.currentText() if hasattr(w, 'comboBox_turma3') else ""
            nivel_texto = w.comboBox_modo2_2.currentText() if hasattr(w, 'comboBox_modo2_2') else ""

            nivel_map = {"Fácil": 1, "Médio": 2, "Difícil": 3}
            id_nivel = nivel_map.get(nivel_texto, 1)

            alunos = buscar_alunos_por_turma(turma_selecionada if turma_selecionada != "Todas" and turma_selecionada else None)

            # Lista para armazenar acertos de cada aluno (para calcular média)
            acertos_lista = []

            if hasattr(w, 'lista_alunos3'):
                w.lista_alunos3.clear()
                for aluno in alunos:
                    id_aluno = aluno.get('id_usuario')
                    nome = aluno.get('nome', 'N/A')
                    turma = aluno.get('turma', 'N/A')

                    acertos = contar_acertos_nivel_aluno(id_aluno, id_nivel)
                    acertos_lista.append(acertos)

                    texto = f"{nome} (Turma: {turma}) - {acertos} acertos"
                    item = QListWidgetItem(texto)
                    item.setData(1000, aluno)
                    item.setData(1001, id_nivel)
                    w.lista_alunos3.addItem(item)

            # Calcula estatísticas da turma baseado nos acertos
            if acertos_lista:
                media = sum(acertos_lista) / len(acertos_lista)
                menor_nota = min(acertos_lista)
                maior_nota = max(acertos_lista)
            else:
                media = 0
                menor_nota = 0
                maior_nota = 0

            if hasattr(w, 'lbl_mediaturma2'):
                w.lbl_mediaturma2.setText(f"{media:.1f}")

            if hasattr(w, 'lbl_menornota'):
                w.lbl_menornota.setText(f"{menor_nota:.1f}")

            if hasattr(w, 'lbl_maiornota'):
                w.lbl_maiornota.setText(f"{maior_nota:.1f}")

            if hasattr(w, 'lista_perguntascommenosacerto'):
                w.lista_perguntascommenosacerto.clear()

                dados_erro = buscar_desempenho_geral()
                if dados_erro:
                    for item in dados_erro[:10]:
                        enunciado = item.get('enunciado', 'Sem nome')[:50]
                        taxa_erro = item.get('taxa_erro', 0)
                        texto = f"{enunciado}... ({taxa_erro:.0f}%)"
                        list_item = QListWidgetItem(texto)
                        w.lista_perguntascommenosacerto.addItem(list_item)

        except Exception as exc:
            print(f"[ProfessorController] Erro ao filtrar relatório de turmas: {exc}")

    def _filtrar_ranking_geral(self):
        try:
            from app.services.jogo_service import buscar_ranking_alunos

            w = self.main.window

            turma = w.comboBox_turmas.currentText() if hasattr(w, 'comboBox_turmas') else "Todas"
            ranking = buscar_ranking_alunos(turma if turma != "Todas" else None)

            if not hasattr(w, 'tbl_rankinggeral'):
                return

            tabela = w.tbl_rankinggeral
            tabela.setColumnCount(4)
            tabela.setHorizontalHeaderLabels(["Posição", "Aluno", "Turma", "Pontuação"])
            tabela.horizontalHeader().setVisible(True)
            tabela.setRowCount(0)

            for idx, aluno in enumerate(ranking):
                tabela.insertRow(idx)
                tabela.setItem(idx, 0, criar_item_tabela(idx + 1))
                tabela.setItem(idx, 1, criar_item_tabela(aluno.get('nome', 'N/A')))
                tabela.setItem(idx, 2, criar_item_tabela(aluno.get('turma') or '-'))
                tabela.setItem(idx, 3, criar_item_tabela(aluno.get('pontuacao', 0)))

        except Exception as exc:
            print(f"[ProfessorController] Erro ao filtrar ranking geral: {exc}")

    def _preencher_relatorio_individual(self, dados_aluno):
        """Preenche o relatório individual do aluno (desempenho só no modo Desafio)."""
        try:
            from app.services.jogo_service import buscar_desempenho_aluno, buscar_ranking

            w = self.main.window

            id_usuario = dados_aluno.get('id_usuario')
            nome = dados_aluno.get('nome', 'N/A')
            turma = dados_aluno.get('turma', 'N/A')
            id_nivel = dados_aluno.get('id_nivel', 1) if isinstance(dados_aluno, dict) and 'id_nivel' in dados_aluno else 1

            if hasattr(w, 'lbl_nome_aluno'):
                w.lbl_nome_aluno.setText(f"Aluno: {nome}")

            if hasattr(w, 'lbl_turma_aluno'):
                w.lbl_turma_aluno.setText(f"Turma: {turma}")

            if id_usuario:
                desempenho = buscar_desempenho_aluno(id_usuario)
                
                acertos = 0
                taxa_acerto = 0.0
                tempo_medio = 0.0
                taxa_dicas = 0.0
                nivel_desbloqueado = "Fácil"
                comparacao = "Sem dados"

                if desempenho:
                    total_perguntas = len(desempenho)
                    acertos = sum(1 for d in desempenho if d.get('correta'))
                    taxa_acerto = (acertos / total_perguntas * 100) if total_perguntas > 0 else 0

                    tempos = [d.get('tempo_resposta_seg', 0) for d in desempenho if d.get('tempo_resposta_seg')]
                    tempo_medio = sum(tempos) / len(tempos) if tempos else 0

                    total_dicas = sum(1 for d in desempenho if d.get('usou_dica'))
                    taxa_dicas = (total_dicas / total_perguntas * 100) if total_perguntas > 0 else 0

                    nivel_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
                    nivel_desbloqueado = nivel_map.get(id_nivel, "Fácil")

                    ranking = buscar_ranking(id_nivel, limite=100)
                    if ranking:
                        pontos_aluno = dados_aluno.get('melhor_pontuacao', 0)
                        media_geral = sum(r.get('melhor_pontuacao', 0) for r in ranking) / len(ranking)
                        comparacao = "Acima da média" if pontos_aluno >= media_geral else "Abaixo da média"
                else:
                    comparacao = "Sem dados em modo desafio"

                if hasattr(w, 'lbl_acertos'):
                    w.lbl_acertos.setText(f"{acertos}")

                if hasattr(w, 'lbl_taxa_acerto'):
                    w.lbl_taxa_acerto.setText(f"{taxa_acerto:.1f}%")

                if hasattr(w, 'lbl_tempo_medio'):
                    w.lbl_tempo_medio.setText(f"{tempo_medio:.1f}s")

                if hasattr(w, 'lbl_uso_dicas'):
                    w.lbl_uso_dicas.setText(f"{taxa_dicas:.1f}%")

                if hasattr(w, 'lbl_nivel_desbloqueado'):
                    w.lbl_nivel_desbloqueado.setText(f"{nivel_desbloqueado}")

                if hasattr(w, 'lbl_comparacao_media'):
                    w.lbl_comparacao_media.setText(comparacao)

                if hasattr(w, 'tbl_desempenho') and desempenho:
                    tabela = w.tbl_desempenho
                    tabela.setRowCount(0)

                    for idx, item in enumerate(desempenho[-10:]):
                        tabela.insertRow(idx)

                        enunciado = item.get('enunciado', 'N/A')[:50]
                        correta = "✓" if item.get('correta') else "✗"
                        tempo = f"{item.get('tempo_resposta_seg', 0):.1f}s"

                        tabela.setItem(idx, 0, QTableWidgetItem(enunciado))
                        tabela.setItem(idx, 1, QTableWidgetItem(correta))
                        tabela.setItem(idx, 2, QTableWidgetItem(tempo))

        except Exception as exc:
            print(f"[ProfessorController] Erro ao preencher relatório individual: {exc}")

