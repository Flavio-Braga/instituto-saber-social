import csv
import io
from datetime import date, datetime, timedelta

from flask import Blueprint, render_template, request, Response
from flask_login import login_required

from db import db
from models import Unidade, Turma, Atendido, Frequencia

relatorios_route = Blueprint("relatorios", __name__)

MIN_FREQUENCIA = 70.0  # Legal minimum attendance rate (%)


def _parse_date(value, default):
    if not value:
        return default
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return default


def _read_filters():
    """Read and normalize report filters from the request query string."""
    hoje = date.today()
    inicio = _parse_date(request.args.get("inicio"), hoje - timedelta(days=30))
    fim = _parse_date(request.args.get("fim"), hoje)
    return {
        "unidade_id": request.args.get("unidade_id", type=int),
        "turma_id": request.args.get("turma_id", type=int),
        "turno": (request.args.get("turno") or "").strip(),
        "inicio": inicio,
        "fim": fim,
    }


def _build_rows(filters):
    """Compute one report row per matching active atendido."""
    query = (
        Atendido.query.join(Turma, Atendido.id_turma == Turma.id_turma)
        .filter(Atendido.status.is_(True))
    )
    if filters["unidade_id"]:
        query = query.filter(Turma.id_unidade == filters["unidade_id"])
    if filters["turma_id"]:
        query = query.filter(Turma.id_turma == filters["turma_id"])
    if filters["turno"]:
        query = query.filter(Turma.turno == filters["turno"])

    atendidos = query.order_by(Turma.nome, Atendido.nome).all()

    rows = []
    for atendido in atendidos:
        base = Frequencia.query.filter(
            Frequencia.id_atendido == atendido.id_atendido,
            Frequencia.id_turma == atendido.id_turma,
            Frequencia.data_encontro.between(filters["inicio"], filters["fim"]),
        )
        total = base.count()
        presentes = base.filter(Frequencia.presente.is_(True)).count()
        percentual = (presentes / total * 100) if total else 0.0
        rows.append(
            {
                "nome": atendido.nome,
                "turma": atendido.turma.nome,
                "turno": atendido.turma.turno,
                "unidade": atendido.turma.unidade.nome,
                "total": total,
                "presentes": presentes,
                "percentual": round(percentual, 1),
                "abaixo_minimo": total > 0 and percentual < MIN_FREQUENCIA,
            }
        )
    return rows


def _totais(rows):
    total_dias = sum(r["total"] for r in rows)
    total_presentes = sum(r["presentes"] for r in rows)
    media = (total_presentes / total_dias * 100) if total_dias else 0.0
    return {
        "total_dias": total_dias,
        "total_presentes": total_presentes,
        "media": round(media, 1),
        "qtd_atendidos": len(rows),
    }


@relatorios_route.route("/relatorios", methods=["GET"])
@login_required
def relatorios():
    filters = _read_filters()
    rows = _build_rows(filters)
    return render_template(
        "relatorios.html",
        unidades=Unidade.query.order_by(Unidade.nome).all(),
        turmas=Turma.query.order_by(Turma.nome).all(),
        filters=filters,
        rows=rows,
        totais=_totais(rows),
        min_frequencia=MIN_FREQUENCIA,
    )


@relatorios_route.route("/relatorios/export", methods=["GET"])
@login_required
def exportar_csv():
    filters = _read_filters()
    rows = _build_rows(filters)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Nome", "Unidade", "Turma", "Turno", "Total de dias", "Dias presentes", "% de frequência"]
    )
    for r in rows:
        writer.writerow(
            [r["nome"], r["unidade"], r["turma"], r["turno"], r["total"], r["presentes"], r["percentual"]]
        )

    filename = f"frequencia_{filters['inicio'].isoformat()}_{filters['fim'].isoformat()}.csv"
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
