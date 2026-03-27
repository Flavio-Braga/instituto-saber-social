#Imports
from flask import Flask, render_template, request
from db import db
from models import Usuario

#Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)


### Rotas
#Rota - Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        return 'Login enviado'
    return render_template('login.html')

#Rota - Registrar Login
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':

        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        email = request.form['emailForm']
        cargo = request.form['cargoForm']

        novo_usuario = Usuario(nome=nome, senha=senha, email=email, cargo=cargo)
        db.session.add(novo_usuario)
        db.session.commit()

        print(novo_usuario.nome)
        print(novo_usuario.senha)
        print(novo_usuario.email)
        print(novo_usuario.cargo)
        return render_template('registrar_login.html')
    return render_template('registrar_login.html')

#Aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)