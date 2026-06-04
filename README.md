<div align="center">

# 🧪 QuimicLab

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/license-Educational-brightgreen.svg)](#-licença)

**Um jogo educacional gamificado para aprender sobre materiais de laboratório de Química**

[📖 Documentação](#-documentação) • [🚀 Início Rápido](#-como-instalar-e-executar) • [📋 Features](#-funcionalidades) • [👨‍💻 Autores](#-autores)

</div>

---

## 📋 Sobre o Projeto

**QuimicLab** é uma aplicação desktop interativa desenvolvida em **Python** com **PySide6** (Qt for Python) que utiliza **gamificação** para tornar o aprendizado de Química mais engajador e divertido.

O sistema foi desenvolvido como projeto integrador para a **ETEC Júlio de Mesquita** e oferece uma plataforma completa para alunos praticarem e professores acompanharem o desempenho no aprendizado de materiais e equipamentos de laboratório.

### 🎯 Objetivos do Sistema

1. **Educar** estudantes sobre os nomes de vidrarias usadas em aulas de química
2. **Ensinar** a identificar funções e aplicações dos materiais de laboratório
3. **Fornecer** feedback pedagógico através de relatórios detalhados de desempenho
4. **Engajar** alunos através de gamificação (pontuação, ranking, desafios)
5. **Facilitar** o acompanhamento pedagógico do professor

### 👥 Públicos-alvo

| Tipo | Descrição |
|------|-----------|
| **Alunos** | Estudantes do 1º ano do curso técnico em Química da ETEC |
| **Professores** | Docentes responsáveis pela disciplina "Química Geral e Experimental" |
| **Administradores** | Gestores que acompanham o programa educacional |

---

## 🎮 Funcionalidades

### Para Alunos 👨‍🎓

- ✅ **Autenticação Segura**: Login com email e senha (credenciais ETEC)
- ✅ **Três Níveis de Dificuldade**:
  - 🟢 **Fácil**: Identificação do nome do material de laboratório
  - 🟡 **Médio**: Identificação de sua função específica
  - 🔴 **Difícil**: Aplicação do material em contextos experimentais reais

- ✅ **Dois Modos de Jogo**:
  - 📚 **Modo Tradicional**: Prática livre sem pontuação ou penalidades
  - 🏆 **Modo Desafio**: Com pontuação registrada no ranking

- ✅ **Sistema Inteligente de Dicas**:
  - Eliminação de 2 alternativas incorretas (reduz para 2 opções)
  - Dica explicativa em formato textual
  - Limite: 1 dica de cada tipo por nível de dificuldade
  - Sem penalização de pontos

- ✅ **Feedback Pedagógico Imediato**:
  - Resposta correta indicada após envio
  - Explicação didática complementar
  - Referência de fontes de consulta

- ✅ **Controle de Tempo**:
  - 2 minutos por questão (configurável)
  - Timer visual com alerta
  - Questão marcada como não respondida se tempo expirar

- ✅ **Progresso e Desbloqueio**:
  - Necessário 60% de acerto para avançar de nível
  - Acompanhamento visual do progresso
  - Histórico de todas as sessões jogadas

- ✅ **Interface Responsiva**:
  - Escalável para diferentes resoluções
  - Imagens ilustrativas para cada questão
  - Design intuitivo e user-friendly

### Para Professores 👨‍🏫

- ✅ **Dashboard Completo**:
  - Visão geral do desempenho da turma
  - Acesso rápido a relatórios e gerenciamento

- ✅ **Relatórios Detalhados**:
  - **Ranking Geral**: Melhor desempenho dos alunos
  - **Relatório Individual**: Análise completa por aluno
  - **Estatísticas por Nível**: Taxa de acerto por dificuldade
  - **Análise de Questões**: Questões com maior índice de erro
  - **Comparação entre Turmas**: Desempenho médio comparativo

- ✅ **Gestão Completa de Conteúdo**:
  - ➕ **Adicionar Questões**: Cadastro com 4 alternativas
  - ✏️ **Editar Questões**: Modificar textos e imagens
  - 🗑️ **Remover Questões**: Deletar questões inativas
  - 📊 **Alterar Nível**: Reclassificar dificuldade

- ✅ **Recursos Pedagógicos**:
  - Associar imagens ilustrativas a cada questão
  - Definir dicas explicativas
  - Adicionar referências pedagógicas

- ✅ **Segurança e Privacidade**:
  - Ranking preserva privacidade de alunos
  - Apenas informações de desempenho exibidas
  - Acesso restrito a dados sensíveis

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Descrição |
|-----------|-----------|-----------|
| **Linguagem** | Python 3.8+ | Linguagem principal do projeto |
| **GUI** | PySide6 (Qt) | Framework para interface gráfica desktop |
| **Banco de Dados** | MySQL 5.7+ | Sistema de gerenciamento relacional |
| **Arquitetura** | MVC | Model-View-Controller para separação de responsabilidades |
| **Ambiente** | Visual Studio Code | IDE de desenvolvimento |
| **Controle de Versão** | Git | Sistema de versionamento de código |

### Dependências Python

```
PySide6>=6.6,<7.0      # Framework Qt para Python
python-dotenv          # Carregamento de variáveis de ambiente
mysql-connector-python # Conector para MySQL
```

---

## 📦 Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes componentes instalados:

| Requisito | Versão | Link |
|-----------|--------|------|
| **Python** | 3.8+ | [Download](https://www.python.org/downloads/) |
| **MySQL** | 5.7+ | [Download](https://www.mysql.com/downloads/) |
| **Git** | Latest | [Download](https://git-scm.com/) |
| **pip** | Latest | Incluído com Python 3.4+ |

### Verificar Instalações

```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar Git
git --version

# Verificar MySQL (deve estar rodando)
mysql --version
```

---

## 🚀 Como Instalar e Executar

### Passo 1️⃣: Clonar o Repositório

```bash
git clone https://github.com/SaLCosta1/PI_QUIMICLAB.git
cd PI_QUIMICLAB-frontend-daniel
```

### Passo 2️⃣: Criar e Ativar Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 **Por que usar venv?** Ambientes virtuais isolam dependências do projeto das dependências globais do Python, evitando conflitos.

### Passo 3️⃣: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4️⃣: Configurar o Banco de Dados

#### 4.1: Iniciar o MySQL

**Windows (via Command Prompt):**
```bash
mysql -u root -p
```

**Linux/Mac:**
```bash
sudo mysql -u root -p
```

#### 4.2: Executar o Script SQL

```sql
-- Dentro do MySQL, execute:
source Back/diagrama_pi.sql;

-- Ou importe diretamente do terminal:
mysql -u root -p quimic_lab < Back/diagrama_pi.sql
```

#### 4.3: Configurar Credenciais (IMPORTANTE!)

Edite o arquivo `Back/Conectar_Banco.py`:

```python
import mysql.connector

def conectar_banco():
    """Estabelece conexão com o banco de dados MySQL"""
    conexao = mysql.connector.connect(
        host="localhost",           # Seu servidor MySQL
        user="seu_usuario",         # ⚙️ ALTERAR: seu usuário MySQL
        password="sua_senha",       # ⚙️ ALTERAR: sua senha MySQL
        database="quimic_lab"       # Nome do banco (criado pelo SQL)
    )
    return conexao
```

### Passo 5️⃣: Executar a Aplicação

```bash
python main.py
```

Uma janela desktop abrirá com a interface do QuimicLab. 🎉

---

## 📁 Estrutura do Projeto

```
PI_QUIMICLAB-frontend-daniel/
│
├── 📄 main.py                      # ⭐ Ponto de entrada da aplicação
├── 📄 requirements.txt              # Dependências Python
├── 📄 README.md                     # Este arquivo
│
├── 📁 app/                          # Frontend (Interface Gráfica)
│   ├── 📁 assets/                   # Recursos visuais
│   │   └── 📁 images/              # Imagens do projeto
│   │
│   ├── 📁 controllers/              # Lógica de navegação (MVC - Controller)
│   │   ├── animation_controller.py  # Animações e efeitos visuais
│   │   ├── auth_controller.py       # Login e autenticação
│   │   ├── editor_controller.py     # Edição de questões (professor)
│   │   ├── navigation_controller.py # Navegação entre telas
│   │   ├── professor_controller.py  # Funcionalidades do professor
│   │   ├── question_controller.py   # Lógica do jogo (perguntas)
│   │   ├── ranking_controller.py    # Ranking e estatísticas
│   │   └── __init__.py
│   │
│   ├── 📁 services/                 # Camada de negócios (MVC - Model)
│   │   ├── auth_service.py          # Serviços de autenticação
│   │   ├── jogo_service.py          # Lógica principal do jogo
│   │   ├── pergunta_service.py      # Gerenciamento de perguntas
│   │   ├── ranking_service.py       # Cálculos de ranking
│   │   ├── 📁 mocks/                # Dados de teste (sem DB)
│   │   │   ├── auth_service_mock.py
│   │   │   ├── jogo_service_mock.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── 📁 ui/                       # Interface (MVC - View)
│   │   ├── 📁 screens/
│   │   │   └── front_viewer.ui      # Layout Qt Designer
│   │   └── __init__.py
│   │
│   ├── 📁 utils/                    # Funções utilitárias
│   │   ├── ui_loader.py             # Carregador de UI (.ui → .py)
│   │   ├── scaler.py                # Ajuste de escala responsiva
│   │   ├── imagem_util.py           # Processamento de imagens
│   │   ├── helpers.py               # Funções auxiliares
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📁 Back/                         # Backend (Banco de Dados)
│   ├── 📄 Conectar_Banco.py         # 🔌 Conexão MySQL (EDITAR COM SUAS CREDENCIAIS)
│   ├── 📄 aluno.py                  # Modelo e operações de aluno
│   ├── 📄 professor.py              # Modelo e operações de professor
│   ├── 📄 Jogo.py                   # Lógica de jogo no BD
│   ├── 📄 Perguntas.py              # Gerenciamento de perguntas
│   ├── 📄 diagrama_pi.sql           # 📊 Schema do banco (executar primeiro!)
│   ├── 📄 requerimentos.txt         # Dependências (se houver)
│   └── __init__.py
│
├── 📁 Back/                         (Não presente nesta pasta - referência)
│   └── ... (Backend separado - se aplicável)
│
└── 📄 .gitignore                    # Arquivos ignorados pelo Git

```

### Descrição de Pastas Principais

| Pasta | Responsabilidade | Exemplos |
|-------|------------------|----------|
| `controllers/` | Lógica de navegação e eventos | Clique em botão → Ação |
| `services/` | Lógica de negócios | Validação, cálculos, regras |
| `ui/` | Interface gráfica visual | Layouts, botões, campos |
| `utils/` | Funções reutilizáveis | Formatação, escalas, imagens |
| `Back/` | Banco de dados | Modelos, conexões, queries |

---

## 👤 Contas de Teste
│   │   ├── auth_controller.py
│   │   ├── question_controller.py
│   │   ├── professor_controller.py
│   │   └── ...
│   ├── services/                    # Serviços de negócio
│   │   ├── jogo_service.py         # Lógica do jogo
│   │   ├── auth_service.py
│   │   └── ...
│   ├── ui/                          # Interface gráfica (UI)
│   │   └── screens/
│   │       └── front_viewer.ui
│   └── utils/                       # Funções utilitárias
│       ├── ui_loader.py
│       ├── scaler.py
│       └── helpers.py
│
├── Back/                            # Backend (banco de dados)
│   ├── Conectar_Banco.py           # Conexão MySQL
│   ├── Jogo.py                     # Operações do jogo
│   ├── aluno.py                    # Autenticação aluno
│   ├── professor.py                # Autenticação professor
│   ├── Perguntas.py                # Modelo de pergunta
│   ├── diagrama_pi.sql             # Schema do banco
│   └── ...
│
└── README.md                        # Este arquivo
```

---

## 👥 Contas de Teste

#### Aluno (Teste)
```
Email:  teste.aluno@aluno.cps.gov.br
Senha:  senha1234+
Turma:  3C
```

#### Professor (Teste)
```
Email:  professor.nome@cps.sp.gov.br
Senha:  senha1234+
```

> 💡 **Dica de Registro**: Para cadastrar novos alunos, use o formato:
> - Email: `nome.sobrenome@aluno.cps.gov.br`
> - Senha: Deve conter letras maiúsculas, números e caracteres especiais

---

## 📚 Como Usar

### 🎮 Para Alunos (Passo a Passo)

1. **Iniciar a Aplicação**
   ```bash
   python main.py
   ```

2. **Login**
   - Clique em "Login Aluno"
   - Insira seu email e senha
   - Clique em "Entrar"

3. **Escolher Modo de Jogo**
   - 📚 **Modo Tradicional**: Prática sem pontuação
   - 🏆 **Modo Desafio**: Com pontuação e ranking

4. **Selecionar Nível de Dificuldade**
   - 🟢 **Fácil**: Começar por aqui (recomendado para iniciantes)
   - 🟡 **Médio**: Avançar após 60% de acerto em Fácil
   - 🔴 **Difícil**: Avançar após 60% de acerto em Médio

5. **Responder Questões**
   - Leia a pergunta com atenção
   - Analise a imagem ilustrativa
   - Use dicas se necessário (máximo 1 de cada tipo)
   - Selecione sua resposta em até 2 minutos
   - Clique em "Confirmar Resposta"

6. **Visualizar Resultado**
   - Veja a resposta correta
   - Leia a explicação pedagógica
   - Consulte a referência (se disponível)
   - Clique em "Próxima Questão"

7. **Acompanhar Progresso**
   - Veja sua pontuação em tempo real
   - Acompanhe o progresso da barra
   - Confira seu desempenho no final da sessão

### 👨‍🏫 Para Professores (Passo a Passo)

1. **Fazer Login**
   - Clique em "Login Professor"
   - Insira email e senha
   - Clique em "Entrar"

2. **Acessar Dashboard**
   - Menu principal com opções:
     - Relatórios
     - Gerenciamento de Questões
     - Configurações

3. **Visualizar Relatórios**

   **Ranking Geral**:
   - Veja os melhores alunos
   - Compare desempenho
   - Analise tendências

   **Relatório Individual**:
   - Selecione um aluno
   - Visualize:
     - Pontuação total
     - Taxa de acerto por nível
     - Questões erradas
     - Tempo médio de resposta
     - Histórico de sessões

4. **Gerenciar Perguntas**

   **Adicionar Nova Pergunta**:
   - Clique em "Nova Pergunta"
   - Preencha o texto da pergunta
   - Insira 4 alternativas
   - Selecione a alternativa correta
   - Escolha o nível de dificuldade
   - Adicione uma imagem (opcional)
   - Insira dica explicativa (opcional)
   - Clique em "Salvar"

   **Editar Pergunta**:
   - Selecione a pergunta na lista
   - Modifique os campos desejados
   - Clique em "Atualizar"

   **Alterar Nível**:
   - Selecione a pergunta
   - Clique em "Alterar Nível"
   - Escolha novo nível
   - Confirme

   **Remover Pergunta**:
   - Selecione a pergunta
   - Clique em "Remover"
   - Confirme a exclusão

5. **Acompanhamento Pedagógico**
   - Identifique questões com maior taxa de erro
   - Reavalie o nível de dificuldade se necessário
   - Acompanhe o progresso dos alunos
   - Compare desempenho entre turmas

---

## 📊 Conteúdo do Banco de Dados

### Tabelas Principais

| Tabela | Descrição | Registros |
|--------|-----------|-----------|
| `usuario` | Alunos e Professores | ~50+ cadastros |
| `nivel` | Níveis de dificuldade | 3 (Fácil, Médio, Difícil) |
| `pergunta` | Perguntas do jogo | 30+ perguntas |
| `alternativa` | Opções de resposta | 120+ (4 por pergunta) |
| `sessao_jogo` | Sessões do aluno | Criadas dinamicamente |
| `resposta` | Respostas do aluno | Registro de cada tentativa |
| `ranking` | Pontuações | Atualizado em tempo real |
| `dica` | Dicas das perguntas | Associadas às perguntas |

> 📖 Veja `Back/diagrama_pi.sql` para o schema completo

---

## 🏗️ Arquitetura do Projeto

### Padrão MVC (Model-View-Controller)

```
┌─────────────────────────────────────────┐
│         VIEW (Interface Gráfica)        │
│  - PySide6 / Qt Designer                │
│  - app/ui/                              │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    CONTROLLER (Lógica de Navegação)     │
│  - Eventos de botões                    │
│  - Navegação entre telas                │
│  - app/controllers/                     │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│     MODEL (Lógica de Negócios)          │
│  - Validações                           │
│  - Cálculos e Regras                    │
│  - app/services/ + Back/                │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    BANCO DE DADOS (MySQL)               │
│  - Persistência de dados                │
│  - Queries e transações                 │
└─────────────────────────────────────────┘
```

### Fluxo de Uso

```
Usuário interage com UI
    ↓
Controller captura evento
    ↓
Controller chama Service
    ↓
Service executa lógica de negócios
    ↓
Service conecta ao Banco de Dados
    ↓
Resultado retorna ao Controller
    ↓
Controller atualiza a UI
    ↓
Usuário vê resultado
```

---

## 🐛 Troubleshooting (Resolução de Problemas)

### ❌ Erro: "Conexão com banco de dados falhou"

**Causa**: MySQL não está rodando ou credenciais incorretas

**Solução**:
1. Verifique se MySQL está rodando:
   ```bash
   mysql -u root -p
   ```
2. Confirme credenciais em `Back/Conectar_Banco.py`
3. Garanta que o banco `quimic_lab` foi criado:
   ```bash
   mysql -u root -p quimic_lab -e "SHOW TABLES;"
   ```

### ❌ Erro: "ModuleNotFoundError: No module named 'PySide6'"

**Causa**: Dependências não instaladas

**Solução**:
```bash
# Ativar ambiente virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
```

### ❌ Erro: "Nenhuma pergunta encontrada"

**Causa**: Banco de dados vazio

**Solução**:
1. Verifique se o script SQL foi executado:
   ```bash
   mysql -u root -p quimic_lab < Back/diagrama_pi.sql
   ```
2. Confirme perguntas cadastradas:
   ```sql
   SELECT COUNT(*) FROM pergunta;
   ```

### ❌ Interface gráfica distorcida ou com letras pequenas

**Causa**: Escala de tela não compatível

**Solução**:
1. Edite `app/utils/scaler.py`
2. Ajuste as constantes de escala
3. Reinicie a aplicação

### ❌ Erro: "Permission denied" ao executar main.py

**Causa**: Falta de permissão de execução (Linux/Mac)

**Solução**:
```bash
chmod +x main.py
python main.py
```

---

## 📖 Documentação Completa

Acesse a documentação técnica completa:
- 📄 **Documentação do Projeto**: [PDF - Análise e Especificações]
- 📊 **Banco de Dados**: `Back/diagrama_pi.sql`
- 🎨 **Design de Telas**: `app/ui/screens/`

---

## 🤝 Contribuindo

Quer contribuir com o projeto? Siga os passos:

1. **Faça um Fork** do repositório
2. **Crie uma Branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit suas mudanças** (`git commit -m 'Adicionei MinhaFeature'`)
4. **Push para a Branch** (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request** descrevendo suas mudanças

### Padrões de Código

- Use **PEP 8** para Python
- Adicione **docstrings** em todas as funções
- Escreva **nomes descritivos** para variáveis
- Mantenha a **estrutura MVC**

---

## 📝 Licença

Este projeto foi desenvolvido para fins **educacionais** pela **ETEC Júlio de Mesquita** em 2026.

Uso autorizado apenas dentro do contexto educacional da instituição.

---

## 👨‍💻 Autores e Colaboradores

### 📌 Equipe de Desenvolvimento

| Nome | Rol | Email |
|------|-----|-------|
| **Arthur Prates Lopes** | Desenvolvedor | - |
| **Daniel Moura Lourenço** | Desenvolvedor | - |
| **Eloa Luiza de Oliveira Teixeira** | Desenvolvedora | - |
| **Maria Eduarda Vasconcelos de Moraes** | Desenvolvedora | - |
| **Pedro Henrique dos Santos Pinto** | Desenvolvedor | - |
| **Sabrina Lopes da Costa** | Desenvolvedora | - |

### 👨‍🏫 Orientação e Parceria

| Rol | Nome |
|-----|------|
| **Orientador** | Prof. Rudolf |
| **Parceiro** | ETEC Júlio de Mesquita |
| **Responsável Parceiro** | Maria do Socorro Sousa da Silva |

---

## 📞 Suporte e Contato

### Para Dúvidas Técnicas
- 📧 Entre em contato com os desenvolvedores
- 🐛 Reporte bugs via [Issues](https://github.com/SaLCosta1/PI_QUIMICLAB/issues)
- 💡 Sugira melhorias via Pull Requests

### Para Dúvidas Pedagógicas
- 👨‍🏫 Contate o Prof. Rudolf
- 🏫 Entre em contato com a ETEC Júlio de Mesquita

---

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| **Linguagem Principal** | Python 3.8+ |
| **Linhas de Código** | 5000+ |
| **Arquivos** | 50+ |
| **Tabelas BD** | 8+ |
| **Perguntas** | 30+ |
| **Versão** | 1.0.0 |
| **Status** | ✅ Em Produção |

---

## 🔄 Histórico de Versões

### v1.0.0 - Junho 2026 ✅
- ✅ Sistema completo implementado
- ✅ Autenticação de alunos e professores
- ✅ 30+ perguntas cadastradas
- ✅ Relatórios funcionais
- ✅ Sistema de ranking
- ✅ Interface responsiva

---

**Desenvolvido com ❤️ para educação em Química**

[⬆ Voltar ao Topo](#-quimiclab)
