from flask import Blueprint, render_template, request
from models import Unidade
from db import db

unidade_route = Blueprint('unidade', __name__)

"""

Rota de Unidade

 - /unidade/ (GET) - Lista as Unidades cadastradas
 - /unidade/ (POST) - Insere uma Unidade no servidor
 - /unidade/new (GET) - Renderizar um formulário para criar uma Unidade
 - /unidade/<id> (GET) - Obter os dados de uma Unidade
 - /unidade/<id>/edit (GET) - Renderizar um formulário para editar uma Unidade
 - /unidade/<id>/update (PUT) - Atualizar os dados de uma Unidade
 - /unidade/<id>/delete (DELETE) - Deletar os dados de uma Unidade

"""


@unidade_route.route('/')
def lista_unidade():
    """ listar as unidades """
    unidades = Unidade.query.all()
    return render_template('lista_unidade.html', db=unidades)


@unidade_route.route('/', methods=['POST'])
def inserir_unidade():
    """ inserir os dados da unidade """
    nome = request.form["nomeForm"]
    tipo = request.form["tipoForm"]

    nova_unidade = Unidade(
        nome=nome,
        tipo=tipo,
    )
    db.session.add(nova_unidade)
    db.session.commit()

    return render_template("item_unidade.html", unidade=nova_unidade)


@unidade_route.route('/new')
def form_new_unidade():
    """ formulário para criar unidade """
    return render_template('form_unidade.html')


@unidade_route.route('/<int:unidade_id>')
def detalhe_unidade(unidade_id):
    """ exibir informações da unidade """
    unidade = db.get_or_404(Unidade, unidade_id)
    return render_template('detalhe_unidade.html', unidade=unidade)


@unidade_route.route('/<int:unidade_id>/edit')
def form_edit_unidade(unidade_id):
    """ formulário para editar informações da unidade """
    unidade = db.get_or_404(Unidade, unidade_id)
    return render_template('form_edit_unidade.html', unidade=unidade)


@unidade_route.route('/<int:unidade_id>/update', methods=['PUT'])
def atualizar_unidade(unidade_id):
    """ atualizar informações da unidade """
    unidade = db.get_or_404(Unidade, unidade_id)

    unidade.nome = request.form["nomeForm"]
    unidade.tipo = request.form["tipoForm"]

    db.session.commit()

    return render_template("item_unidade.html", unidade=unidade)


@unidade_route.route('/<int:unidade_id>/delete', methods=['DELETE'])
def deletar_unidade(unidade_id):
    """ deletar dados da unidade """
    unidade = Unidade.query.get(unidade_id)

    if unidade:
        db.session.delete(unidade)
        db.session.commit()

    return ''
