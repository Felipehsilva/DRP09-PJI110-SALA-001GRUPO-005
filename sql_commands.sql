

CREATE TABLE usuario (
    cpf INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    login_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    senha VARCHAR(20) NOT NULL
);

CREATE TABLE Agendamentos (
    agendamento VARCHAR(200) PRIMARY KEY,
    cpf int NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario(cpf) ON DELETE CASCADE
);

use pi_schema; 
select * from usuario;

DROP TABLE Usuario;

-- limpa os dados da tabela sem deletar a tabela
ALTER TABLE Agendamentos DROP FOREIGN KEY Agendamentos_ibfk_1;
TRUNCATE TABLE usuario;

