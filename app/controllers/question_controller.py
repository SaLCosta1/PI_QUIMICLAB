import random
from pathlib import Path

from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

from app.services.jogo_service import (
    carregar_perguntas,
    criar_sessao,
    registrar_resposta,
    registrar_uso_dica,
    finalizar_sessao,
    atualizar_ranking,
    NIVEL,
    NIVEL_NOME,
)
from app.utils.imagem_util import pixmap_de_blob, aplicar_pixmap_no_label

TEMPO_POR_QUESTAO = 120

# Pontos por acerto no modo Desafio, conforme o nível da pergunta
# (ver coluna `pontuacao_desafio` da tabela `nivel`): Fácil=100, Médio=200, Difícil=300.
PONTOS_DESAFIO = {1: 100, 2: 200, 3: 300}

_STYLE_ALT = """
QPushButton{
    background-color: white;
    border: 2px solid #921913;
    border-radius: 25px;
    color: black;
}

QPushButton:hover{
    background-color: #f0f0f0;
}
"""

class QuestionController:
    def __init__(self, main):
        self.main = main
        w = main.window
        ir = main.ir_para
        base = Path(__file__).resolve().parent.parent
        self._icone_dica = str(base / "assets" / "images" / "icone_dica.png")
        self._icone_lixo = str(base / "assets" / "images" / "icone_lixo.png")
        self._modo = "tradicional"
        self._dificuldade = "medio"
        self._perguntas = []
        self._indice = 0
        self._acertos = 0
        self._respostas = []
        self._sessao_id = None
        self._id_nivel = 1
        self._pontuacao = 0
        self._eliminadas = []
        self._dica_visivel = False
        self._ajuda_usada = False
        self._timer = QTimer()
        self._tempo_restante = TEMPO_POR_QUESTAO
        w.btn_voltar_tipojogo.clicked.connect(
            self._voltar_para_perfil
        )
        w.btn_tradicional.clicked.connect(
            lambda: self._escolher_modo("tradicional")
        )
        w.btn_desafio.clicked.connect(
            lambda: self._iniciar_jogo("desafio")
        )
        w.btn_voltarperfil4.clicked.connect(
            lambda: ir(w.pg_tipo_jogo)
        )
        w.btn_facil.clicked.connect(
            lambda: self._iniciar_jogo("facil")
        )
        w.btn_medio.clicked.connect(
            lambda: self._iniciar_jogo("medio")
        )
        w.btn_dificil.clicked.connect(
            lambda: self._iniciar_jogo("dificil")
        )
        w.btn_altA.clicked.connect(lambda: self._responder("A"))
        w.btn_altB.clicked.connect(lambda: self._responder("B"))
        w.btn_altC.clicked.connect(lambda: self._responder("C"))
        w.btn_altD.clicked.connect(lambda: self._responder("D"))
        w.btn_eliminar.clicked.connect(self._eliminar_alternativa)
        w.btn_dicaexp.clicked.connect(self._mostrar_dica)
        w.btn_gabarito.clicked.connect(self._ir_gabarito)
        w.btn_gabarito_2.clicked.connect(self._ir_gabarito)
        w.btn_voltarmodos3_2.clicked.connect(
            self._voltar_ao_inicio_pos_jogo
        )
        w.comboBox_escolherpergunta_2.currentIndexChanged.connect(
            self._mostrar_gabarito_questao
        )
        self._timer.timeout.connect(self._tick_timer)

    def _escolher_modo(self, modo):
        self._modo = modo
        self.main.ir_para(self.main.window.pg_modos)

    def _iniciar_jogo(self, dificuldade):
        if dificuldade == "desafio":
            self._modo = "desafio"
            self._dificuldade = "desafio"
            self._id_nivel = 1
        else:
            self._modo = "tradicional"
            self._dificuldade = dificuldade
            self._id_nivel = NIVEL.get(dificuldade, 1)
        if self.main.usuario_logado and self._id_nivel > 1 and dificuldade != "desafio":
            try:
                from app.services.jogo_service import verificar_desbloqueio_nivel
                info_desbloqueio = verificar_desbloqueio_nivel(
                    self.main.usuario_logado.get("id_usuario"),
                    self._id_nivel - 1
                )
                if not info_desbloqueio['desbloqueado']:
                    self._aviso(
                        "Nível Bloqueado\n\n" +
                        info_desbloqueio['mensagem']
                    )
                    return
            except Exception as exc:
                print(f"[QuestionController] Erro ao verificar desbloqueio: {exc}")
        self._perguntas = []
        self._indice = 0
        self._acertos = 0
        self._respostas = []
        self._pontuacao = 0
        self._eliminadas = []
        self._dica_visivel = False
        self._ajuda_usada = False
        self._sessao_id = None
        try:
            # Em desafio, carrega perguntas de TODOS os níveis (variado);
            # no tradicional, carrega apenas o nível escolhido.
            dificuldade_carregar = "desafio" if dificuldade == "desafio" else dificuldade
            self._perguntas = carregar_perguntas(dificuldade_carregar)
        except Exception as exc:
            print(f"[QuestionController] Erro ao carregar perguntas: {exc}")
            self._perguntas = []
        if not self._perguntas:
            nivel_txt = NIVEL_NOME.get(self._id_nivel, dificuldade)
            self._aviso(
                f"Nenhuma pergunta encontrada no nível {nivel_txt}.\n\n"
                "Verifique se o MySQL está rodando e se o professor "
                "cadastrou questões neste nível."
            )
            return
        if self.main.usuario_logado and self.main.usuario_logado.get("id_usuario"):
            try:
                self._sessao_id = criar_sessao(
                    self.main.usuario_logado["id_usuario"],
                    self._id_nivel,
                    self._modo,
                )
            except Exception as exc:
                print(f"[QuestionController] Erro ao criar sessão: {exc}")
                self._sessao_id = None
        self._mostrar_pergunta()

    def _mostrar_pergunta(self):
        if not self._perguntas or self._indice >= len(self._perguntas):
            return
        w = self.main.window
        pergunta = self._perguntas[self._indice]
        self._eliminadas = []
        self._dica_visivel = False
        self._ajuda_usada = False
        w.txt_dica.hide()
        w.txt_dica.clear()
        w.lbl_pergunta.setText(pergunta.enunciado)
        if self._modo == "desafio":
            w.lbl_infonivel.setText("Desafio")
        else:
            nome_nivel = NIVEL_NOME.get(pergunta.id_nivel, str(pergunta.id_nivel))
            w.lbl_infonivel.setText(f"Nível {nome_nivel}")
        self._exibir_imagem_pergunta(pergunta)
        alternativas = pergunta.alternativas
        textos = [
            a.get("texto", "") if isinstance(a, dict) else getattr(a, "texto", "")
            for a in alternativas
        ]
        w.btn_altA.setText(textos[0] if len(textos) > 0 else "")
        w.btn_altB.setText(textos[1] if len(textos) > 1 else "")
        w.btn_altC.setText(textos[2] if len(textos) > 2 else "")
        w.btn_altD.setText(textos[3] if len(textos) > 3 else "")
        for btn in (w.btn_altA, w.btn_altB, w.btn_altC, w.btn_altD):
            btn.setEnabled(True)
            btn.setStyleSheet(_STYLE_ALT)
        w.btn_dicaexp.show()
        w.btn_eliminar.show()
        self._timer.stop()
        self._tempo_restante = TEMPO_POR_QUESTAO
        w.lbl_timer.setText(str(self._tempo_restante))
        self._timer.start(1000)
        self.main.ir_para(w.pg_questao)

    def _exibir_imagem_pergunta(self, pergunta):
        w = self.main.window
        if not hasattr(w, "lbl_imagem"):
            return
        try:
            imagem = getattr(pergunta, "imagem", None)
            pix = pixmap_de_blob(imagem)
            aplicar_pixmap_no_label(w.lbl_imagem, pix)
        except Exception as exc:
            print(f"[QuestionController] Erro ao exibir imagem: {exc}")

    def _tick_timer(self):
        self._tempo_restante -= 1
        self.main.window.lbl_timer.setText(str(max(self._tempo_restante, 0)))
        if self._tempo_restante <= 0:
            self._timer.stop()
            self._aviso("O tempo acabou. A próxima pergunta será exibida.")
            if self._indice + 1 >= len(self._perguntas):
                self._finalizar_partida()
            else:
                self._indice += 1
                self._mostrar_pergunta()

    def _responder(self, letra):
        if not self._perguntas or self._indice >= len(self._perguntas):
            return
        pergunta = self._perguntas[self._indice]
        alternativa = pergunta.alternativa_por_letra(letra)
        if not alternativa:
            self._aviso("Selecione uma alternativa válida.")
            return
        correta = (
            alternativa.get("correta") in (1, True)
            if isinstance(alternativa, dict)
            else alternativa.correta in (1, True)
        )
        self._timer.stop()
        if correta:
            # Pontos do acerto: no Desafio valem conforme o nível da pergunta
            # (Fácil=100, Médio=200, Difícil=300); fora do Desafio, 10 por acerto.
            pontos = PONTOS_DESAFIO.get(pergunta.id_nivel, 100) if self._modo == "desafio" else 10
            # Dica ou eliminação no Desafio reduz a pontuação da pergunta pela metade
            # (ex.: Difícil 300 com dica = 150). Errar continua valendo 0.
            if self._modo == "desafio" and self._ajuda_usada:
                pontos = pontos // 2
            # Só pontua se ainda não tinha acertado esta pergunta nesta sessão.
            # A verificação roda ANTES de gravar a resposta (registro mais abaixo),
            # senão enxergaria a própria resposta atual e zeraria a pontuação.
            ja_pontuou = False
            if self._sessao_id:
                try:
                    from app.services.jogo_service import ja_acertou_pergunta_nesta_sessao
                    id_pergunta = pergunta.id_pergunta if hasattr(pergunta, 'id_pergunta') else pergunta.get('id_pergunta')
                    ja_pontuou = ja_acertou_pergunta_nesta_sessao(self._sessao_id, id_pergunta)
                except Exception as e:
                    print(f"[QuestionController] Erro ao verificar pergunta: {e}")
                    ja_pontuou = False
            if not ja_pontuou:
                self._pontuacao += pontos
            self._acertos += 1
        # Grava a resposta DEPOIS de pontuar: se gravarmos antes, a verificação de
        # "já acertou nesta sessão" (acima) enxerga a própria resposta recém-inserida
        # e a pontuação fica sempre zerada.
        try:
            registrar_resposta(
                self._sessao_id,
                pergunta,
                alternativa,
                correta,
                TEMPO_POR_QUESTAO - self._tempo_restante,
            )
        except Exception as exc:
            print(f"[QuestionController] Erro ao registrar resposta: {exc}")
        alt_id = (
            alternativa["id_alternativa"]
            if isinstance(alternativa, dict)
            else alternativa.id_alternativa
        )
        self._respostas.append({
            "pergunta": pergunta.id_pergunta,
            "alternativa": alt_id,
            "correta": correta,
            "enunciado": pergunta.enunciado,
        })
        if self._indice + 1 >= len(self._perguntas):
            self._finalizar_partida()
            return
        self._indice += 1
        self._mostrar_pergunta()

    def _mostrar_dica(self):
        if not self._perguntas or self._indice >= len(self._perguntas):
            return
        pergunta = self._perguntas[self._indice]
        dica = self._buscar_dica_texto(pergunta) or self._buscar_dica_eliminacao(pergunta)
        if not dica:
            self._aviso("Nenhuma dica disponível para esta pergunta.")
            return
        if self._ajuda_usada:
            self._aviso("Dica ou eliminar já foram usados nesta pergunta.")
            return
        self._dica_visivel = True
        w = self.main.window
        texto_dica = dica.get("conteudo") if isinstance(dica, dict) else dica.conteudo
        w.txt_dica.setText(texto_dica)
        w.txt_dica.show()
        self._ajuda_usada = True
        try:
            registrar_uso_dica(self._sessao_id, pergunta, dica)
        except Exception as exc:
            print(f"[QuestionController] Erro ao registrar dica: {exc}")

    def _eliminar_alternativa(self):
        if not self._perguntas or self._indice >= len(self._perguntas):
            return
        if self._ajuda_usada:
            self._aviso("Dica ou eliminar já foram usados nesta pergunta.")
            return
        pergunta = self._perguntas[self._indice]
        correta = pergunta.alternativa_correta()
        if not correta:
            self._aviso("Erro ao buscar resposta correta.")
            return
        correta_id = (
            correta.get("id_alternativa")
            if isinstance(correta, dict)
            else correta.id_alternativa
        )
        para_eliminar = [
            a for a in pergunta.alternativas
            if (
                a.get("id_alternativa") if isinstance(a, dict)
                else a.id_alternativa
            ) != correta_id
        ]
        self._eliminadas = [
            (
                a.get("id_alternativa") if isinstance(a, dict)
                else a.id_alternativa
            )
            for a in para_eliminar[:2]
        ]
        w = self.main.window
        for btn, alternativa in zip(
            (w.btn_altA, w.btn_altB, w.btn_altC, w.btn_altD),
            pergunta.alternativas,
        ):
            alt_id = (
                alternativa.get("id_alternativa")
                if isinstance(alternativa, dict)
                else alternativa.id_alternativa
            )
            if alt_id in self._eliminadas:
                btn.setEnabled(False)
        self._ajuda_usada = True

    def _finalizar_partida(self):
        self._timer.stop()
        if self._sessao_id is not None:
            try:
                finalizar_sessao(self._sessao_id, self._pontuacao)
            except Exception as exc:
                print(f"[QuestionController] Erro ao finalizar sessão: {exc}")
        if (
            self._modo == "desafio"
            and self.main.usuario_logado
            and self.main.usuario_logado.get("id_usuario")
        ):
            try:
                atualizar_ranking(
                    self.main.usuario_logado["id_usuario"],
                    self._id_nivel,
                    self._pontuacao,
                )
            except Exception as exc:
                print(f"[QuestionController] Erro ao atualizar ranking: {exc}")
        total = len(self._perguntas)
        w = self.main.window
        nivel_nome = NIVEL_NOME.get(self._id_nivel, str(self._id_nivel))
        if self._modo == "tradicional":
            w.lbl_modo.setText(f"Nível {nivel_nome}")
            w.lbl_acertos.setText(f"{self._acertos}/{total}")
            self.main.ir_para(w.pg_feedbacktradicional)
        else:
            w.lbl_modo_2.setText("Desafio")
            w.lbl_acertos_2.setText(f"{self._acertos}/{total}\n{self._pontuacao} pts")
            self.main.ir_para(w.pg_feedbackdesafio)

    def _ir_gabarito(self):
        w = self.main.window
        w.comboBox_escolherpergunta_2.blockSignals(True)
        w.comboBox_escolherpergunta_2.clear()
        for i in range(len(self._perguntas)):
            w.comboBox_escolherpergunta_2.addItem(f"Questão {i + 1}")
        w.comboBox_escolherpergunta_2.blockSignals(False)
        w.comboBox_escolherpergunta_2.setCurrentIndex(0)
        self._mostrar_gabarito_questao(0)
        self.main.ir_para(w.page_2)

    def _mostrar_gabarito_questao(self, index):
        if not self._perguntas or index < 0 or index >= len(self._perguntas):
            return
        w = self.main.window
        pergunta = self._perguntas[index]
        resposta = self._respostas[index] if index < len(self._respostas) else {}
        try:
            # Barra superior vira título do gabarito
            if hasattr(w, "lbl_titulo_gabarito_3"):
                w.lbl_titulo_gabarito_3.setText(
                    f"Gabarito — Questão {index + 1}/{len(self._perguntas)}"
                )
            # Enunciado + alternativas no card da esquerda (lista_enunciadopergunta_2)
            if hasattr(w, "lista_enunciadopergunta_2"):
                lista = w.lista_enunciadopergunta_2
                lista.setWordWrap(True)
                lista.clear()
                lista.addItem(pergunta.enunciado)
                letras = ["A", "B", "C", "D"]
                for i, alt in enumerate(pergunta.alternativas):
                    texto = (
                        alt.get("texto", "") if isinstance(alt, dict)
                        else getattr(alt, "texto", "")
                    )
                    if i < len(letras):
                        lista.addItem(f"{letras[i]}) {texto}")
        except Exception as exc:
            print(f"[QuestionController] Erro ao exibir enunciado: {exc}")
        nivel_nome = NIVEL_NOME.get(pergunta.id_nivel, str(pergunta.id_nivel))
        w.lbl_nivel2_5.setText(f"Nível {nivel_nome}")
        resposta_usuario = ""
        if "alternativa" in resposta:
            alt_id = resposta["alternativa"]
            for i, alt in enumerate(pergunta.alternativas):
                alt_id_pergunta = (
                    alt.get("id_alternativa")
                    if isinstance(alt, dict)
                    else getattr(alt, "id_alternativa", None)
                )
                if alt_id_pergunta == alt_id:
                    resposta_usuario = chr(65 + i)
                    break
        w.lbl_suaresposta_3.setText(resposta_usuario)
        resposta_correta = ""
        for i, alt in enumerate(pergunta.alternativas):
            correta = (
                alt.get("correta")
                if isinstance(alt, dict)
                else getattr(alt, "correta", None)
            )
            if correta in (1, True):
                resposta_correta = chr(65 + i)
                break
        w.lbl_gabarito_3.setText(resposta_correta)

    def _buscar_dica_texto(self, pergunta):
        if hasattr(pergunta, "dica_texto"):
            return pergunta.dica_texto()
        for dica in getattr(pergunta, "dicas", []):
            tipo = (
                dica.get("tipo")
                if isinstance(dica, dict)
                else getattr(dica, "tipo", None)
            )
            if tipo == "texto":
                return dica
        return None

    def _buscar_dica_eliminacao(self, pergunta):
        if hasattr(pergunta, "dica_eliminacao"):
            return pergunta.dica_eliminacao()
        for dica in getattr(pergunta, "dicas", []):
            tipo = (
                dica.get("tipo")
                if isinstance(dica, dict)
                else getattr(dica, "tipo", None)
            )
            if tipo == "eliminacao":
                return dica
        return None

    def _voltar_ao_inicio_pos_jogo(self):
        self.main.ir_para(self.main.window.pg_tipo_jogo)

    def _voltar_para_perfil(self):
        # Sai da área do aluno direto para a escolha aluno/professor,
        # sem retraçar a tela de login.
        self.main.usuario_logado = None
        self.main.ir_para(self.main.window.pg_perfil)

    def _aviso(self, texto):
        QMessageBox.warning(
            self.main.window,
            "Atenção",
            texto,
        )

    def _info(self, texto):
        QMessageBox.information(
            self.main.window,
            "Informação",
            texto,
        )
