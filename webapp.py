from flask import Flask, render_template, request, redirect,session , flash






app = Flask(__name__)

app.secret_key = 'aprendendodoiniciocomdaniel'

#@app.route("/") # se colocar só / vira a homeage

#@app.route("/logingpt") 
#def testRedirect():
 #   return render_template('login-gpt.html',
                           
#                           titulo = "Pagina de Login de teste"
                           
#                           )
                          

@app.route("/login") 
def Logar():
    return render_template('login.html',
                           
                           titulo = "Pagina de Login"
                           
                           )

@app.route('/autenticar',methods=['POST',]) 
def autenticar():
    if request.form['txtSenha'] == 'admin':
        session['usuario_logado'] = request.form['txtLogin']
        flash("Usuario Logado com sucesso!")
        return redirect('/agendar')
    else:
        flash("Usuario/Senha invalida")
        return redirect("/login")
    



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
    return redirect('/login')




app.run(debug=True)# debug = True evita ter que rodar manualmente o flask apos cada atualizacao no codigo

