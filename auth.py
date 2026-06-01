"""Flask-Login integration.

The Colaborador model is intentionally left untouched (no UserMixin). Instead we
wrap it in a lightweight adapter that exposes the interface Flask-Login expects
and transparently proxies every other attribute back to the Colaborador row.
"""

from flask_login import LoginManager

from db import db
from models import Colaborador

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para continuar."


class LoginUser:
    """Adapter that gives a Colaborador the Flask-Login user interface."""

    def __init__(self, colaborador: Colaborador):
        self.colaborador = colaborador

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.colaborador.id_colaborador)

    def __getattr__(self, name):
        # Only reached for attributes not defined on LoginUser itself.
        if name == "colaborador":
            raise AttributeError(name)
        return getattr(self.colaborador, name)


@login_manager.user_loader
def load_user(user_id: str):
    colaborador = db.session.get(Colaborador, int(user_id))
    return LoginUser(colaborador) if colaborador else None
