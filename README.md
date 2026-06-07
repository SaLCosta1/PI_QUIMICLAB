# QuimicLab

Aplicação desktop educacional, em formato de quiz, para o estudo de materiais e
vidrarias de laboratório de Química. O sistema permite que alunos pratiquem por
meio de perguntas de múltipla escolha e que professores cadastrem questões e
acompanhem o desempenho das turmas.

Desenvolvido como Projeto Integrador para a ETEC Júlio de Mesquita.

---

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Regras do jogo](#regras-do-jogo)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e execução](#instalação-e-execução)
- [Configuração do banco de dados](#configuração-do-banco-de-dados)
- [Contas de teste](#contas-de-teste)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Arquitetura](#arquitetura)
- [Banco de dados](#banco-de-dados)
- [Solução de problemas](#solução-de-problemas)
- [Documentação adicional](#documentação-adicional)
- [Limitações conhecidas](#limitações-conhecidas)
- [Autores e orientação](#autores-e-orientação)
- [Licença](#licença)

---

## Visão geral

O QuimicLab tem dois perfis de usuário:

- **Aluno**: joga os quizzes, acumula pontos e progride entre os níveis de
  dificuldade.
- **Professor**: cadastra, edita e remove perguntas, além de consultar
  relatórios de desempenho e rankings.

A interface é construída com PySide6 (Qt para Python) e os dados são
persistidos em um banco MySQL.

---

## Funcionalidades

### Aluno

- Autenticação por e-mail institucional e senha.
- Dois modos de jogo: Tradicional (prática) e Desafio (pontuado, com ranking).
- Três níveis de dificuldade: Fácil, Médio e Difícil.
- Recursos de ajuda por questão: dica em texto ou eliminação de duas
  alternativas incorretas.
- Tempo limitado por questão, com cronômetro visível.
- Gabarito ao final da partida, com a resposta marcada e a correta.
- Progressão de níveis condicionada ao percentual de acerto.

### Professor

- Cadastro de perguntas com quatro alternativas, definição da alternativa
  correta, nível de dificuldade, imagem ilustrativa e dica (opcionais).
- Edição e exclusão (lógica) de perguntas existentes.
- Relatório de desempenho por aluno e por turma.
- Ranking de alunos e ranking de turmas.
- Identificação das perguntas com maior índice de erro.

---

## Regras do jogo

Estas são as regras efetivamente implementadas no código.

### Modos

| Modo | Como funciona | Pontuação | Ranking |
|------|---------------|-----------|---------|
| Tradicional | O aluno escolhe um nível (Fácil, Médio ou Difícil) e responde às perguntas daquele nível. | 10 pontos por acerto. | Não |
| Desafio | Perguntas de todos os níveis, em ordem variada. | Por nível da pergunta: Fácil = 100, Médio = 200, Difícil = 300. | Sim |

### Ajudas (por questão)

Cada pergunta admite **uma** ajuda, à escolha do aluno:

- **Dica**: exibe um texto de apoio.
- **Eliminar**: desabilita duas alternativas incorretas, restando a correta e
  uma incorreta.

No modo Desafio, usar qualquer ajuda e acertar a questão vale **metade** dos
pontos daquele nível. No modo Tradicional não há penalização.

### Tempo

Cada questão tem um limite de 120 segundos. Ao esgotar o tempo, a questão é
considerada não respondida e o jogo avança para a próxima.

### Progressão de níveis

No modo Tradicional, para acessar um nível (Médio ou Difícil) o aluno precisa
ter acertado pelo menos **60% das perguntas do nível anterior**. O percentual
considera as perguntas distintas acertadas em relação ao total de perguntas
ativas daquele nível. O valor é definido pela constante `PERCENTUAL_DESBLOQUEIO`
em `app/services/jogo_service.py`.

---

## Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Linguagem | Python 3.10 ou superior (testado com 3.13) |
| Interface gráfica | PySide6 (Qt for Python) |
| Banco de dados | MySQL |
| Controle de versão | Git |

Dependências Python (`requirements.txt`):

```
PySide6>=6.6,<7.0
python-dotenv
mysql-connector-python
```

> Observação: o código usa anotações de tipo no formato `int | None`,
> introduzido no Python 3.10. Versões anteriores não são compatíveis.

---

## Pré-requisitos

- Python 3.10 ou superior.
- MySQL instalado e em execução.
- Git (para clonar o repositório).

Para verificar as versões instaladas:

```bash
python --version
mysql --version
git --version
```

---

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/SaLCosta1/PI_QUIMICLAB.git
cd PI_QUIMICLAB
```

### 2. Criar e ativar o ambiente virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

O ambiente virtual isola as dependências do projeto das bibliotecas globais do
sistema.

### 3. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Consulte a seção [Configuração do banco de dados](#configuração-do-banco-de-dados).

### 5. Executar a aplicação

```bash
python main.py
```

A janela do QuimicLab será aberta em modo maximizado.

---

## Configuração do banco de dados

### 1. Criar o schema

O script de criação cria o banco `quimic_lab` e todas as tabelas. A partir do
terminal:

```bash
mysql -u root -p < Back/codigo.sql
```

Ou, já conectado ao MySQL:

```sql
source Back/codigo.sql;
```

> O arquivo `Back/diagrama_pi.sql` contém o mesmo schema. Caso o banco tenha
> sido criado em uma versão anterior (com colunas `imagem_url`), aplique
> `Back/migracao_imagem_blob.sql` para migrar as imagens para o formato atual.

### 2. Ajustar as credenciais de conexão

As credenciais ficam em `Back/Conectar_Banco.py`. Edite os valores conforme a
sua instalação do MySQL:

```python
import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # ajuste para o seu usuário
        password="SenhaPI@1234",  # ajuste para a sua senha
        database="quimic_lab"
    )
```

### 3. (Opcional) Inserir dados de teste

Para popular o banco com um professor, um aluno e algumas perguntas de exemplo:

```bash
mysql -u root -p quimic_lab < Back/seed_teste.sql
```

---

## Contas de teste

Disponíveis após executar `Back/seed_teste.sql`:

Professor:

```
E-mail: sabrina.costa@cps.sp.gov.br
Senha:  senha1234+
```

Aluno:

```
E-mail: aluno.teste@aluno.cps.gov.br
Senha:  senha1234+
Turma:  3C
```

Formato dos e-mails institucionais para novos cadastros:

- Aluno: `nome.sobrenome@aluno.cps.gov.br`
- Professor: `nome.sobrenome@cps.sp.gov.br`

---

## Estrutura do projeto

```
PI_QUIMICLAB/
├── main.py                       Ponto de entrada da aplicação
├── requirements.txt              Dependências Python
├── README.md                     Este arquivo
├── explicando_tudo.md            Documentação didática do código
├── mudancas_claude.md            Registro de alterações
│
├── app/                          Frontend (interface e lógica de tela)
│   ├── assets/
│   │   └── images/               Imagens e ícones da interface
│   │
│   ├── controllers/              Lógica de cada parte da tela
│   │   ├── animation_controller.py    Animações dos botões
│   │   ├── auth_controller.py         Login, cadastro e troca de senha
│   │   ├── editor_controller.py       Formulário de criar/editar pergunta
│   │   ├── navigation_controller.py   Navegação entre telas
│   │   ├── professor_controller.py    Relatórios e rankings
│   │   ├── question_controller.py     Lógica do jogo
│   │   └── ranking_controller.py
│   │
│   ├── services/                 Ponte entre a interface e o backend
│   │   ├── auth_service.py            Autenticação
│   │   ├── jogo_service.py            Perguntas, sessões, ranking, desbloqueio
│   │   ├── pergunta_service.py        CRUD de perguntas
│   │   └── ranking_service.py
│   │
│   ├── ui/
│   │   └── screens/
│   │       └── front_viewer.ui   Layout das telas (Qt Designer)
│   │
│   └── utils/                    Funções reutilizáveis
│       ├── ui_loader.py               Carrega o arquivo .ui
│       ├── scaler.py                  Redimensionamento responsivo
│       ├── imagem_util.py             Conversão de imagens do banco
│       └── helpers.py                 Estilos e animações auxiliares
│
└── Back/                         Backend (acesso ao banco de dados)
    ├── Conectar_Banco.py         Conexão com o MySQL
    ├── aluno.py                  Login e cadastro de aluno
    ├── professor.py              Login e cadastro de professor
    ├── Jogo.py                   Operações de jogo no banco
    ├── Perguntas.py              Classe Pergunta
    ├── codigo.sql                Schema do banco
    ├── diagrama_pi.sql           Schema do banco (equivalente)
    ├── migracao_imagem_blob.sql  Migração de imagens (schema antigo)
    └── seed_teste.sql            Dados de teste
```

---

## Arquitetura

O projeto é organizado em camadas, cada uma com uma responsabilidade. Uma
camada só conversa com a vizinha:

```
Interface (.ui)        Telas desenhadas no Qt Designer.
      |
Controllers            Tratam eventos (cliques), validam entradas e
(app/controllers)      decidem a navegação.
      |
Services               Traduzem as solicitações da interface para o
(app/services)          backend e tratam erros.
      |
Backend                Executa as operações no banco (SQL).
(Back)
      |
MySQL                  Persistência dos dados.
```

Padrão de retorno adotado nas camadas de serviço e backend: as funções devolvem
uma dupla `(resultado, erro)`. Em caso de sucesso, `(dados, None)`; em caso de
falha, `(None, "mensagem de erro")`. Os controllers verificam o segundo valor
para decidir se exibem um aviso ou seguem o fluxo.

Para uma explicação detalhada do funcionamento interno, consulte
[explicando_tudo.md](explicando_tudo.md).

---

## Banco de dados

Principais tabelas do schema `quimic_lab`:

| Tabela | Descrição |
|--------|-----------|
| `usuario` | Alunos e professores |
| `nivel` | Níveis de dificuldade (Fácil, Médio, Difícil) |
| `pergunta` | Enunciados das questões |
| `alternativa` | Alternativas de cada pergunta |
| `dica` | Dicas associadas às perguntas |
| `sessao_jogo` | Sessões de jogo iniciadas pelos alunos |
| `resposta` | Respostas registradas em cada sessão |
| `ranking` | Melhores pontuações por aluno e nível |
| `uso_dica` | Registro de uso de dicas |

O schema completo está em `Back/codigo.sql`.

---

## Solução de problemas

**A aplicação abre, mas exibe "Nenhuma pergunta encontrada".**
O MySQL provavelmente não está em execução ou o banco está sem perguntas
cadastradas. Verifique se o serviço do MySQL está ativo e se o schema e os
dados foram importados.

**Erro `ModuleNotFoundError: No module named 'PySide6'`.**
As dependências não foram instaladas no ambiente virtual ativo. Ative o
ambiente virtual e execute `pip install -r requirements.txt`.

**Erro de conexão com o banco de dados.**
Confirme as credenciais em `Back/Conectar_Banco.py` e verifique se o banco
`quimic_lab` existe:

```bash
mysql -u root -p quimic_lab -e "SHOW TABLES;"
```

**A interface aparece com proporções incorretas em telas muito diferentes de
1920x1080.**
O ajuste de escala é feito em `app/utils/scaler.py`, que parte de um design
base de 1920x1080. Em resoluções muito distintas pode haver pequenas
diferenças visuais.

---

## Documentação adicional

- [explicando_tudo.md](explicando_tudo.md): guia didático do código, voltado a
  quem está começando no projeto.
- [mudancas_claude.md](mudancas_claude.md): histórico de alterações.
- `Back/codigo.sql`: definição completa do banco de dados.

---

## Limitações conhecidas

- As senhas são armazenadas em texto simples (a coluna `senha_hash` ainda não
  aplica hash). Não utilize senhas reais.
- A funcionalidade de troca de senha valida apenas o preenchimento dos campos;
  a persistência da nova senha ainda não está implementada.

---

## Autores e orientação

Equipe de desenvolvimento:

- Arthur Prates Lopes
- Daniel Moura Lourenço
- Eloa Luiza de Oliveira Teixeira
- Maria Eduarda Vasconcelos de Moraes
- Pedro Henrique dos Santos Pinto
- Sabrina Lopes da Costa

Orientação e parceria:

- Orientador: Prof. Rudolf
- Instituição parceira: ETEC Júlio de Mesquita
- Responsável pela parceria: Maria do Socorro Sousa da Silva

---

## Licença

Projeto desenvolvido para fins educacionais pela ETEC Júlio de Mesquita (2026).
Uso autorizado no contexto educacional da instituição.
