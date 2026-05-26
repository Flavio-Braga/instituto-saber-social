from flask import Blueprint, render_template, request
from models import Colaborador
from db import db

colaborador_route = Blueprint('colaborador', __name__)

"""

Rota de Colaboradores

 - /colaborador/ (GET) - Lista os colaboradores
 - /colaborador/ (POST) - Inserir um colaborador no servidor
 - /colaborador/new (GET) - Renderizar um formulário para criar um colaborador
 - /colaborador/<id> (GET) - Obter os dados de um colaborador
 - /colaborador/<id>/edit (GET) - Renderizar um formulário para editar um colaborador
 - /colaborador/<id>/update (PUT) - Atualizar os dados de um colaborador
 - /colaborador/<id>/delete (DELETE) - Deletar os dados de um colaborador

"""


@colaborador_route.route('/')
def lista_colaborador():
    """ listar os colaboradores """
    colaborador = Colaborador.query.all()
    return render_template('colaborador/lista_colaborador.html', db=colaborador)


@colaborador_route.route('/', methods=['POST'])
def inserir_colaborador():
    """ inserir os dados do colaborador """
    nome = request.form["nomeForm"]
    senha = request.form["senhaForm"]
    email = request.form["emailForm"]
    cargo = request.form["cargoForm"]
    telefone = request.form.get("telefoneForm") or None

    novo_colaborador = Colaborador(
        nome_completo=nome,
        id_unidade=1,
        senha=senha,
        email=email,
        cargo=cargo,
        telefone=telefone,
    )
    db.session.add(novo_colaborador)
    db.session.commit()

    return render_template("colaborador/item_colaborador.html", colaborador=novo_colaborador)


@colaborador_route.route('/new')
def form_new_colaborador():
    """ formulário para criar colaborador """
    return render_template('colaborador/form_colaborador.html')


@colaborador_route.route('/<int:colaborador_id>')
def detalhe_colaborador(colaborador_id):
    """ exibir informações do colaborador """
    colaborador = db.get_or_404(Colaborador, colaborador_id)
    return render_template('colaborador/detalhe_colaborador.html', colaborador=colaborador)


@colaborador_route.route('/<int:colaborador_id>/edit')
def form_edit_colaborador(colaborador_id):
    """ formulário para editar informações do colaborador """
    colaborador = db.get_or_404(Colaborador, colaborador_id)
    return render_template('form_edit_cliente.html', colaborador=colaborador)


@colaborador_route.route('/<int:colaborador_id>/update', methods=['PUT'])
def atualizar_colaborador(colaborador_id):
    """ atualizar informações do colaborador """
    colaborador = db.get_or_404(Colaborador, colaborador_id)

    colaborador.nome_completo = request.form["nomeForm"]
    colaborador.senha = request.form["senhaForm"]
    colaborador.email = request.form["emailForm"]
    colaborador.cargo = request.form["cargoForm"]
    colaborador.telefone = request.form.get("telefoneForm") or None

    db.session.commit()

    return render_template("colaborador/item_colaborador.html", colaborador=colaborador)


@colaborador_route.route('/<int:colaborador_id>/delete', methods=['DELETE'])
def deletar_colaborador(colaborador_id):
    """ deletar dados do colaborador """
    colaborador = Colaborador.query.get(colaborador_id)

    if colaborador:
        db.session.delete(colaborador)
        db.session.commit()

    return ''
