-- Cria o banco de dados
CREATE DATABASE controle_alimentacao;

-- Usa o banco de dados criado
USE controle_alimentacao;

-- Cria a tabela de usuários
CREATE TABLE usuarios (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    celular VARCHAR(15),
    senha VARCHAR(255) NOT NULL,
    idade INT,
    peso DECIMAL(5,2),
    sexo ENUM('M', 'F', 'Outro')
);

-- Cria a tabela de alimentos
CREATE TABLE alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    calorias_por_porcao DECIMAL(6,2) NOT NULL
);

-- Cria a tabela de refeições
CREATE TABLE refeicoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf_usuario VARCHAR(11),
    tipo_refeicao ENUM('Almoço', 'Jantar') NOT NULL,
    data_refeicao DATE NOT NULL,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf)
);

-- Cria a tabela de detalhes das refeições
CREATE TABLE detalhes_refeicao (
    id_refeicao INT,
    id_alimento INT,
    proporcao DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_refeicao) REFERENCES refeicoes(id),
    FOREIGN KEY (id_alimento) REFERENCES alimentos(id)
);
