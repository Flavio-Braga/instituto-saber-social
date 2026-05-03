from db import db


class Unidade(db.Model):
    __tablename__ = 'unidades'

    id_unidade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    turmas = db.relationship('Turma', backref='unidade', lazy=True, cascade='all, delete-orphan')
    colaboradores = db.relationship('Colaborador', backref='unidade', lazy=True, cascade='all, delete-orphan')

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo


class Atendido(db.Model):
    __tablename__ = 'atendidos'

    id_atendido = db.Column(db.Integer, primary_key=True)
    id_turma = db.Column(db.Integer, db.ForeignKey('turmas.id_turma'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean(), default=True, nullable=False)

    frequencias = db.relationship('Frequencia', backref='atendido', lazy=True, cascade='all, delete-orphan')

    def __init__(self, id_turma, nome, status=True):
        self.id_turma = id_turma
        self.nome = nome
        self.status = status


class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id_colaborador = db.Column(db.Integer, primary_key=True)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidades.id_unidade'), nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))

    frequencias = db.relationship('Frequencia', backref='colaborador', lazy=True, cascade='all, delete-orphan')

    def __init__(self, id_unidade, nome_completo, senha, cargo, email, telefone=None):
        self.id_unidade = id_unidade
        self.nome_completo = nome_completo
        self.senha = senha
        self.cargo = cargo
        self.email = email
        self.telefone = telefone


class Turma(db.Model):
    __tablename__ = 'turmas'

    id_turma = db.Column(db.Integer, primary_key=True)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidades.id_unidade'), nullable=False)
    nome = db.Column(db.String(10), nullable=False)
    turno = db.Column(db.String(20), nullable=False)

    atendidos = db.relationship('Atendido', backref='turma', lazy=True, cascade='all, delete-orphan')
    frequencias = db.relationship('Frequencia', backref='turma', lazy=True, cascade='all, delete-orphan')

    def __init__(self, id_unidade, nome, turno):
        self.id_unidade = id_unidade
        self.nome = nome
        self.turno = turno


class Frequencia(db.Model):
    __tablename__ = 'frequencias'

    id_registro = db.Column(db.Integer, primary_key=True)
    id_atendido = db.Column(db.Integer, db.ForeignKey('atendidos.id_atendido'), nullable=False)
    id_turma = db.Column(db.Integer, db.ForeignKey('turmas.id_turma'), nullable=False)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('colaboradores.id_colaborador'), nullable=False)
    data_encontro = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean(), nullable=False)

    def __init__(self, id_atendido, id_turma, id_colaborador, data_encontro, presente):
        self.id_atendido = id_atendido
        self.id_turma = id_turma
        self.id_colaborador = id_colaborador
        self.data_encontro = data_encontro
        self.presente = presente
