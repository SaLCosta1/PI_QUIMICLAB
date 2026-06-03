SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `quimic_lab` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `quimic_lab`;

-- usuario
-- senha_hash guarda a senha em texto simples por enquanto (SENHA_PADRAO = 'senha1234+')
-- email do aluno: nome.sobrenome@aluno.cps.gov.br
-- email do professor: nome.sobrenome@cps.sp.gov.br
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `senha_hash` VARCHAR(255) NOT NULL,
  `tipo` ENUM('aluno', 'professor') NOT NULL,
  `turma` VARCHAR(50) NULL DEFAULT NULL,
  `criado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX (`email` ASC)
);

-- nivel
-- ordem 1 = Fácil   -> identifica nome do material      -> 100 pts no desafio
-- ordem 2 = Médio   -> identifica função do material    -> 200 pts no desafio
-- ordem 3 = Difícil -> aplica em procedimento           -> 300 pts no desafio
-- pontuacao_minima_pct: percentual mínimo de acertos pra desbloquear o próximo nível (modo tradicional)
-- pontuacao_desafio: pontos ganhos por acerto no modo desafio
CREATE TABLE IF NOT EXISTS `nivel` (
  `id_nivel` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `ordem` TINYINT NOT NULL,
  `pontuacao_minima_pct` TINYINT NOT NULL DEFAULT 60,
  `tempo_limite_seg` SMALLINT NOT NULL DEFAULT 120,
  `pontuacao_desafio` SMALLINT NOT NULL DEFAULT 100,
  PRIMARY KEY (`id_nivel`)
);

INSERT IGNORE INTO `nivel` (id_nivel, nome, ordem, pontuacao_minima_pct, tempo_limite_seg, pontuacao_desafio) VALUES
(1, 'Fácil',   1, 60, 120, 100),
(2, 'Médio',   2, 60, 120, 200),
(3, 'Difícil', 3, 60, 120, 300);

-- pergunta
-- imagem: bytes da imagem armazenados diretamente no banco (BLOB)
-- imagem_mime: tipo MIME para reconstrução correta no frontend (ex: image/png)
CREATE TABLE IF NOT EXISTS `pergunta` (
  `id_pergunta` INT NOT NULL AUTO_INCREMENT,
  `id_nivel` INT NOT NULL,
  `id_criador` INT NULL DEFAULT NULL,
  `enunciado` TEXT NOT NULL,
  `imagem` MEDIUMBLOB NULL DEFAULT NULL,
  `imagem_mime` VARCHAR(50) NULL DEFAULT NULL,
  `ativa` TINYINT(1) NOT NULL DEFAULT 1,
  `criado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pergunta`),
  INDEX `fk_perg_nivel` (`id_nivel` ASC),
  INDEX `fk_perg_criador` (`id_criador` ASC),
  CONSTRAINT `fk_perg_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`),
  CONSTRAINT `fk_perg_criador` FOREIGN KEY (`id_criador`) REFERENCES `usuario` (`id_usuario`)
);

-- alternativa
CREATE TABLE IF NOT EXISTS `alternativa` (
  `id_alternativa` INT NOT NULL AUTO_INCREMENT,
  `id_pergunta` INT NOT NULL,
  `texto` TEXT NULL DEFAULT NULL,
  `imagem` MEDIUMBLOB NULL DEFAULT NULL,
  `imagem_mime` VARCHAR(50) NULL DEFAULT NULL,
  `correta` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_alternativa`),
  INDEX `fk_alt_pergunta` (`id_pergunta` ASC),
  CONSTRAINT `fk_alt_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`)
);

-- dica
-- penalizacao_pontos: no modo tradicional fica 0, no modo desafio é 50% da pontuacao_desafio do nível
CREATE TABLE IF NOT EXISTS `dica` (
  `id_dica` INT NOT NULL AUTO_INCREMENT,
  `id_pergunta` INT NOT NULL,
  `tipo` ENUM('eliminacao', 'texto') NOT NULL,
  `conteudo` TEXT NOT NULL,
  `penalizacao_pontos` SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_dica`),
  INDEX `fk_dica_perg` (`id_pergunta` ASC),
  CONSTRAINT `fk_dica_perg` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`)
);

-- sessao_jogo
-- modo: tradicional = sem penalização na dica, progressão por acertos
--       desafio     = dica penaliza 50%, rankeamento por pontuação
CREATE TABLE IF NOT EXISTS `sessao_jogo` (
  `id_sessao` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_nivel` INT NOT NULL,
  `modo` ENUM('tradicional', 'desafio') NOT NULL DEFAULT 'tradicional',
  `pontuacao` SMALLINT NOT NULL DEFAULT 0,
  `concluida` TINYINT(1) NOT NULL DEFAULT 0,
  `iniciado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `finalizado_em` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id_sessao`),
  INDEX `fk_sess_usuario` (`id_usuario` ASC),
  INDEX `fk_sess_nivel` (`id_nivel` ASC),
  CONSTRAINT `fk_sess_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `fk_sess_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`)
);

-- resposta
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
  INDEX `fk_resp_sessao` (`id_sessao` ASC),
  INDEX `fk_resp_pergunta` (`id_pergunta` ASC),
  INDEX `fk_resp_alternativa` (`id_alternativa_escolhida` ASC),
  CONSTRAINT `fk_resp_sessao` FOREIGN KEY (`id_sessao`) REFERENCES `sessao_jogo` (`id_sessao`),
  CONSTRAINT `fk_resp_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`),
  CONSTRAINT `fk_resp_alternativa` FOREIGN KEY (`id_alternativa_escolhida`) REFERENCES `alternativa` (`id_alternativa`)
);

-- uso_dica
CREATE TABLE IF NOT EXISTS `uso_dica` (
  `id_uso_dica` INT NOT NULL AUTO_INCREMENT,
  `id_sessao` INT NOT NULL,
  `id_pergunta` INT NOT NULL,
  `id_dica` INT NOT NULL,
  `usado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_uso_dica`),
  INDEX `fk_uso_sessao` (`id_sessao` ASC),
  INDEX `fk_uso_pergunta` (`id_pergunta` ASC),
  INDEX `fk_uso_dica_ref` (`id_dica` ASC),
  CONSTRAINT `fk_uso_sessao` FOREIGN KEY (`id_sessao`) REFERENCES `sessao_jogo` (`id_sessao`),
  CONSTRAINT `fk_uso_pergunta` FOREIGN KEY (`id_pergunta`) REFERENCES `pergunta` (`id_pergunta`),
  CONSTRAINT `fk_uso_dica_ref` FOREIGN KEY (`id_dica`) REFERENCES `dica` (`id_dica`)
);

-- ranking (modo desafio)
CREATE TABLE IF NOT EXISTS `ranking` (
  `id_ranking` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_nivel` INT NOT NULL,
  `melhor_pontuacao` SMALLINT NOT NULL DEFAULT 0,
  `total_tentativas` SMALLINT NOT NULL DEFAULT 0,
  `atualizado_em` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ranking`),
  UNIQUE INDEX `uq_ranking` (`id_usuario` ASC, `id_nivel` ASC),
  INDEX `fk_rank_nivel` (`id_nivel` ASC),
  CONSTRAINT `fk_rank_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `fk_rank_nivel` FOREIGN KEY (`id_nivel`) REFERENCES `nivel` (`id_nivel`)
);

-- view de desempenho do aluno (relatório do professor)
DROP VIEW IF EXISTS `vw_desempenho`;
CREATE OR REPLACE VIEW vw_desempenho AS
SELECT
    u.id_usuario,
    u.nome,
    u.turma,
    n.nome AS nivel,
    s.modo,
    COUNT(r.id_resposta) AS total_respostas,
    SUM(r.correta) AS acertos,
    COUNT(r.id_resposta) - SUM(r.correta) AS erros,
    ROUND(AVG(r.tempo_resposta_seg), 1) AS tempo_medio_seg,
    ROUND(SUM(r.correta) * 100.0 / NULLIF(COUNT(r.id_resposta), 0), 1) AS taxa_acerto_pct
FROM usuario u
JOIN sessao_jogo s ON s.id_usuario = u.id_usuario
JOIN nivel n ON n.id_nivel = s.id_nivel
JOIN resposta r ON r.id_sessao = s.id_sessao
GROUP BY u.id_usuario, u.nome, u.turma, n.id_nivel, n.nome, s.id_sessao, s.modo;

-- view das questões mais erradas
DROP VIEW IF EXISTS `vw_questoes_mais_erradas`;
CREATE OR REPLACE VIEW vw_questoes_mais_erradas AS
SELECT
    p.id_pergunta,
    p.enunciado,
    n.nome AS nivel,
    COUNT(r.id_resposta) AS total_respostas,
    SUM(CASE WHEN r.correta = 0 THEN 1 ELSE 0 END) AS total_erros,
    ROUND(SUM(CASE WHEN r.correta = 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(r.id_resposta), 0), 1) AS taxa_erro_pct
FROM pergunta p
JOIN nivel n ON n.id_nivel = p.id_nivel
JOIN resposta r ON r.id_pergunta = p.id_pergunta
GROUP BY p.id_pergunta, p.enunciado, n.id_nivel, n.nome
ORDER BY taxa_erro_pct DESC;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
