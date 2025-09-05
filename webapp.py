from flask import Flask, render_template, request, redirect,jsonify, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'PI1'

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='avnadmin',
        senha='AVNS_3NuM-f_GZn4ASvN5Glb',
        servidor='mysql-3369c770-felipehenriquedasilva-8135.h.aivencloud.com:11802',
        database='defaultdb'
    )

db = SQLAlchemy(app)

# Configuração do Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'felipehenriquedasilva2008@gmail.com'  # Seu e-mail Gmail
app.config['MAIL_PASSWORD'] = 'spcw fsik hjoq txdq'  # Senha gerada no Gmail (App Password)
app.config['MAIL_DEFAULT_SENDER'] = ('Barbearia', 'felipehenriquedasilva2008@gmail.com')

mail = Mail(app)

# ---------------------------
# MODELOS
# ---------------------------
class Usuario(db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)

class Agendamento(db.Model):
    cpf = db.Column(db.Integer, nullable=False)
    dataAgendamento = db.Column(db.String(50), primary_key=True)
    horaAgendamento = db.Column(db.String(50), primary_key=True)

# ---------------------------
# FUNÇÃO PARA ENVIAR E-MAIL
# ---------------------------
def enviar_email(destinatario, assunto, corpo):
    try:
        msg = Message(subject=assunto, recipients=[destinatario])
        msg.body = corpo
        mail.send(msg)
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# ---------------------------
# ROTAS
# ---------------------------
@app.route("/")
def logar():
    return render_template('login.html', titulo="Página de Login")

@app.route("/logar")
def logar_redirect():
    return render_template('login.html', titulo="Página de Login")

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuario.query.filter_by(login_usuario=request.form['txtLogin']).first()
    if usuario:
        if request.form['txtSenha'] == usuario.senha:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuário {usuario.login_usuario} logado com sucesso!")
            return redirect(url_for('meus_agendamentos'))
        else:
            flash("Senha inválida")
            return redirect(url_for('logar'))
    else:
        flash("Usuário/Senha inválida")
        return redirect(url_for('logar'))

@app.route("/cadastrar")
def cadastrarUsuario():
    return render_template('cadastrar.html', titulo="Cadastrar")

@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['txtCadastroNomeUser']
    user = request.form['txtCadastroUser']
    cpf = request.form['txtCadastroCPF']
    email = request.form['txtCadastroEmail']
    telefone = request.form['txtCadastroTel']
    senha = request.form['txtCadastroSenha']

    usuario = Usuario.query.filter_by(login_usuario=user).first()
    cpf_usuario = Usuario.query.filter_by(cpf=cpf).first()

    if usuario:
        flash("Usuário já cadastrado")
        return redirect(url_for('cadastrarUsuario'))
    if cpf_usuario:
        flash("CPF já cadastrado")
        return redirect(url_for('cadastrarUsuario'))

    novo_user = Usuario(cpf=cpf, login_usuario=user, nome=nome, email=email, telefone=telefone, senha=senha)
    db.session.add(novo_user)
    db.session.commit()
    return redirect(url_for('cadastroSucesso'))

@app.route("/cadastroSucesso")
def cadastroSucesso():
    return render_template('success-registration.html', titulo="Registro Concluído com Sucesso")

@app.route("/agendar")
def agendar():
    if 'usuario_logado' not in session or not session['usuario_logado']:
        return redirect(url_for('logar'))

    # Pega todos os agendamentos existentes
    agendamentos = Agendamento.query.all()

    # Cria uma lista com tuplas (data, hora)
    horarios_ocupados = [(a.dataAgendamento, a.horaAgendamento) for a in agendamentos]

    return render_template('agendar.html', horarios_ocupados=horarios_ocupados)


@app.route('/horarios_ocupados')
def horarios_ocupados():
    data = request.args.get('data')  # Pega a data da query string
    agendamentos = Agendamento.query.filter_by(dataAgendamento=data).all()
    horarios = [a.horaAgendamento for a in agendamentos]
    return jsonify({"ocupados": horarios})


@app.route('/enviarAgendamento', methods=['POST'])
def adicionar_agendamento():
    dataEscolhida = request.form['data']
    horarioEscolhido = request.form['horario']
    user = session.get('usuario_logado')

    if not user:
        flash("Você precisa estar logado para agendar.")
        return redirect(url_for('logar'))

    usuario = Usuario.query.filter_by(login_usuario=user).first()
    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('logar'))

    agendamento_existente = Agendamento.query.filter_by(
        dataAgendamento=dataEscolhida,
        horaAgendamento=horarioEscolhido
    ).first()

    if agendamento_existente:
        flash("Este horário já está agendado. Por favor, escolha outro.")
        return redirect(url_for('agendar'))

    novo_agendamento = Agendamento(
        cpf=usuario.cpf,
        dataAgendamento=dataEscolhida,
        horaAgendamento=horarioEscolhido
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    # Enviar e-mail de confirmação
    enviar_email(
        usuario.email,
        "Confirmação de Agendamento",
        f"Olá {usuario.nome}, seu agendamento foi realizado com sucesso!\n"
        f"Data: {dataEscolhida}\nHorário: {horarioEscolhido}\nObrigado por escolher nossa barbearia!"
    )

    flash("Agendamento realizado com sucesso!")
    return redirect(url_for('agendar'))

@app.route("/meus_agendamentos")
def meus_agendamentos():
    if session.get('usuario_logado') is None:
        flash("Você precisa estar logado para ver seus agendamentos.")
        return redirect(url_for('logar'))

    user = session['usuario_logado']
    usuario = Usuario.query.filter_by(login_usuario=user).first()

    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('logar'))

    agendamentos = Agendamento.query.filter_by(cpf=usuario.cpf).all()
    return render_template("agendamentos.html", agendamentos=agendamentos, titulo="Meus Agendamentos")

@app.route('/remover_agendamento', methods=['POST'])
def remover_agendamento():
    data = request.form.get('data')
    hora = request.form.get('hora')

    agendamento = Agendamento.query.get((data, hora))
    if agendamento:
        db.session.delete(agendamento)
        db.session.commit()

        # Enviar e-mail informando o cancelamento
        user = session.get('usuario_logado')
        usuario = Usuario.query.filter_by(login_usuario=user).first()
        if usuario:
            enviar_email(
                usuario.email,
                "Cancelamento de Agendamento",
                f"Olá {usuario.nome}, seu agendamento para {data} às {hora} foi cancelado com sucesso."
            )

        flash('Agendamento removido com sucesso!', 'success')
    else:
        flash('Agendamento não encontrado!', 'danger')

    return redirect(url_for('meus_agendamentos'))

@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('logar'))

if __name__ == '__main__':
    app.run(debug=True)