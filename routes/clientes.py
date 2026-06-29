from flask import Blueprint, jsonify, request 
from database import db
from models import Cliente, Aluguel
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("clientes", __name__)


@bp.route("/clientes", methods=["POST"])
@jwt_required()
def adicionar_cliente():
    dados = request.get_json()
    if not dados.get("nome"):
        return jsonify({"erro": "Não é possível cadastrar cliente sem nome"}), 400
    if not dados.get("telefone"):
        return jsonify({"erro": "Não é possível cadastrar cliente sem o telefone"}), 400
    if not dados.get("cpf"):
        return jsonify({"erro": "Não é possível cadastrar cliente sem o cpf"}), 400
    if len(dados.get("cpf")) != 11:
        return jsonify({"erro": "CPF deve ter 11 dígitos"}), 400
    if Cliente.query.filter_by(cpf=dados["cpf"]).first():
        return jsonify({"erro": "CPF já cadastrado"}), 400
    novo_cliente = Cliente(
        nome=dados["nome"],
        telefone=dados["telefone"],
        cpf=dados["cpf"],
        email=dados["email"])
    
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify(novo_cliente.to_dict()), 201

@bp.route("/clientes", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([e.to_dict() for e in clientes])

@bp.route("/clientes/<int:id>/historico", methods=["GET"])
@jwt_required()
def buscar_por_historico(id):
    historico = Aluguel.query.filter(Aluguel.cliente_id == id).all()
    return jsonify([e.to_dict() for e in historico])

@bp.route("/clientes/buscar/nome", methods=["GET"])
@jwt_required()
def buscar_por_nome_cliente():
    nome = request.args.get("nome")
    cliente_procurado = Cliente.query.filter(Cliente.nome.ilike(f"%{nome}%")).all()
    return jsonify([e.to_dict() for e in cliente_procurado])


@bp.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
def editar_dados_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    dados = request.get_json()
    if not dados.get("nome"):
        return jsonify({"erro": "Não é possível atualizar cliente sem nome"}), 400
    if not dados.get("telefone"):
        return jsonify({"erro": "Não é possível atualizar cliente sem o telefone"}), 400
    if not dados.get("cpf"):
        return jsonify({"erro": "Não é possível atualizar cliente sem o cpf"}), 400
    if len(dados.get("cpf")) != 11:
        return jsonify({"erro": "CPF deve ter 11 dígitos"}), 400
    if Cliente.query.filter_by(cpf=dados["cpf"]).first():
        return jsonify({"erro": "CPF já cadastrado"}), 400
    cliente.nome = dados["nome"]
    cliente.telefone = dados["telefone"]
    cliente.cpf = dados["cpf"]
    cliente.email = dados["email"]
    
    db.session.commit()
    return jsonify(cliente.to_dict())



@bp.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_Cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if Aluguel.query.filter_by(cliente_id=id, ativo=True).first():
        return jsonify({"erro": "Não é possível deletar um cliente com aluguel ativo"}), 400
    db.session.delete(cliente)
    db.session.commit()
    return jsonify("Cliente deletado com sucesso!")
