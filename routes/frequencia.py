from flask import Blueprint, render_template, request
from models import Frequencia, Atendido, Turma, Colaborador
from db import db
from datetime import datetime

frequencia_route = Blueprint('frequencia', __name__)

"""

Rota de Frequência

 - /frequencia/ (GET) - Lista as Frequências cadastradas
 - /frequencia/ (POST) - Insere uma Frequência no servidor
 - /frequencia/new (GET) - Renderizar um formulário para criar uma Frequência
 - /frequencia/<id> (GET) - Obter os dados de uma Frequência
 - /frequencia/<id>/edit (GET) - Renderizar um formulário para editar uma Frequência
 - /frequencia/<id>/update (PUT) - Atualizar os dados de uma Frequência
 - /frequencia/<id>/delete (DELETE) - Deletar os dados de uma Frequência

"""


@frequencia_route.route('/')
def lista_frequencia():
    """ listar as frequências """
    frequencias = Frequencia.query.all()
    return render_template('lista_frequencia.html', db=frequencias)


@frequencia_route.route('/', methods=['POST'])
def inserir_frequencia():
    """ inserir os dados da frequência """
    id_atendido = request.form["atendidoForm"]
    id_turma = request.form["turmaForm"]
    id_colaborador = request.form["colaboradorForm"]
    data_encontro = datetime.strptime(request.form["dataForm"], '%Y-%m-%d').date()
    presente = request.form.get("presenteForm") == 'on'

    nova_frequencia = Frequencia(
        id_atendido=id_atendido,
        id_turma=id_turma,
        id_colaborador=id_colaborador,
        data_encontro=data_encontro,
        presente=presente,
    )
    db.session.add(nova_frequencia)
    db.session.commit()

    return render_template("item_frequencia.html", frequencia=nova_frequencia)


@frequencia_route.route('/new')
def form_new_frequencia():
    """ formulário para criar frequência """
    atendidos = Atendido.query.all()
    turmas = Turma.query.all()
    colaboradores = Colaborador.query.all()
    return render_template('form_frequencia.html', atendidos=atendidos, turmas=turmas, colaboradores=colaboradores)


@frequencia_route.route('/<int:frequencia_id>')
def detalhe_frequencia(frequencia_id):
    """ exibir informações da frequência """
    frequencia = db.get_or_404(Frequencia, frequencia_id)
    return render_template('detalhe_frequencia.html', frequencia=frequencia)


@frequencia_route.route('/<int:frequencia_id>/edit')
def form_edit_frequencia(frequencia_id):
    """ formulário para editar informações da frequência """
    frequencia = db.get_or_404(Frequencia, frequencia_id)
    atendidos = Atendido.query.all()
    turmas = Turma.query.all()
    colaboradores = Colaborador.query.all()
    return render_template('form_edit_frequencia.html', frequencia=frequencia, atendidos=atendidos, turmas=turmas, colaboradores=colaboradores)


@frequencia_route.route('/<int:frequencia_id>/update', methods=['PUT'])
def atualizar_frequencia(frequencia_id):
    """ atualizar informações da frequência """
    frequencia = db.get_or_404(Frequencia, frequencia_id)

    frequencia.id_atendido = request.form["atendidoForm"]
    frequencia.id_turma = request.form["turmaForm"]
    frequencia.id_colaborador = request.form["colaboradorForm"]
    frequencia.data_encontro = datetime.strptime(request.form["dataForm"], '%Y-%m-%d').date()
    frequencia.presente = request.form.get("presenteForm") == 'on'

    db.session.commit()

    return render_template("item_frequencia.html", frequencia=frequencia)


@frequencia_route.route('/<int:frequencia_id>/delete', methods=['DELETE'])
def deletar_frequencia(frequencia_id):
    """ deletar dados da frequência """
    frequencia = Frequencia.query.get(frequencia_id)

    if frequencia:
        db.session.delete(frequencia)
        db.session.commit()

    return ''
