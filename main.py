from flask import Flask, request, redirect, url_for
from flask_login import current_user

from config import Config
from db import db
from auth import login_manager

# Feature blueprints (core system)
from routes.auth import auth_route
from routes.chamada import chamada_route
from routes.relatorios import relatorios_route

# Admin CRUD blueprints (existing)
from routes.colaborador import colaborador_route
from routes.home import home_route
from routes.unidade import unidade_route
from routes.turma import turma_route
from routes.atendido import atendido_route
from routes.frequencia import frequencia_route

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# Core screens (login, attendance, reports) at the root.
app.register_blueprint(auth_route)
app.register_blueprint(chamada_route)
app.register_blueprint(relatorios_route)

# Existing admin CRUD, kept under their own prefixes.
app.register_blueprint(home_route)
app.register_blueprint(colaborador_route, url_prefix="/colaborador")
app.register_blueprint(unidade_route, url_prefix="/unidade")
app.register_blueprint(turma_route, url_prefix="/turma")
app.register_blueprint(atendido_route, url_prefix="/atendido")
app.register_blueprint(frequencia_route, url_prefix="/frequencia")

# Endpoints reachable without authentication.
PUBLIC_ENDPOINTS = {"auth.login", "static"}


@app.before_request
def require_login():
    if request.endpoint is None or request.endpoint in PUBLIC_ENDPOINTS:
        return
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.path))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
