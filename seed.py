"""Popula o banco de dados com dados de demonstração para desenvolvimento.

Uso:
    python seed.py

Este script APAGA e recria todas as tabelas e carrega:
  - 3 unidades (1 sede + 2 filiais)
  - 2 turmas por unidade (Turma A / Manhã, Turma B / Tarde)
  - 1 colaborador por unidade (e-mail de login + senha "admin123")
  - 10 atendidos por turma
  - ~30 registros de frequência por atendido em dias úteis (70-90% presente)
"""

import random
from datetime import date, timedelta

from flask import Flask

from config import Config
from db import db
from models import Unidade, Turma, Atendido, Colaborador, Frequencia
from security import hash_password

random.seed(42)

FIRST_NAMES = [
    "Ana", "João", "Maria", "Pedro", "Lucas", "Júlia", "Gabriel", "Beatriz",
    "Rafael", "Larissa", "Matheus", "Sophia", "Enzo", "Helena", "Davi",
    "Manuela", "Bernardo", "Valentina", "Miguel", "Laura", "Arthur", "Alice",
    "Heitor", "Cecília", "Theo", "Isabela", "Gustavo", "Lívia", "Felipe", "Yasmin",
]

LAST_NAMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Pereira", "Costa",
    "Rodrigues", "Almeida", "Nascimento", "Carvalho", "Gomes", "Martins",
    "Araújo", "Ribeiro", "Ferreira", "Barbosa", "Rocha", "Dias", "Teixeira",
]

UNIDADES = [
    {"nome": "Sede", "tipo": "sede", "email": "orientadora@sede.com", "colab": "Fernanda Alves"},
    {"nome": "Unidade 2", "tipo": "filial", "email": "orientadora@unidade2.com", "colab": "Patrícia Mendes"},
    {"nome": "Unidade 3", "tipo": "filial", "email": "orientadora@unidade3.com", "colab": "Camila Rocha"},
]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def weekday_sessions(num_sessions):
    """Retorna os últimos `num_sessions` dias úteis, terminando ontem (hoje fica vazio)."""
    days = []
    cursor = date.today() - timedelta(days=1)
    while len(days) < num_sessions:
        if cursor.weekday() < 5:  # Seg-Sex
            days.append(cursor)
        cursor -= timedelta(days=1)
    return sorted(days)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        senha_hash = hash_password("admin123")
        sessions = weekday_sessions(30)

        for u in UNIDADES:
            unidade = Unidade(nome=u["nome"], tipo=u["tipo"])
            db.session.add(unidade)
            db.session.flush()  # gera id_unidade

            colaborador = Colaborador(
                id_unidade=unidade.id_unidade,
                nome_completo=u["colab"],
                senha=senha_hash,
                cargo="Orientadora Social",
                email=u["email"],
                telefone=None,
            )
            db.session.add(colaborador)
            db.session.flush()

            for nome, turno in (("A", "Manhã"), ("B", "Tarde")):
                turma = Turma(id_unidade=unidade.id_unidade, nome=nome, turno=turno)
                db.session.add(turma)
                db.session.flush()

                for _ in range(10):
                    atendido = Atendido(id_turma=turma.id_turma, nome=random_name(), status=True)
                    db.session.add(atendido)
                    db.session.flush()

                    # Cada atendido tem uma taxa-base pessoal de presença entre 70% e 90%.
                    base_rate = random.uniform(0.70, 0.90)
                    for dia in sessions:
                        db.session.add(
                            Frequencia(
                                id_atendido=atendido.id_atendido,
                                id_turma=turma.id_turma,
                                id_colaborador=colaborador.id_colaborador,
                                data_encontro=dia,
                                presente=random.random() < base_rate,
                            )
                        )

        db.session.commit()

        print("Seed concluído.")
        print(f"  Unidades:      {Unidade.query.count()}")
        print(f"  Turmas:        {Turma.query.count()}")
        print(f"  Atendidos:     {Atendido.query.count()}")
        print(f"  Colaboradores: {Colaborador.query.count()}")
        print(f"  Frequências:   {Frequencia.query.count()} registros")
        print("\nLogin: orientadora@sede.com / admin123")


if __name__ == "__main__":
    seed()
