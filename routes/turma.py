from flask import Blueprint, render_template, request
from models import Turma, Unidade
from db import db

turma_route = Blueprint('turma', __name__)

"""

Rota de Turma

 - /turma/ (GET) - Lista as Turmas cadastradas
 - /turma/ (POST) - Insere uma Turma no servidor
 - /turma/new (GET) - Renderizar um formulário para criar uma Turma
 - /turma/<id> (GET) - Obter os dados de uma Turma
 - /turma/<id>/edit (GET) - Renderizar um formulário para editar uma Turma
 - /turma/<id>/update (PUT) - Atualizar os dados de uma Turma
 - /turma/<id>/delete (DELETE) - Deletar os dados de uma Turma

"""


@turma_route.route('/')
def lista_turma():
    """ listar as turmas """
    turmas = Turma.query.all()
    return render_template('lista_turma.html', db=turmas)


@turma_route.route('/', methods=['POST'])
def inserir_turma():
    """ inserir os dados da turma """
    id_unidade = request.form["unidadeForm"]
    nome = request.form["nomeForm"]
    turno = request.form["turnoForm"]

    nova_turma = Turma(
        id_unidade=id_unidade,
        nome=nome,
        turno=turno,
    )
    db.session.add(nova_turma)
    db.session.commit()

    return render_template("item_turma.html", turma=nova_turma)


@turma_route.route('/new')
def form_new_turma():
    """ formulário para criar turma """
    unidades = Unidade.query.all()
    return render_template('form_turma.html', unidades=unidades)


@turma_route.route('/<int:turma_id>')
def detalhe_turma(turma_id):
    """ exibir informações da turma """
    turma = db.get_or_404(Turma, turma_id)
    return render_template('detalhe_turma.html', turma=turma)


@turma_route.route('/<int:turma_id>/edit')
def form_edit_turma(turma_id):
    """ formulário para editar informações da turma """
    turma = db.get_or_404(Turma, turma_id)
    unidades = Unidade.query.all()
    return render_template('form_edit_turma.html', turma=turma, unidades=unidades)


@turma_route.route('/<int:turma_id>/update', methods=['PUT'])
def atualizar_turma(turma_id):
    """ atualizar informações da turma """
    turma = db.get_or_404(Turma, turma_id)

    turma.id_unidade = request.form["unidadeForm"]
    turma.nome = request.form["nomeForm"]
    turma.turno = request.form["turnoForm"]

    db.session.commit()

    return render_template("item_turma.html", turma=turma)


@turma_route.route('/<int:turma_id>/delete', methods=['DELETE'])
def deletar_turma(turma_id):
    """ deletar dados da turma """
    turma = Turma.query.get(turma_id)

    if turma:
        db.session.delete(turma)
        db.session.commit()

    return ''
