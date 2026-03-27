from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(15))
    senha = db.Column(db.String())
    email = db.Column(db.String(30))
    cargo = db.Column(db.String())
    esta_ativo = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, nome, senha, email, cargo):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cargo = cargo

class Atendido(db.Model):
    __tablename__ = 'atendidos'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30))
    nis = db.Column(db.Integer)

