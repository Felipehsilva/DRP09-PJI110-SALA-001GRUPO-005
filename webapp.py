from flask import Flask, render_template, request, redirect,session , flash, url_for
from flask_sqlalchemy import SQLAlchemy 





app = Flask(__name__)

app.secret_key = 'PI1'

app.config['SQLALCHEMY_DATABASE_URI'] = \
'{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'avnadmin',
    senha = 'AVNS_3NuM-f_GZn4ASvN5Glb',
    servidor = 'mysql-3369c770-felipehenriquedasilva-8135.h.aivencloud.com:11802',
    database = 'defaultdb'

)

db = SQLAlchemy(app)
                          
class Usuario(db.Model):
    # a variavel tem que ser o mesmo nome do campo da tabela
    cpf = db.Column(db.Integer, primary_key=True)
    nome= db.Column(db.String(100), nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Agendamento(db.Model):
    # a variavel tem que ser o mesmo nome do campo da tabela
    cpf = db.Column(db.Integer, nullable=False)
    dataAgendamento = db.Column(db.String(50), primary_key=True)
    horaAgendamento = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return '<Name %r>' % self.name    


@app.route("/logar") 
def logar():
    return render_template('login.html',
                           
                           titulo = "Pagina de Login"
                           
                           )

@app.route("/") 
def logar1():
    return render_template('login.html',
                           
                           titulo = "Pagina de Login"
                           
                           )

@app.route('/autenticar',methods=['POST',]) 
def autenticar():
    usuario = Usuario.query.filter_by(login_usuario = request.form['txtLogin']).first()
    if usuario:    
        if request.form['txtSenha'] == usuario.senha:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuario {usuario.login_usuario} Logado com sucesso!")
            return redirect(url_for('meus_agendamentos'))
        else:
            flash("Senha Invalida")
            return redirect(url_for('logar'))
    else:
        flash("Usuario/Senha invalida")
        return redirect(url_for('logar'))



@app.route("/cadastrar") 
def cadastrarUsuario():
    return render_template('cadastrar.html',
                           
                           titulo = "Cadastrar"
                           
                           )

@app.route('/adicionar',methods=['POST'])
def adicionar_usuario():
    nome = request.form['txtCadastroNomeUser']
    user = request.form['txtCadastroUser']
    cpf = request.form['txtCadastroCPF']
    email = request.form['txtCadastroEmail']
    telefone = request.form['txtCadastroTel']
    senha = request.form['txtCadastroSenha']
    


    usuario = Usuario.query.filter_by(login_usuario = user).first() 
    cpf_usuario = Usuario.query.filter_by(cpf = cpf).first() 

    if usuario: 
        flash("Usuario ja cadastrado")
        return redirect(url_for('cadastrarUsuario'))
    if cpf_usuario: 
        flash("CPF ja cadastrado")
        return redirect(url_for('cadastrarUsuario'))
    novo_user = Usuario(cpf = cpf, login_usuario = user, nome = nome, email = email, telefone = telefone, senha = senha)
    db.session.add(novo_user)
    db.session.commit()
    return redirect(url_for('cadastroSucesso'))

@app.route("/cadastroSucesso") 
def cadastroSucesso():
    
    
    return render_template('success-registration.html',
                           
                           titulo = "Registro Concluido com Sucesso"
                           
                           )

@app.route("/agendamentos") 
def agendamentos():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('logar'))
    
    return render_template('agendamentos.html',
                           
                           titulo = "agendamentos"
                           
                           )


@app.route("/agendar") 
def agendar():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('logar'))
    
    return render_template('agendar.html',
                           
                           
                           
                           )

@app.route('/enviarAgendamento', methods=['POST'])
def adicionar_agendamento():
    dataEscolhida = request.form['data']
    horarioEscolhido = request.form['horario']
    user = session.get('usuario_logado')  # Usando .get() para evitar erro se não existir

    if not user:
        flash("Você precisa estar logado para agendar.")
        return redirect(url_for('logar'))

    usuario = Usuario.query.filter_by(login_usuario=user).first()

    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('logar'))

    # Verificar se já existe um agendamento no mesmo dia e horário
    agendamento_existente = Agendamento.query.filter_by(
        dataAgendamento=dataEscolhida,
        horaAgendamento=horarioEscolhido
    ).first()

    if agendamento_existente:
        flash("Este horário já está agendado. Por favor, escolha outro.")
        return redirect(url_for('agendar'))

    # Criar um novo agendamento
    novo_agendamento = Agendamento(
        cpf=usuario.cpf,
        dataAgendamento=dataEscolhida,
        horaAgendamento=horarioEscolhido
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    flash("Agendamento realizado com sucesso!")
    return redirect(url_for('agendar'))

@app.route("/meus_agendamentos")
def meus_agendamentos():
    if 'usuario_logado' not in session or not session['usuario_logado']:
        flash("Você precisa estar logado para ver seus agendamentos.")
        return redirect(url_for('logar'))

    user = session['usuario_logado']
    usuario = Usuario.query.filter_by(login_usuario=user).first()

    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('logar'))

    agendamentos = Agendamento.query.filter_by(cpf=usuario.cpf).all()
    
  
    return render_template("agendamentos.html", agendamentos=agendamentos, titulo="Meus Agendamentos")

@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('logar'))





if __name__ == '__main__':
    app.run(debug=True)# debug = True evita ter que rodar manualmente o flask apos cada atualizacao no codigo
    