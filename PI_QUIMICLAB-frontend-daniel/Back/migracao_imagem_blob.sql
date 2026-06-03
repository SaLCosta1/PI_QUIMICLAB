-- Migração: colunas imagem_url → imagem (MEDIUMBLOB) + imagem_mime
-- Execute apenas se o banco foi criado com a versão antiga do schema.
USE quimic_lab;

ALTER TABLE pergunta
  DROP COLUMN IF EXISTS imagem_url,
  ADD COLUMN IF NOT EXISTS imagem MEDIUMBLOB NULL DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS imagem_mime VARCHAR(50) NULL DEFAULT NULL;

ALTER TABLE alternativa
  DROP COLUMN IF EXISTS imagem_url,
  ADD COLUMN IF NOT EXISTS imagem MEDIUMBLOB NULL DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS imagem_mime VARCHAR(50) NULL DEFAULT NULL;

DROP VIEW IF EXISTS vw_desempenho;
DROP VIEW IF EXISTS vw_questoes_mais_erradas;

-- Recrie as views executando o trecho final de Back/codigo.sql
