SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `quimic_lab` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `quimic_lab`;

CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `senha_hash` VARCHAR(255) NOT NULL,
  `tipo` ENUM('aluno', 'professor') NOT NULL,
  `turma` VARCHAR(50) NULL DEFAULT NULL,
  `criado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX (`email` ASC),
  PRIMARY KEY (`id_usuario`));

CREATE TABLE IF NOT EXISTS `nivel` (
  `id_nivel` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `ordem` TINYINT NOT NULL,
  `pontuacao_minima_pct` TINYINT NOT NULL DEFAULT 60,
  `tempo_limite_seg` SMALLINT NOT NULL DEFAULT 120,
  PRIMARY KEY (`id_nivel`));

INSERT IGNORE INTO `nivel` (id_nivel, nome, ordem, pontuacao_minima_pct, tempo_limite_seg) VALUES
  (1, 'facil',   1, 60, 120),
  (2, 'medio',   2, 60, 90),
  (3, 'dificil', 3, 60, 60);

CREATE TABLE IF NOT EXISTS `pergunta` (
  `id_pergunta` INT NOT NULL AUTO_INCREMENT,
  `id_nivel` INT NOT NULL,
  `id_criador` INT NULL DEFAULT NULL,
  `enunciado` TEXT NOT NULL,
  `imagem_url` VARCHAR(500) NULL DEFAULT NULL,
  `ativa` TINYINT(1) NOT NULL DEFAULT 1,
  `criado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pergunta`),
  CONSTRAINT `fk_perg_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`),
  CONSTRAINT `fk_perg_criador` FOREIGN KEY (`id_criador`) REFERENCES `usuario` (`id_usuario`));

CREATE TABLE IF NOT EXISTS `alternativa` (
  `id_alternativa` INT NOT NULL AUTO_INCREMENT,
  `id_pergunta` INT NOT NULL,
  `texto` TEXT NULL DEFAULT NULL,
  `imagem_url` VARCHAR(500) NULL DEFAULT NULL,
  `correta` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_alternativa`),
  CONSTRAINT `fk_alt_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`));

CREATE TABLE IF NOT EXISTS `dica` (
  `id_dica` INT NOT NULL AUTO_INCREMENT,
  `id_pergunta` INT NOT NULL,
  `tipo` ENUM('eliminacao', 'texto') NOT NULL,
  `conteudo` TEXT NOT NULL,
  `penalizacao_pontos` SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_dica`),
  CONSTRAINT `fk_dica_perg` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`));

CREATE TABLE IF NOT EXISTS `sessao_jogo` (
  `id_sessao` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_nivel` INT NOT NULL,
  `pontuacao` SMALLINT NOT NULL DEFAULT 0,
  `concluida` TINYINT(1) NOT NULL DEFAULT 0,
  `iniciado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `finalizado_em` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id_sessao`),
  CONSTRAINT `fk_sess_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `fk_sess_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`));

CREATE TABLE IF NOT EXISTS `resposta` (
  `id_resposta` INT NOT NULL AUTO_INCREMENT,
  `id_sessao` INT NOT NULL,
  `id_pergunta` INT NOT NULL,
  `id_alternativa_escolhida` INT NOT NULL,
  `correta` TINYINT(1) NOT NULL,
  `tempo_resposta_seg` SMALLINT NULL DEFAULT NULL,
  `feedback_exibido` TINYINT(1) NOT NULL DEFAULT 0,
  `respondido_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_resposta`),
  CONSTRAINT `fk_resp_sessao` FOREIGN KEY (`id_sessao`) REFERENCES `sessao_jogo` (`id_sessao`),
  CONSTRAINT `fk_resp_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`),
  CONSTRAINT `fk_resp_alternativa` FOREIGN KEY (`id_alternativa_escolhida`) REFERENCES `alternativa` (`id_alternativa`));

CREATE TABLE IF NOT EXISTS `uso_dica` (
  `id_uso_dica` INT NOT NULL AUTO_INCREMENT,
  `id_sessao` INT NOT NULL,
  `id_pergunta` INT NOT NULL,
  `id_dica` INT NOT NULL,
  `usado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_uso_dica`),
  CONSTRAINT `fk_uso_sessao` FOREIGN KEY (`id_sessao`) REFERENCES `sessao_jogo` (`id_sessao`),
  CONSTRAINT `fk_uso_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`),
  CONSTRAINT `fk_uso_dica_ref` FOREIGN KEY (`id_dica`) REFERENCES `dica` (`id_dica`));

CREATE TABLE IF NOT EXISTS `ranking` (
  `id_ranking` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_nivel` INT NOT NULL,
  `melhor_pontuacao` SMALLINT NOT NULL DEFAULT 0,
  `total_tentativas` SMALLINT NOT NULL DEFAULT 0,
  `atualizado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ranking`),
  UNIQUE INDEX `uq_ranking` (`id_usuario` ASC, `id_nivel` ASC),
  CONSTRAINT `fk_rank_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `fk_rank_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`));

DROP TABLE IF EXISTS `vw_desempenho`;
DROP TABLE IF EXISTS `vw_questoes_mais_erradas`;

CREATE OR REPLACE VIEW vw_desempenho AS
SELECT
    u.id_usuario,
    u.nome,
    u.turma,
    n.nome                                                        AS nivel,
    COUNT(r.id_resposta)                                          AS total_respostas,
    SUM(r.correta)                                                AS acertos,
    COUNT(r.id_resposta) - SUM(r.correta)                        AS erros,
    ROUND(AVG(r.tempo_resposta_seg), 1)                          AS tempo_medio_seg,
    ROUND(SUM(r.correta) * 100.0 / NULLIF(COUNT(r.id_resposta), 0), 1) AS taxa_acerto_pct
FROM usuario u
JOIN sessao_jogo s ON s.id_usuario = u.id_usuario
JOIN nivel n       ON n.id_nivel   = s.id_nivel
JOIN resposta r    ON r.id_sessao  = s.id_sessao
GROUP BY u.id_usuario, u.nome, u.turma, n.id_nivel, n.nome;

CREATE OR REPLACE VIEW vw_questoes_mais_erradas AS
SELECT
    p.id_pergunta,
    p.enunciado,
    n.nome                                                              AS nivel,
    COUNT(r.id_resposta)                                                AS total_respostas,
    SUM(CASE WHEN r.correta = 0 THEN 1 ELSE 0 END)                    AS total_erros,
    ROUND(SUM(CASE WHEN r.correta = 0 THEN 1 ELSE 0 END)
          * 100.0 / NULLIF(COUNT(r.id_resposta), 0), 1)               AS taxa_erro_pct
FROM pergunta p
JOIN nivel n    ON n.id_nivel    = p.id_nivel
JOIN resposta r ON r.id_pergunta = p.id_pergunta
GROUP BY p.id_pergunta, p.enunciado, n.id_nivel, n.nome
ORDER BY taxa_erro_pct DESC;

-- ---------------------------------------------------------
-- Perguntas de exemplo para testar o jogo
-- ---------------------------------------------------------
INSERT IGNORE INTO pergunta (id_pergunta, id_nivel, enunciado, ativa) VALUES
(1, 1, 'Qual é o símbolo químico do ouro?', 1),
(2, 1, 'Quantos elétrons tem o átomo de carbono?', 1),
(3, 1, 'Qual é a fórmula molecular da água?', 1),
(4, 2, 'Qual é o número atômico do oxigênio?', 1),
(5, 2, 'O que é uma ligação covalente?', 1),
(6, 2, 'Qual é o pH de uma solução neutra?', 1),
(7, 3, 'O que é entalpia?', 1),
(8, 3, 'Qual é a lei de Avogadro?', 1);

INSERT IGNORE INTO alternativa (id_pergunta, texto, correta) VALUES
(1,'Au',1),(1,'Ag',0),(1,'Fe',0),(1,'Cu',0),
(2,'6',1),(2,'4',0),(2,'8',0),(2,'12',0),
(3,'H2O',1),(3,'CO2',0),(3,'NaCl',0),(3,'H2O2',0),
(4,'8',1),(4,'6',0),(4,'16',0),(4,'2',0),
(5,'Compartilhamento de elétrons entre átomos',1),
(5,'Transferência de elétrons entre átomos',0),
(5,'Atração entre íons de cargas opostas',0),
(5,'União de prótons entre núcleos',0),
(6,'7',1),(6,'0',0),(6,'14',0),(6,'5',0),
(7,'Energia total de um sistema termodinâmico a pressão constante',1),
(7,'Medida de desordem molecular',0),
(7,'Energia cinética das moléculas',0),
(7,'Calor específico de uma substância',0),
(8,'Volumes iguais de gases, nas mesmas condições, contêm o mesmo número de moléculas',1),
(8,'A pressão de um gás é inversamente proporcional ao volume',0),
(8,'A energia não pode ser criada nem destruída',0),
(8,'A massa se conserva em reações químicas',0);

INSERT IGNORE INTO dica (id_pergunta, tipo, conteudo, penalizacao_pontos) VALUES
(1,'texto','Vem do latim "Aurum".',10),
(1,'eliminacao','Elimina duas alternativas incorretas.',20),
(2,'texto','O número de elétrons é igual ao número atômico.',10),
(2,'eliminacao','Elimina duas alternativas incorretas.',20),
(3,'texto','Dois hidrogênios e um oxigênio.',10),
(3,'eliminacao','Elimina duas alternativas incorretas.',20),
(4,'texto','Está no grupo 16 da tabela periódica.',15),
(4,'eliminacao','Elimina duas alternativas incorretas.',25),
(5,'texto','Ocorre entre átomos de não-metais.',15),
(5,'eliminacao','Elimina duas alternativas incorretas.',25),
(6,'texto','Nem ácido nem básico.',15),
(6,'eliminacao','Elimina duas alternativas incorretas.',25),
(7,'texto','Relacionada a reações exotérmicas e endotérmicas.',20),
(7,'eliminacao','Elimina duas alternativas incorretas.',30),
(8,'texto','Relacionada ao número de Avogadro: 6,02 × 10²³.',20),
(8,'eliminacao','Elimina duas alternativas incorretas.',30);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
