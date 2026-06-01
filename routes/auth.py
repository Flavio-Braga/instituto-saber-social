from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models import Colaborador
from security import check_password
from auth import LoginUser

auth_route = Blueprint("auth", __name__)


@auth_route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        colaborador = Colaborador.query.filter_by(email=email).first()
        if colaborador and check_password(password, colaborador.senha):
            login_user(LoginUser(colaborador))
            next_url = request.args.get("next")
            return redirect(next_url or url_for("chamada.chamada"))

        return render_template("login.html", error="E-mail ou senha inválidos.")

    return render_template("login.html")


@auth_route.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("auth.login"))
