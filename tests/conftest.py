import os
os.environ['TESTING'] = "True"

import pytest
from webapp import app, db

@pytest.fixture
def client():
    """
    Fixture que configura o cliente de testes da aplicação Flask.
    Aqui usamos o banco de dados em memória do SQLite (sqlite:///:memory:) 
    para simular a conexão de banco, isolando os testes da base de produção.
    O banco em memória é destruído assim que a aplicação é encerrada.
    """
    # Ativa o modo de teste para facilitar debug de erros internos do Flask
    app.config['TESTING'] = True
    # Usa banco em memória para que os dados existam apenas durante os testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # O WTF_CSRF_ENABLED pode precisar ser falso se utilizássemos Flask-WTF
    # app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as test_client:
        with app.app_context():
            # Cria a estrutura de tabelas no banco de dados simulado
            db.create_all()
            yield test_client
            # Após executar os testes dependentes desta fixture, os dados são limpos
            db.session.remove()
            db.drop_all()
