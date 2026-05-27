# =========================================================
# controllers/question_controller.py
# Loop completo: questão → timer → resposta → feedback → gabarito
# Suporta as 3 variantes de página de questão do .ui:
#   pg_questao / pg_questao_2 / pg_questao_3  (sufixos '', '_2', '_3')
# =========================================================
import time, random
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from services.jogo_service import (
    Pergunta, carregar_perguntas, criar_sessao,
    registrar_resposta, registrar_uso_dica,
    finalizar_sessao, atualizar_ranking, NIVEL,
)

TEMPO_SEG      = 60
PONTOS_ACERTO  = 10

# Estilo dos botões de alternativa
_ESTILO_NORMAL  = "background-color:white;color:#222;border:2px solid #921913;border-radius:25px;padding:0 18px"
_ESTILO_CERTO   = "background-color:#4caf50;color:white;border:none;border-radius:25px;padding:0 18px"
_ESTILO_ERRADO  = "background-color:#e53935;color:white;border:none;border-radius:25px;padding:0 18px"
_ESTILO_CINZA   = "background-color:#ccc;color:#888;border:2px solid #ccc;border-radius:25px;padding:0 18px"


class QuestionController:
    def __init__(self, main):
        self.main = main
        w = main.window

        # Estado
        self._perguntas: list[Pergunta] = []
        self._idx            = 0
        self._id_sessao      = None
        self._pontuacao      = 0
        self._acertos        = 0
        self._penalizacao    = 0
        self._eliminadas: set[int] = set()
        self._tempo_inicio   = 0.0
        self._dificuldade    = "facil"
        self._sufixo         = ""   # '', '_2' ou '_3' — página ativa

        # Timer
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._seg_restantes = TEMPO_SEG

        # Botões de modo
        self._liga(w, 'btn_facil',   lambda: self.iniciar("facil"))
        self._liga(w, 'btn_medio',   lambda: self.iniciar("medio"))
        self._liga(w, 'btn_dificil', lambda: self.iniciar("dificil"))
        self._liga(w, 'btn_shuffle', lambda: self.iniciar("aleatorio"))

        # Botões de alternativa (todas as variantes de página)
        for suf in ('', '_2', '_3'):
            for letra, idx in (('A',0),('B',1),('C',2),('D',3)):
                btn = getattr(w, f'btn_alt{letra}{suf}', None)
                if btn:
                    btn.clicked.connect(
                        (lambda i=idx, s=suf: lambda: self._responder(i, s))()
                    )
            # Dicas
            dica_exp = getattr(w, f'btn_dicaexp{suf}', None)
            eliminar = getattr(w, f'btn_eliminar{suf}', None)
            if dica_exp:
                dica_exp.clicked.connect((lambda s=suf: lambda: self._dica_texto(s))())
            if eliminar:
                eliminar.clicked.connect((lambda s=suf: lambda: self._dica_eliminacao(s))())

        # Feedback / gabarito
        self._liga(w, 'btn_gabarito',       self._ir_gabarito)
        self._liga(w, 'btn_voltarmodos3',   lambda: main.ir_para(w.pg_modos))
        self._liga(w, 'btn_voltarmodos3_2', lambda: main.ir_para(w.pg_modos))

    # --------------------------------------------------
    @staticmethod
    def _liga(w, nome, slot):
        btn = getattr(w, nome, None)
        if btn:
            btn.clicked.connect(slot)

    def _w(self, nome):
        return getattr(self.main.window, nome + self._sufixo, None)

    # --------------------------------------------------
    def iniciar(self, dificuldade: str):
        if not self.main.usuario_logado:
            QMessageBox.warning(self.main.window, "Atenção", "Faça login primeiro.")
            return

        perguntas = carregar_perguntas(dificuldade)
        if not perguntas:
            QMessageBox.warning(self.main.window, "Sem perguntas",
                                "Nenhuma pergunta cadastrada para este modo.")
            return

        self._dificuldade = dificuldade
        self._perguntas   = perguntas
        self._idx         = 0
        self._pontuacao   = 0
        self._acertos     = 0
        id_nivel          = NIVEL.get(dificuldade, 1)
        self._id_sessao   = criar_sessao(
            self.main.usuario_logado["id_usuario"], id_nivel)

        # Escolhe a variante de página pelo nível
        mapa = {"facil": "", "medio": "_2", "dificil": "_3", "aleatorio": ""}
        self._sufixo = mapa.get(dificuldade, "")
        pagina = getattr(self.main.window, f'pg_questao{self._sufixo}',
                         self.main.window.pg_questao)
        self.main.ir_para(pagina)
        self._exibir()

    # --------------------------------------------------
    def _exibir(self):
        w = self.main.window
        p = self._perguntas[self._idx]
        self._penalizacao = 0
        self._eliminadas  = set()
        self._tempo_inicio = time.time()

        # Enunciado
        lbl = self._w('lbl_pergunta')
        if lbl:
            lbl.setText(p.enunciado)

        # Alternativas
        for i, letra in enumerate(('A','B','C','D')):
            btn = self._w(f'btn_alt{letra}')
            if btn:
                if i < len(p.alternativas):
                    btn.setText(p.alternativas[i].texto)
                    btn.setEnabled(True)
                    btn.setVisible(True)
                    btn.setStyleSheet(_ESTILO_NORMAL)
                else:
                    btn.setVisible(False)

        # Esconde dica
        dica_lbl = self._w('txt_dica')
        if dica_lbl:
            dica_lbl.setVisible(False)
            dica_lbl.clear()

        # Habilita botões de dica
        btn_dica = self._w('btn_dicaexp')
        btn_elim = self._w('btn_eliminar')
        if btn_dica: btn_dica.setEnabled(p.dica_texto() is not None)
        if btn_elim: btn_elim.setEnabled(p.dica_eliminacao() is not None)

        # Timer
        self._seg_restantes = TEMPO_SEG
        lbl_timer = self._w('lbl_timer')
        if lbl_timer:
            lbl_timer.setText(str(self._seg_restantes))
        self._timer.start()

    # --------------------------------------------------
    def _tick(self):
        self._seg_restantes -= 1
        lbl = self._w('lbl_timer')
        if lbl:
            lbl.setText(str(self._seg_restantes))
        if self._seg_restantes <= 0:
            self._timer.stop()
            self._mostrar_feedback(acertou=False, timeout=True)

    # --------------------------------------------------
    def _responder(self, idx: int, sufixo: str):
        # Ignora clique se não for a página ativa
        if sufixo != self._sufixo:
            return
        if idx in self._eliminadas:
            return
        self._timer.stop()
        tempo = int(time.time() - self._tempo_inicio)

        p = self._perguntas[self._idx]
        alt = p.alternativa_por_indice(idx)
        if not alt:
            return

        acertou = alt.correta
        if self._id_sessao:
            registrar_resposta(self._id_sessao, p, alt, acertou, tempo)

        if acertou:
            pts = max(0, PONTOS_ACERTO - self._penalizacao)
            self._pontuacao += pts
            self._acertos   += 1
            self._cor_btn(idx, _ESTILO_CERTO)
        else:
            self._cor_btn(idx, _ESTILO_ERRADO)
            certa = p.alternativa_correta()
            if certa:
                self._cor_btn(p.alternativas.index(certa), _ESTILO_CERTO)

        for i in range(4):
            btn = self._w(f'btn_alt{"ABCD"[i]}')
            if btn: btn.setEnabled(False)

        self._mostrar_feedback(acertou, timeout=False)

    def _cor_btn(self, idx: int, estilo: str):
        btn = self._w(f'btn_alt{"ABCD"[idx]}')
        if btn:
            btn.setStyleSheet(estilo)

    # --------------------------------------------------
    def _mostrar_feedback(self, acertou: bool, timeout: bool):
        p = self._perguntas[self._idx]
        if timeout:
            msg = "⏰ Tempo esgotado!"
        elif acertou:
            msg = f"✅ Correto! +{max(0, PONTOS_ACERTO - self._penalizacao)} pts"
        else:
            certa = p.alternativa_correta()
            msg = f"❌ Errado! Certa: {certa.texto if certa else '?'}"

        lbl = self._w('txt_dica')
        if lbl:
            lbl.setText(msg)
            lbl.setVisible(True)

        # Avança automaticamente após 2 s
        QTimer.singleShot(2000, self._proxima)

    def _proxima(self):
        self._idx += 1
        if self._idx < len(self._perguntas):
            self._exibir()
        else:
            self._encerrar()

    # --------------------------------------------------
    def _encerrar(self):
        if self._id_sessao:
            id_nivel = NIVEL.get(self._dificuldade, 1)
            finalizar_sessao(self._id_sessao, self._pontuacao)
            atualizar_ranking(
                self.main.usuario_logado["id_usuario"],
                id_nivel, self._pontuacao)

        w = self.main.window
        # Preenche feedback
        if hasattr(w, 'lbl_acertos_feedback'):
            total = len(self._perguntas)
            taxa  = round(self._acertos * 100 / total, 1) if total else 0
            w.lbl_acertos_feedback.setText(f"{self._acertos}/{total} ({taxa}%)")
        if hasattr(w, 'lbl_nivel_feedback'):
            nomes = {1:"Fácil", 2:"Médio", 3:"Difícil"}
            w.lbl_nivel_feedback.setText(
                nomes.get(NIVEL.get(self._dificuldade, 1), self._dificuldade)
            )

        self.main.ir_para(w.pg_feedback)

    def _ir_gabarito(self):
        self.main.ir_para(self.main.window.pg_gabarito)

    # --------------------------------------------------
    def _dica_texto(self, sufixo: str):
        if sufixo != self._sufixo:
            return
        p = self._perguntas[self._idx]
        d = p.dica_texto()
        if not d:
            return
        self._penalizacao += d.penalizacao_pontos
        if self._id_sessao:
            registrar_uso_dica(self._id_sessao, p, d)
        lbl = self._w('txt_dica')
        if lbl:
            lbl.setText(f"💡 {d.conteudo}")
            lbl.setVisible(True)
        btn = self._w('btn_dicaexp')
        if btn: btn.setEnabled(False)

    def _dica_eliminacao(self, sufixo: str):
        if sufixo != self._sufixo:
            return
        p = self._perguntas[self._idx]
        d = p.dica_eliminacao()
        if not d:
            return
        self._penalizacao += d.penalizacao_pontos
        if self._id_sessao:
            registrar_uso_dica(self._id_sessao, p, d)

        erradas = [i for i, a in enumerate(p.alternativas)
                   if not a.correta and i not in self._eliminadas]
        random.shuffle(erradas)
        for i in erradas[:2]:
            self._eliminadas.add(i)
            self._cor_btn(i, _ESTILO_CINZA)
            btn = self._w(f'btn_alt{"ABCD"[i]}')
            if btn: btn.setEnabled(False)

        btn = self._w('btn_eliminar')
        if btn: btn.setEnabled(False)
