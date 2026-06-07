# Explicando tudo — QuimicLab

> Guia para quem está chegando agora no projeto. A ideia é que, lendo este
> documento, você entenda **o que cada parte do código faz**, **como elas se
> conversam** e **onde mexer** quando precisar mudar algo. Não precisa ser
> expert em Python nem em Qt — vou explicando os conceitos no caminho.

---

## 1. O que é o QuimicLab

O QuimicLab é um **jogo de perguntas e respostas de química** (estilo quiz) para
uso em sala de aula, com dois tipos de usuário:

- **Aluno** — joga os quizzes, ganha pontos, sobe de nível.
- **Professor** — cadastra/edita perguntas e acompanha o desempenho dos alunos
  (relatórios e rankings).

A interface é feita com **PySide6** (a versão oficial do Qt para Python — é uma
biblioteca para criar janelas, botões, telas etc.). Os dados ficam num banco
**MySQL**.

---

## 2. Como rodar o projeto

1. Ter o **MySQL** rodando e o banco `quimic_lab` criado (veja `Back/codigo.sql`).
2. Instalar as dependências: `pip install -r requirements.txt`.
3. Rodar: `python main.py`.

> ⚠️ Se o jogo abrir mas disser "Nenhuma pergunta encontrada", quase sempre é o
> **MySQL desligado** ou o **banco sem perguntas cadastradas**.

---

## 3. A grande ideia: o código é dividido em CAMADAS

Esse é **o conceito mais importante** para entender o projeto. Em vez de jogar
tudo num arquivo só, o código é separado por responsabilidade. Cada camada só
conversa com a vizinha:

```
   VOCÊ (usuário)
        │ clica num botão
        ▼
┌─────────────────────┐
│   UI  (.ui)         │  As telas desenhadas no Qt Designer. Só aparência.
│  front_viewer.ui    │  Botões, caixas de texto, labels...
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   CONTROLLERS       │  "O que acontece quando clico?" Pegam o texto digitado,
│  app/controllers/   │  validam, decidem para qual tela ir, chamam os services.
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   SERVICES          │  A "ponte". Traduzem o que a tela quer para o que o
│  app/services/      │  backend entende (e vice-versa). Tratam erros.
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   BACK  (backend)   │  Conversa de verdade com o banco: SQL, login,
│  Back/              │  carregar perguntas, salvar respostas...
└─────────────────────┘
        │
        ▼
   🗄️ Banco MySQL
```

**Por que isso é bom?** Se um dia o banco mudar, você só mexe na camada `Back/`.
Se a tela mudar, você mexe só no controller. As partes não ficam "grudadas".

---

## 4. O caminho de uma ação (exemplo: aluno faz login)

Acompanhe um clique do começo ao fim — entender **um** fluxo inteiro vale mais
que decorar nomes de arquivos:

1. **Tela**: o aluno digita e-mail/senha e clica em "Entrar".
2. **Controller** [auth_controller.py](app/controllers/auth_controller.py): o botão
   está conectado ao método `_entrar_aluno`. Ele:
   - lê o que foi digitado (`w.input_loginaluno.text()`),
   - confere se não está vazio,
   - chama o **service** `login_aluno(...)`.
3. **Service** [auth_service.py](app/services/auth_service.py): a função
   `login_aluno` chama o **backend** `BackAluno.login(...)`.
4. **Back** [aluno.py](Back/aluno.py): faz o `SELECT` no MySQL procurando o usuário.
5. A resposta **volta subindo** pelas mesmas camadas:
   - deu certo → o controller guarda o usuário em `self.main.usuario_logado` e
     navega para a tela do jogo;
   - deu errado → o controller mostra um aviso na tela.

> 💡 **Guarde essa imagem**: clique → controller → service → back → banco, e a
> resposta volta pelo mesmo caminho. Quase tudo no sistema segue esse trajeto.

---

## 5. Conceitos do Qt/PySide6 que aparecem o tempo todo

Antes de entrar arquivo por arquivo, três ideias do Qt que você **precisa**
reconhecer, senão o código parece mágica:

### a) `window` e os widgets
`window` é a janela carregada do arquivo `.ui`. Tudo que foi desenhado no Qt
Designer vira um atributo dela pelo **nome** (`objectName`). Ex.: um botão
chamado `btn_entraraluno` vira `window.btn_entraraluno`. No código você verá
muito `w = main.window` para encurtar.

### b) Sinais e slots (signals/slots) — "quando acontecer X, faça Y"
Botões emitem **sinais** (ex.: `.clicked`). A gente **conecta** esse sinal a uma
função (o "slot"):

```python
w.btn_entraraluno.clicked.connect(self._entrar_aluno)
```

Leia como: *"quando clicarem em btn_entraraluno, chame _entrar_aluno"*.

Quando precisa passar um argumento, usa-se `lambda`:

```python
w.btn_soualuno.clicked.connect(lambda: ir(w.pg_loginaluno))
```

O `lambda` é uma mini-função sem nome; aqui ela serve só para "segurar" o
argumento `w.pg_loginaluno` até o clique acontecer.

### c) `QStackedWidget` — as telas são um baralho de cartas
Todas as telas vivem dentro de um `stack` (um `QStackedWidget`). Só **uma** fica
visível por vez, como um baralho onde você vê só a carta de cima. Trocar de tela
= mostrar outra carta. Isso é feito pelo `ir_para` (ver seção 6).

---

## 6. Passeio pelos arquivos

### `main.py` (raiz) — o ponto de partida
[main.py](main.py) é onde tudo começa. Ele:
1. cria a aplicação Qt,
2. carrega a interface (`carregar_ui`),
3. cria a classe `Main`, que é o **centro do sistema**.

A classe `Main` guarda a `window`, o `usuario_logado` e **instancia todos os
controllers**. Detalhe importante que está comentado no código:
- o `NavigationController` é criado **primeiro**, porque os outros usam o atalho
  `self.ir_para` que vem dele;
- o `AnimationController` é criado **por último**, porque ele "varre" todos os
  botões já existentes para aplicar animação.

> 🔑 `self.main` aparece em **todo** controller. É a referência ao centro do
> sistema. Por isso um controller consegue, por exemplo, ler `self.main.usuario_logado`
> ou navegar com `self.main.ir_para(...)`.

### `app/controllers/` — a lógica de cada parte da tela

| Arquivo | Cuida de... |
|---|---|
| [navigation_controller.py](app/controllers/navigation_controller.py) | Trocar de tela (`ir_para`) |
| [auth_controller.py](app/controllers/auth_controller.py) | Login, cadastro, troca de senha, **olhinho da senha**, aceite dos termos |
| [question_controller.py](app/controllers/question_controller.py) | O jogo em si: perguntas, respostas, pontos, dica, timer, gabarito |
| [professor_controller.py](app/controllers/professor_controller.py) | Área do professor: relatórios e rankings |
| [editor_controller.py](app/controllers/editor_controller.py) | Formulário de criar/editar pergunta |
| [ranking_controller.py](app/controllers/ranking_controller.py) | Vazio de propósito (o ProfessorController faz o ranking) |
| [animation_controller.py](app/controllers/animation_controller.py) | Animações dos botões (bounce + hover) |

#### A navegação (`ir_para`)
Em [navigation_controller.py](app/controllers/navigation_controller.py), o método
`ir_para(pagina)` simplesmente manda o `stack` mostrar aquela tela. É a função
mais usada do sistema — toda troca de tela passa por ela.

### `app/services/` — a ponte com o backend

| Arquivo | Faz... |
|---|---|
| [auth_service.py](app/services/auth_service.py) | Login/cadastro de aluno e professor |
| [jogo_service.py](app/services/jogo_service.py) | Carregar perguntas, criar/finalizar sessão, registrar respostas, rankings, desbloqueio de nível |
| [pergunta_service.py](app/services/pergunta_service.py) | CRUD de perguntas (criar, listar, obter, atualizar, deletar) |
| [ranking_service.py](app/services/ranking_service.py) | Vazio — reservado para o futuro |

> 📐 **Padrão de retorno (decore isto)**: quase toda função de service/back
> devolve uma **dupla** `(resultado, erro)`:
> - deu certo → `(dados, None)`
> - deu errado → `(None, "mensagem de erro")`
>
> Por isso você vê tanto `usuario, erro = login_aluno(...)`. O controller checa o
> `erro`: se tiver mensagem, mostra um aviso; se for `None`, segue em frente.

### `Back/` — o backend (banco de dados)

| Arquivo | Faz... |
|---|---|
| [Conectar_Banco.py](Back/Conectar_Banco.py) | Abre a conexão com o MySQL |
| [aluno.py](Back/aluno.py) | Login/cadastro de aluno |
| [professor.py](Back/professor.py) | Login/cadastro de professor |
| [Perguntas.py](Back/Perguntas.py) | A classe `Pergunta` (enunciado, alternativas, dicas) |
| [Jogo.py](Back/Jogo.py) | Toda a lógica do jogo no banco (perguntas, sessão, ranking) |

Um padrão que se repete em todo o `Back/`: cada operação **abre uma conexão,
faz o SQL e fecha a conexão** (o `try/finally` garante que sempre fecha, mesmo
se der erro). Isso evita conexões penduradas.

### `app/utils/` — ferramentas reaproveitadas

| Arquivo | Faz... |
|---|---|
| [ui_loader.py](app/utils/ui_loader.py) | Carrega o `.ui` e conserta layout/imagens/ícones |
| [scaler.py](app/utils/scaler.py) | **Responsividade**: redimensiona a tela para o monitor |
| [helpers.py](app/utils/helpers.py) | Estilos prontos de tabela/lista, animação de fade, cursor de mão |
| [imagem_util.py](app/utils/imagem_util.py) | Converte imagem do banco (bytes) para mostrar na tela |

---

## 7. Recursos diferenciados (o "tempero" do projeto)

Aqui estão as partes que fogem do feijão-com-arroz e que costumam gerar
"como é que isso funciona?". Vale entender com calma.

### 🔒 O "olhinho" da senha (mostrar/ocultar)
**Onde:** [auth_controller.py](app/controllers/auth_controller.py), métodos
`_configurar_senha` e `_icone_olho`.

Por padrão, um campo de senha esconde o texto com bolinhas (`•••`). Isso é o
`EchoMode.Password`. O diferencial aqui é o **botãozinho de olho** que deixa
mostrar/ocultar o que foi digitado. Como ele foi feito:

1. **O ícone é desenhado na mão**, não é uma imagem nem um emoji. O método
   `_icone_olho` usa o `QPainter` (uma "caneta" do Qt) para desenhar:
   - **olho aberto** = um contorno oval + uma pupila (senha visível);
   - **olho fechado** = o mesmo contorno com um traço diagonal por cima (senha oculta).
2. **O botão é colocado por cima do campo**, encostado na direita
   (`_configurar_senha` calcula a posição). Para o texto não passar por baixo do
   olho, o campo ganha uma margem à direita (`setTextMargins`).
3. **Clicar alterna** entre `EchoMode.Password` e `EchoMode.Normal` e troca o
   ícone — é a função interna `alternar()`.

Esse mesmo tratamento é aplicado a **todos** os campos de senha do sistema
(login, cadastro e troca), com aquele `for` no `__init__` que percorre os nomes
dos campos.

### ✅ Marcar a alternativa correta (botão verde)
**Onde:** [editor_controller.py](app/controllers/editor_controller.py),
`_criar_marcadores_corretas` e `_atualizar_marcadores`.

Quando o professor cadastra uma pergunta, ele precisa dizer **qual** alternativa
é a certa. Para isso, cada alternativa ganha um botão **"Correta"** ao lado.
Clicar nele: marca aquela como correta (o campo fica **verde** e o botão vira
"✓ Correta") e desmarca as outras. A letra escolhida fica guardada em
`_alt_correta_2` (edição) ou `_alt_correta_3` (adição).

### ✨ Botões que "pulam" e mudam de cor (animação)
**Onde:** [animation_controller.py](app/controllers/animation_controller.py).

- `aplicar_bounce`: ao clicar, o botão cresce e encolhe rapidinho (efeito de
  "pulo"), usando `QPropertyAnimation` sobre a geometria do botão.
- `aplicar_hover`: ao passar o mouse, o fundo muda de cor. O truque esperto é que
  ele **lê a cor atual** do botão no CSS e escolhe um tom de hover combinando
  (mapa `hover_map`).

O `AnimationController` aplica isso automaticamente em **todos** os botões da
janela (o `for ... findChildren(QPushButton)` no `setup`).

### 📐 A tela se ajusta ao monitor (responsividade)
**Onde:** [scaler.py](app/utils/scaler.py).

A interface foi desenhada pensando numa tela de **1920×1080**. Em telas maiores
ou menores, tudo seria desproporcional. O `scaler` resolve isso: ele calcula a
proporção entre o monitor e o tamanho de design (`fx`, `fy`) e redimensiona
**posição, tamanho e fonte** de cada widget. O detalhe fino está em
`_escalar_fonte`: a fonte é escalada tanto pelo `pointSize` quanto pelo
`font-size: Npx` do CSS — senão o texto "estouraria" as caixas.

### 🖼️ Imagens nas perguntas (BLOB ↔ base64)
**Onde:** [imagem_util.py](app/utils/imagem_util.py) e
[pergunta_service.py](app/services/pergunta_service.py).

Uma pergunta pode ter imagem. No banco ela é guardada como **BLOB** (um monte de
bytes). Na hora de mostrar, `pixmap_de_blob` converte esses bytes num `QPixmap`
(o formato de imagem do Qt). Quando o professor escolhe uma imagem do computador,
o caminho inverso acontece: vira **base64** (texto) para trafegar entre as
camadas e depois bytes para salvar no banco.

### 🎯 Regras de pontuação do jogo
**Onde:** [question_controller.py](app/controllers/question_controller.py).

Três regras não óbvias, todas comentadas no código:

1. **Pontos por nível no Desafio**: acertar no modo Desafio vale conforme o nível
   (Fácil=100, Médio=200, Difícil=300 — a constante `PONTOS_DESAFIO`). Fora do
   Desafio, vale 10 por acerto.
2. **Dica/eliminação cortam pela metade**: se o aluno usou ajuda e acertou no
   Desafio, ganha metade dos pontos.
3. **Não pontuar a mesma pergunta duas vezes**: a função
   `ja_acertou_pergunta_nesta_sessao` checa isso. ⚠️ **Atenção**: essa checagem
   roda **antes** de gravar a resposta atual — se gravasse antes, ela veria a
   própria resposta e zeraria os pontos (isso já foi um bug; está explicado no
   comentário do `_responder`).

### 🔓 Desbloqueio de nível
**Onde:** `verificar_desbloqueio_nivel` em
[jogo_service.py](app/services/jogo_service.py). O aluno precisa de **10 acertos**
num nível para liberar o próximo. A função devolve um dicionário com
`desbloqueado` (sim/não), quantos acertos faltam e uma mensagem pronta.

---

## 8. Dicas para quando você for mexer

- **Quer mudar o que um botão faz?** Procure o `objectName` dele (ex.:
  `btn_entraraluno`) no controller correspondente — a conexão `.clicked.connect`
  diz qual método é chamado.
- **Quer mudar uma regra do jogo (pontos, tempo)?** Olhe as constantes no topo de
  [question_controller.py](app/controllers/question_controller.py)
  (`TEMPO_POR_QUESTAO`, `PONTOS_DESAFIO`).
- **Quer mudar como algo é salvo no banco?** É na camada `Back/` ou nos
  `services/` — **nunca** coloque SQL dentro de um controller.
- **Apareceu erro de tela inexistente** (`object has no attribute 'pg_...'`)?
  O nome da página no `.ui` mudou ou está errado no controller.
- Toda mudança de código deve ser registrada em
  [mudancas_claude.md](mudancas_claude.md).

---

## 9. Mini-glossário

| Termo | O que é |
|---|---|
| **Widget** | Qualquer elemento de tela (botão, label, caixa de texto...) |
| **Signal / Slot** | "Evento" (clique) e a função que responde a ele |
| **`lambda`** | Mini-função sem nome, usada para passar argumentos numa conexão |
| **`QStackedWidget` (`stack`)** | O "baralho" de telas; só uma aparece por vez |
| **Controller** | Quem decide o que acontece numa parte da tela |
| **Service** | A ponte entre a tela e o backend |
| **BLOB** | Dados binários (ex.: imagem) guardados no banco |
| **base64** | Forma de representar bytes como texto |
| **CRUD** | Create, Read, Update, Delete (criar, ler, atualizar, deletar) |
| **Stub** | Versão "de mentira" de uma função, usada como placeholder |
