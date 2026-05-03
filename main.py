from flask import Flask, render_template, request
from db import db
from routes.colaborador import colaborador_route
from routes.home import home_route

# Setup
app = Flask(__name__)
app.register_blueprint(colaborador_route, url_prefix='/colaborador')
app.register_blueprint(home_route)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    from models import Usuario
    
    if request.method == "POST":
        nome = request.form["nomeForm"]
        senha = request.form["senhaForm"]

        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario and usuario.senha == senha:
            return render_template("index.html")

        return render_template("login.html", error="Usuário ou senha inválidos")
    return render_template("login.html")

# Aplicação
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
