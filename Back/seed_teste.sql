-- Seed de teste: 1 professor + 2 perguntas básicas (nível Fácil)
-- Idempotente o suficiente para o cenário de teste (assume banco recém-criado).
USE quimic_lab;

-- Professor de teste
INSERT INTO usuario (nome, email, senha_hash, tipo)
VALUES ('Sabrina Costa', 'sabrina.costa@cps.sp.gov.br', 'senha1234+', 'professor');
SET @prof := LAST_INSERT_ID();

-- Aluno de teste
INSERT INTO usuario (nome, email, senha_hash, tipo, turma)
VALUES ('Aluno Teste', 'aluno.teste@aluno.cps.gov.br', 'senha1234+', 'aluno', '3C');

-- Pergunta 1: 1 + 1
INSERT INTO pergunta (id_nivel, id_criador, enunciado, ativa)
VALUES (1, @prof, 'Quanto é 1 + 1?', 1);
SET @p1 := LAST_INSERT_ID();
INSERT INTO alternativa (id_pergunta, texto, correta) VALUES
  (@p1, '1', 0),
  (@p1, '2', 1),
  (@p1, '3', 0),
  (@p1, '4', 0);
INSERT INTO dica (id_pergunta, tipo, conteudo, penalizacao_pontos)
VALUES (@p1, 'texto', 'Some uma unidade a outra unidade.', 0);

-- Pergunta 2: 2 - 1
INSERT INTO pergunta (id_nivel, id_criador, enunciado, ativa)
VALUES (1, @prof, 'Quanto é 2 - 1?', 1);
SET @p2 := LAST_INSERT_ID();
INSERT INTO alternativa (id_pergunta, texto, correta) VALUES
  (@p2, '0', 0),
  (@p2, '1', 1),
  (@p2, '2', 0),
  (@p2, '3', 0);
INSERT INTO dica (id_pergunta, tipo, conteudo, penalizacao_pontos)
VALUES (@p2, 'texto', 'Retire uma unidade de duas.', 0);
