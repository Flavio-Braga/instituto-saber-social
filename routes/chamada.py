from datetime import date, datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user

from db import db
from models import Turma, Atendido, Frequencia

chamada_route = Blueprint("chamada", __name__)


def _parse_date(value):
    """Parse a YYYY-MM-DD string, falling back to today on empty/invalid input."""
    if not value:
        return date.today()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return date.today()


def _turma_da_unidade(turma_id):
    """Return the Turma if it belongs to the logged-in collaborator's unit, else None."""
    if not turma_id:
        return None
    turma = db.session.get(Turma, turma_id)
    if turma and turma.id_unidade == current_user.id_unidade:
        return turma
    return None


@chamada_route.route("/chamada", methods=["GET"])
@login_required
def chamada():
    # Only classes from the collaborator's own unit.
    turmas = (
        Turma.query.filter_by(id_unidade=current_user.id_unidade)
        .order_by(Turma.turno, Turma.nome)
        .all()
    )

    data_encontro = _parse_date(request.args.get("data"))
    turma_id = request.args.get("turma_id", type=int)
    turma = _turma_da_unidade(turma_id)

    atendidos = []
    estado = {}  # id_atendido -> presente (bool)
    if turma:
        atendidos = (
            Atendido.query.filter_by(id_turma=turma.id_turma, status=True)
            .order_by(Atendido.nome)
            .all()
        )
        registros = Frequencia.query.filter_by(
            id_turma=turma.id_turma, data_encontro=data_encontro
        ).all()
        estado = {r.id_atendido: r.presente for r in registros}

    ja_registrada = len(estado) > 0
    presentes = sum(1 for v in estado.values() if v)

    return render_template(
        "chamada.html",
        turmas=turmas,
        turma=turma,
        atendidos=atendidos,
        estado=estado,
        data_encontro=data_encontro,
        data_str=data_encontro.isoformat(),
        ja_registrada=ja_registrada,
        presentes_iniciais=presentes,
    )


@chamada_route.route("/chamada", methods=["POST"])
@login_required
def salvar_chamada():
    turma_id = request.form.get("turma_id", type=int)
    data_encontro = _parse_date(request.form.get("data"))
    turma = _turma_da_unidade(turma_id)

    if not turma:
        abort(403)

    atendidos = Atendido.query.filter_by(id_turma=turma.id_turma, status=True).all()

    # Existing records for this class/date, keyed for an in-place upsert.
    existentes = {
        r.id_atendido: r
        for r in Frequencia.query.filter_by(
            id_turma=turma.id_turma, data_encontro=data_encontro
        ).all()
    }

    for atendido in atendidos:
        presente = request.form.get(f"present_{atendido.id_atendido}") == "1"
        registro = existentes.get(atendido.id_atendido)
        if registro:
            registro.presente = presente
            registro.id_colaborador = current_user.id_colaborador
        else:
            db.session.add(
                Frequencia(
                    id_atendido=atendido.id_atendido,
                    id_turma=turma.id_turma,
                    id_colaborador=current_user.id_colaborador,
                    data_encontro=data_encontro,
                    presente=presente,
                )
            )

    db.session.commit()
    flash("Chamada salva com sucesso!", "success")
    return redirect(
        url_for("chamada.chamada", turma_id=turma.id_turma, data=data_encontro.isoformat())
    )


@chamada_route.route("/api/turmas", methods=["GET"])
@login_required
def api_turmas():
    """Return classes for a given unit as JSON (used by the reports filters)."""
    unidade_id = request.args.get("unidade_id", type=int)
    query = Turma.query
    if unidade_id:
        query = query.filter_by(id_unidade=unidade_id)
    turmas = query.order_by(Turma.turno, Turma.nome).all()
    return jsonify(
        [
            {"id_turma": t.id_turma, "nome": t.nome, "turno": t.turno}
            for t in turmas
        ]
    )
