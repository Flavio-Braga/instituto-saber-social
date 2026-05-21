from flask import Flask, render_template, request, redirect, url_for, session
from db import db
from routes.colaborador import colaborador_route
from routes.home import home_route
from routes.unidade import unidade_route

# Setup
app = Flask(__name__)
app.register_blueprint(colaborador_route, url_prefix='/colaborador')
app.register_blueprint(home_route)
app.register_blueprint(unidade_route, url_prefix='/unidade')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "sua-chave-secreta-aqui"
db.init_app(app)


@app.before_request
def verificar_login():
    rotas_publicas = ["/login"]
    if request.path in rotas_publicas or request.path.startswith("/static"):
        return
    if "usuario_logado" not in session:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    from models import Colaborador

    if request.method == "POST":
        nome = request.form["nomeForm"]
        senha = request.form["senhaForm"]

        colaborador = Colaborador.query.filter_by(nome_completo=nome).first()
        if colaborador and colaborador.senha == senha:
            session["usuario_logado"] = colaborador.id_colaborador
            return redirect(url_for("home.home"))

        return render_template("login.html", error="Usuário ou senha inválidos")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Aplicação
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
