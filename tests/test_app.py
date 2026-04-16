import pytest
from unittest.mock import patch
from webapp import db, Usuario, Agendamento

def test_adicionar_usuario(client):
    """
    Teste de Integração 1: Valida o fluxo de cadastro de um novo usuário.
    Enviaremos um POST para a rota /adicionar simulando o formulário HTML.
    O banco que receberá isso será o banco em memória (SQLite) configurado na fixture.
    """
    response = client.post('/adicionar', data={
        'txtCadastroNomeUser': 'Test User',
        'txtCadastroUser': 'testuser',
        'txtCadastroCPF': '12345678900',
        'txtCadastroEmail': 'test@test.com',
        'txtCadastroTel': '11999999999',
        'txtCadastroSenha': 'mypassword',
        'txtRua': 'Rua Teste',
        'txtBairro': 'Bairro Teste'
    }, follow_redirects=True)

    # Verifica se a requisição resultou em 200 OK (após redirecionamento da página de sucesso)
    assert response.status_code == 200

    # Verifica se o usuário de fato entrou no banco testado localmente
    usuario = Usuario.query.filter_by(login_usuario='testuser').first()
    assert usuario is not None
    assert usuario.nome == 'Test User'

# Utilizamos o decorador patch para mockar a 'requests.get' que a nossa aplicação chama.
# A função 'mock_get' entrará exatamente no lugar de 'requests.get' no nosso código,
# isolando a necessidade de conectar à internet.
@patch('webapp.requests.get')
def test_agendamento_mock_api_externa(mock_get, client):
    """
    Teste Unitário/Integração com Mock: 
    Testa a criação do agendamento validando como o sistema lida 
    com o retorno do calendário (A API do Brasil). Aqui nós interceptamos
    (mockamos) a chamada a requests.get evitando requisições reais.
    """

    # Primeiro, preparamos o banco com um usuário para que possamos logar
    usuario = Usuario(
        cpf=987654321, 
        nome='Mock User', 
        login_usuario='mockuser', 
        email='mock@test.com', 
        telefone='11888888888', 
        senha='senha', 
        rua='', 
        bairro=''
    )
    db.session.add(usuario)
    db.session.commit()

    # Temos que simular um login, pois a rota exige "session['usuario_logado']".
    # Usamos o 'with client.session_transaction()' do pytest-flask (ou built-in test_client)
    with client.session_transaction() as sess:
        sess['usuario_logado'] = 'mockuser'

    # Configuramos nosso mock: quando requests.get() for chamado,
    # ele irá retornar um objeto simulado cuja propriedade .status_code = 200
    # e .json() retorna a lista vazia (nenhum feriado), permitindo que grave o agendamento.
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"date": "2024-01-01", "name": "Confraternização Universal"}]

    # Realiza um agendamento num dia LIMPO (10 de agosto, não está no mock de feriados acima)
    response = client.post('/enviarAgendamento', data={
        'data': '10/08/2026',
        'horario': '14:00'
    }, follow_redirects=True)

    # Garante o status de sucesso na navegação
    assert response.status_code == 200
    
    # Verifica se mock foi realmente acionado, evitando a fuga para internet real
    mock_get.assert_called_once()

    # Confirma que foi gravado
    agendamento = Agendamento.query.filter_by(dataAgendamento='10/08/2026').first()
    assert agendamento is not None
    assert int(agendamento.cpf) == 987654321

def test_api_agendamentos_json_fornecimento(client):
    """
    Teste de API: Valida o Requiremento Extra - Verifica se a rota da 
    API rest de agendamentos está respondendo corretamente num Array JSON com os agendamentos.
    """
    # Preparando massa de dados no banco Mockado
    agendamento_mock = Agendamento(
        cpf=111222333,
        dataAgendamento='01/01/2026',
        horaAgendamento='08:00'
    )
    db.session.add(agendamento_mock)
    db.session.commit()

    # Faz o requerimento no endpoint que fornece a API
    response = client.get('/api/agendamentos')

    # Valida código de status HTTP que informa sucesso
    assert response.status_code == 200
    
    # Isola a resposta em objeto JSON nativo
    json_data = response.get_json()

    # Valida a tipagem e se está correto
    assert isinstance(json_data, list)
    assert len(json_data) >= 1
    
    # Varre por item conhecido
    encontrado = any(item['cpf_cliente'] == 111222333 for item in json_data)
    assert encontrado is True
