# Imports
from flask import Flask
from db import db
from routes.colaborador import colaborador_route
from routes.home import home_route

# Setup
app = Flask(__name__)
app.register_blueprint(colaborador_route, url_prefix='/colaborador')
app.register_blueprint(home_route)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

## Rotas
# Rota - Login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         nome = request.form["nomeForm"]
#         senha = request.form["senhaForm"]

#         if db.session().query(Usuario).filter_by(nome=nome).first():
#             if db.session().query(Usuario).filter_by(senha=senha).first():
#                 return render_template("home.html")

#         return "Login não existe"
#     return render_template("login.html")

# Aplicação
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
