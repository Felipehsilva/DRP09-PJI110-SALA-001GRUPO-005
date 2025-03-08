from flask import Flask, render_template, request, redirect,session , flash, url_for


class Usuario:
    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha

usuario01 = Usuario('Felipe','felipe','admin')
usuario02 = Usuario('Ze Ruela','zruela','1234')
usuario03 = Usuario('joao','joao','654321')

usuarios = {
    usuario01.login:usuario01,
    usuario02.login:usuario02,
    usuario03.login:usuario03
}



app = Flask(__name__)

app.secret_key = 'aprendendodoiniciocomdaniel'

#@app.route("/") # se colocar só / vira a homeage

#@app.route("/logingpt") 
#def testRedirect():
 #   return render_template('login-gpt.html',
                           
#                           titulo = "Pagina de Login de teste"
                           
#                           )
                          

@app.route("/login") 
def logar():
    return render_template('login.html',
                           
                           titulo = "Pagina de Login"
                           
                           )

@app.route('/autenticar',methods=['POST',]) 
def autenticar():
    if request.form['txtLogin'] in usuarios:
        usuarioEncontrado = usuarios[request.form['txtLogin']]
        if request.form['txtSenha'] == usuarioEncontrado.senha:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuario {usuarioEncontrado.login} Logado com sucesso!")
            return redirect(url_for('cadastrarUsusario'))
        else:
            flash("Senha Invalida")
            return redirect(url_for('logar'))
    else:
        flash("Usuario/Senha invalida")
        return redirect(url_for('logar'))
    



@app.route("/cadastrar") 
def cadastrarUsusario():
    return render_template('cadastrar.html',
                           
                           titulo = "Cadastrar"
                           
                           )

@app.route("/agendar") 
def agendar():
    return render_template('agendar.html',
                           
                           titulo = "Agendar"
                           
                           )


@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('logar'))



app.run(debug=True)# debug = True evita ter que rodar manualmente o flask apos cada atualizacao no codigo

