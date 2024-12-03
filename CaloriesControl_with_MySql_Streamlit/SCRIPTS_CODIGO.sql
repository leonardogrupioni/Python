-- 1. Criação do Banco de Dados
-- Cria o banco de dados 'controle_alimentacao'

CREATE DATABASE IF NOT EXISTS controle_alimentacao;
USE controle_alimentacao;

-- 2. Criação das Tabelas
-- 2.1. Tabela 'usuarios'
-- Armazena os dados dos usuários

CREATE TABLE IF NOT EXISTS usuarios (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    celular VARCHAR(15),
    senha VARCHAR(255) NOT NULL,
    idade INT,
    peso DECIMAL(5,2),
    sexo ENUM('M', 'F', 'Outro')
);

-- 2.2. Tabela 'alimentos'
-- Armazena os alimentos disponíveis

CREATE TABLE IF NOT EXISTS alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    calorias_por_porcao DECIMAL(6,2) NOT NULL
);

-- 2.3. Tabela 'refeicoes'
-- Armazena as refeições registradas pelos usuários

CREATE TABLE IF NOT EXISTS refeicoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf_usuario VARCHAR(11),
    tipo_refeicao ENUM('Almoço', 'Jantar') NOT NULL,
    data_refeicao DATE NOT NULL,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON DELETE CASCADE
);

-- 2.4. Tabela 'detalhes_refeicao'
-- Armazena os detalhes dos alimentos consumidos em cada refeição

CREATE TABLE IF NOT EXISTS detalhes_refeicao (
    id_refeicao INT,
    id_alimento INT,
    proporcao DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_refeicao) REFERENCES refeicoes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_alimento) REFERENCES alimentos(id)
);


-- 3. Inserção de Dados Iniciais
-- 3.1. Inserção de Alimentos Padrão

INSERT INTO alimentos (nome, calorias_por_porcao) VALUES
('Arroz', 130),
('Feijão', 95),
('Frango grelhado', 165),
('Salada', 20),
('Batata cozida', 80),
('Macarrão', 158),
('Carne bovina', 250),
('Peixe', 120),
('Ovo cozido', 78),
('Suco natural', 90)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);


-- 4. Consultas SQL Utilizadas no Aplicativo

-- As consultas abaixo são utilizadas nas operações do aplicativo em Python.
-- Elas estão parametrizadas com '?' ou '%s' nos scripts Python, mas aqui
-- apresentamos exemplos genéricos para referência.

-- 4.1. Operações com Usuários

-- 4.1.1. Cadastro de Novo Usuário
-- Comentário: Insere um novo usuário na tabela 'usuarios'.

-- Exemplo de uso:
INSERT INTO usuarios (cpf, nome, email, celular, senha, idade, peso, sexo)
VALUES ('CPF_DO_USUARIO', 'Nome Completo', 'email@exemplo.com', '123456789', 'SENHA_HASH', 30, 70.5, 'M');

-- 4.1.2. Autenticação de Usuário
-- Comentário: Seleciona a senha do usuário para verificação durante o login.

-- Exemplo de uso:
SELECT senha FROM usuarios WHERE cpf = 'CPF_DO_USUARIO';

-- 4.1.3. Atualização dos Dados do Usuário
-- Comentário: Atualiza as informações do usuário na tabela 'usuarios'.

-- Exemplo de uso:
UPDATE usuarios
SET nome='Novo Nome', email='novoemail@exemplo.com', celular='987654321', senha='NOVO_SENHA_HASH', idade=31, peso=72.0, sexo='M'
WHERE cpf='CPF_DO_USUARIO';

-- 4.1.4. Exclusão de Usuário
-- Comentário: Remove o usuário e todas as suas informações relacionadas.

-- Exemplo de uso:
DELETE FROM usuarios WHERE cpf = 'CPF_DO_USUARIO';

-- 4.2. Operações com Alimentos

-- 4.2.1. Inserção de Novo Alimento
-- Comentário: Adiciona um novo alimento à tabela 'alimentos'.

-- Exemplo de uso:
INSERT INTO alimentos (nome, calorias_por_porcao)
VALUES ('Nome do Alimento', 100.0);

-- 4.2.2. Seleção de Alimentos
-- Comentário: Recupera todos os alimentos cadastrados.

-- Exemplo de uso:
SELECT id, nome, calorias_por_porcao FROM alimentos;

-- 4.3. Operações com Refeições

-- 4.3.1. Registro de Nova Refeição
-- Comentário: Insere uma nova refeição na tabela 'refeicoes'.

-- Exemplo de uso:
INSERT INTO refeicoes (cpf_usuario, tipo_refeicao, data_refeicao)
VALUES ('CPF_DO_USUARIO', 'Almoço', '2023-10-01');

-- 4.3.2. Registro dos Detalhes da Refeição
-- Comentário: Insere os alimentos consumidos em uma refeição específica.

-- Exemplo de uso:
INSERT INTO detalhes_refeicao (id_refeicao, id_alimento, proporcao)
VALUES (ID_DA_REFEICAO, ID_DO_ALIMENTO, 1.5);

-- 4.3.3. Consulta do Histórico de Refeições
-- Comentário: Recupera os detalhes das refeições do usuário em uma data específica.

-- Exemplo de uso:
SELECT a.nome, a.calorias_por_porcao, dr.proporcao
FROM refeicoes r
JOIN detalhes_refeicao dr ON r.id = dr.id_refeicao
JOIN alimentos a ON dr.id_alimento = a.id
WHERE r.cpf_usuario = 'CPF_DO_USUARIO' AND r.tipo_refeicao = 'Almoço' AND r.data_refeicao = '2023-10-01';

-- 4.3.4. Cálculo de Calorias Consumidas
-- Comentário: Calcula o total de calorias com base nos alimentos e proporções consumidas.

-- A operação é realizada no código Python, mas utiliza dados obtidos através das consultas SQL acima.

-- 4.3.5. Exclusão de Refeições Relacionadas a um Usuário (Ao Excluir Conta)
-- Comentário: Remove as refeições e detalhes associados a um usuário.

-- Exemplo de uso para detalhes das refeições:
DELETE dr FROM detalhes_refeicao dr
JOIN refeicoes r ON dr.id_refeicao = r.id
WHERE r.cpf_usuario = 'CPF_DO_USUARIO';

-- Exemplo de uso para as refeições:
DELETE FROM refeicoes WHERE cpf_usuario = 'CPF_DO_USUARIO';


-- 5. Considerações Finais
-- Este script fornece a estrutura necessária para criar o banco de dados
-- e as tabelas utilizadas pelo aplicativo de controle de alimentação diária.
-- As consultas SQL apresentadas servem como referência para as operações
-- executadas pelo aplicativo em Python.