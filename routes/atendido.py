from flask import Blueprint, render_template, request
from models import Atendido, Turma
from db import db

atendido_route = Blueprint('atendido', __name__)

"""

Rota de Atendido

 - /atendido/ (GET) - Lista os Atendidos cadastrados
 - /atendido/ (POST) - Insere um Atendido no servidor
 - /atendido/new (GET) - Renderizar um formulário para criar um Atendido
 - /atendido/<id> (GET) - Obter os dados de um Atendido
 - /atendido/<id>/edit (GET) - Renderizar um formulário para editar um Atendido
 - /atendido/<id>/update (PUT) - Atualizar os dados de um Atendido
 - /atendido/<id>/delete (DELETE) - Deletar os dados de um Atendido

"""


@atendido_route.route('/')
def lista_atendido():
    """ listar os atendidos """
    atendidos = Atendido.query.all()
    return render_template('lista_atendido.html', db=atendidos)


@atendido_route.route('/', methods=['POST'])
def inserir_atendido():
    """ inserir os dados do atendido """
    id_turma = request.form["turmaForm"]
    nome = request.form["nomeForm"]
    status = request.form.get("statusForm") == 'on'

    novo_atendido = Atendido(
        id_turma=id_turma,
        nome=nome,
        status=status,
    )
    db.session.add(novo_atendido)
    db.session.commit()

    return render_template("item_atendido.html", atendido=novo_atendido)


@atendido_route.route('/new')
def form_new_atendido():
    """ formulário para criar atendido """
    turmas = Turma.query.all()
    return render_template('form_atendido.html', turmas=turmas)


@atendido_route.route('/<int:atendido_id>')
def detalhe_atendido(atendido_id):
    """ exibir informações do atendido """
    atendido = db.get_or_404(Atendido, atendido_id)
    return render_template('detalhe_atendido.html', atendido=atendido)


@atendido_route.route('/<int:atendido_id>/edit')
def form_edit_atendido(atendido_id):
    """ formulário para editar informações do atendido """
    atendido = db.get_or_404(Atendido, atendido_id)
    turmas = Turma.query.all()
    return render_template('form_edit_atendido.html', atendido=atendido, turmas=turmas)


@atendido_route.route('/<int:atendido_id>/update', methods=['PUT'])
def atualizar_atendido(atendido_id):
    """ atualizar informações do atendido """
    atendido = db.get_or_404(Atendido, atendido_id)

    atendido.id_turma = request.form["turmaForm"]
    atendido.nome = request.form["nomeForm"]
    atendido.status = request.form.get("statusForm") == 'on'

    db.session.commit()

    return render_template("item_atendido.html", atendido=atendido)


@atendido_route.route('/<int:atendido_id>/delete', methods=['DELETE'])
def deletar_atendido(atendido_id):
    """ deletar dados do atendido """
    atendido = Atendido.query.get(atendido_id)

    if atendido:
        db.session.delete(atendido)
        db.session.commit()

    return ''
