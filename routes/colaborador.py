from flask import Blueprint, render_template, request
from models import Usuario
from db import db

colaborador_route = Blueprint('colaborador', __name__)

"""

Rota de Colaboradores

 - /colaborador/ (GET) - Lista os colaboradores
 - /colaborador/ (POST) - Inserir um colaboradores no servidor
 - /colaborador/new (GET) - Renderizar um Forms para criar um colaborador
 - /colaborador/<id> (GET) - Obter os dados de um colaborador
 - /colaborador/<id>/edit (GET) - Renderizar um Forms para editar um colaborador
 - /colaborador/<id>/update (PUT) - Atualizar os dados de um colaborador
 - /colaborador/<id>/delete (DELETE) - Deleta os dados de um colaborador

"""

@colaborador_route.route('/')
def lista_colaborador():
    """ listar os colaboradores """
    usuario = Usuario.query.all()
    return render_template('lista_colaborador.html', db=usuario)

@colaborador_route.route('/', methods=['POST'])
def inserir_colaborador():
    """ inserir os dados do colaborador """
    nome = request.form["nomeForm"]
    senha = request.form["senhaForm"]
    email = request.form["emailForm"]
    cargo = request.form["cargoForm"]

    novo_colaborador = Usuario(nome=nome, senha=senha, email=email, cargo=cargo)
    db.session.add(novo_colaborador)
    db.session.commit()

    # print(novo_colaborador.nome)
    # print(novo_colaborador.senha)
    # print(novo_colaborador.email)
    # print(novo_colaborador.cargo)
    return render_template("item_colaborador.html", colaborador=novo_colaborador)

@colaborador_route.route('/new')
def form_new_colaborador():
    """ formulário para criar colaborador """
    return render_template('form_colaborador.html')

@colaborador_route.route('/<int:colaborador_id>')
def detalhe_colaborador(colaborador_id):
    """ exibir informações do colaborador """
    return render_template('detalhe_colaborador.html')

@colaborador_route.route('/<int:colaborador_id>/edit')
def form_edit_colaborador(colaborador_id):
    """ form para editar informações do colaborador """
    return render_template('form_edit_cliente.html')

@colaborador_route.route('/<int:colaborador_id>/update', methods=['PUT'])
def atualizar_colaborador(colaborador_id):
    """ atualizar informações do colaborador """
    pass

@colaborador_route.route('/<int:colaborador_id>/delete', methods=['DELETE'])
def deletar_colaborador(colaborador_id):
    """ deletar dados do colaborador """
    colaborador = Usuario.query.get(colaborador_id)

    if colaborador:
        db.session.delete(colaborador)
        db.session.commit()

    return ''

