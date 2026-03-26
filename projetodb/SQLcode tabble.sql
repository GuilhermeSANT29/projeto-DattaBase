-- CRIAR BANCO
CREATE DATABASE IF NOT EXISTS projetodb;
USE projetodb;

-- CRIAR USUÁRIO
CREATE USER IF NOT EXISTS 'ADM'@'localhost' IDENTIFIED BY 'senha123';

-- DAR PERMISSÕES
GRANT ALL PRIVILEGES ON projetodb.* TO 'ADM'@'localhost';
FLUSH PRIVILEGES;

-- =========================
-- TABELA MAQUINAS
-- =========================
CREATE TABLE IF NOT EXISTS maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(100)
);

-- =========================
-- TABELA SENSORES
-- =========================
CREATE TABLE IF NOT EXISTS sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    maquina_id INT,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
        ON DELETE CASCADE
);

-- =========================
-- TABELA OPERADORES
-- =========================
CREATE TABLE IF NOT EXISTS operadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    turno VARCHAR(50)
);

-- =========================
-- TABELA LEITURAS
-- =========================
CREATE TABLE IF NOT EXISTS leituras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    temperatura DECIMAL(5,2),
    data_hora DATETIME,
    FOREIGN KEY (sensor_id) REFERENCES sensores(id)
        ON DELETE CASCADE
);

-- =========================
-- TABELA ALERTAS
-- =========================
CREATE TABLE IF NOT EXISTS alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    leitura_id INT,
    nivel VARCHAR(20),
    FOREIGN KEY (leitura_id) REFERENCES leituras(id)
        ON DELETE CASCADE
);

-- =========================
-- TABELA MANUTENCOES
-- =========================
CREATE TABLE IF NOT EXISTS manutencoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maquina_id INT NOT NULL,
    operador_id INT NULL,
    descricao TEXT,
    data_prevista DATETIME NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
        ON DELETE CASCADE,
        
    FOREIGN KEY (operador_id) REFERENCES operadores(id)
        ON DELETE SET NULL
);