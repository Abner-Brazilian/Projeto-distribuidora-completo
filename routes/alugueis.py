from flask import Blueprint, jsonify, request 
from database import db
from models import Equipamento, Aluguel, Cliente
from datetime import date
from datetime import datetime
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("alugueis", __name__)

@bp.route("/alugueis", methods=["POST"])
@jwt_required()
def adicionar_aluguel():
    dados = request.get_json()
    if not dados.get("cliente_id"):
        return jsonify({"erro": "Não é possível cadastrar aluguel sem o id do cliente"}), 400
    if not isinstance (dados.get("cliente_id"), (int)):
        return jsonify ({"erro": "O id do cliente deve ser um numero"}), 400
    if not Cliente.query.filter_by(id=dados["cliente_id"]).first():
        return jsonify({"erro": "O id não existe!"}), 400
    if not dados.get("equipamento_id"):
        return jsonify({"erro": "Não é possível cadastrar o aluguel sem id do equipamento"}), 400
    if not isinstance (dados.get("equipamento_id"), (int)):
        return jsonify ({"erro": "equipamento id deve ser um numero"}), 400
    if not Equipamento.query.filter_by(id=dados["equipamento_id"]).first():
        return jsonify({"erro": "O id não existe!"}), 400
    equipamento = Equipamento.query.get(dados["equipamento_id"])
    if equipamento.em_uso:
        return jsonify({"erro": "Não é possível alugar um equipamento já alugado"}), 400
    if not dados.get("data_inicio"):
        return jsonify({"erro": "Não é possível cadastrar aluguel sem a data de inicio"}), 400
    if not dados.get("data_fim"):
        return jsonify({"erro": "Não é possível cadastrar aluguel sem a data de devolção"}), 400 
    try:
        data_inicio = datetime.strptime(dados["data_inicio"], "%Y-%m-%d").date()
        data_fim = datetime.strptime(dados["data_fim"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Formato de data inválido, use AAAA-MM-DD"}), 400
    if data_fim <= data_inicio:
        return jsonify({"erro": "A data de devolução deve ser posterior à data de início"}), 400
    dias = (data_fim - data_inicio).days
    valor_total = dias * equipamento.valor_diario

    novo_aluguel = Aluguel(
        cliente_id=dados["cliente_id"],
        equipamento_id=dados["equipamento_id"],
        data_inicio=data_inicio,
        data_fim=data_fim,
        valor_total=valor_total)
    db.session.add(novo_aluguel)
    db.session.commit()
    return jsonify(novo_aluguel.to_dict()), 201

@bp.route("/alugueis", methods=["GET"])
@jwt_required()
def listar_alugueis():
    alugueis = Aluguel.query.all()
    return jsonify([e.to_dict() for e in alugueis])

@bp.route("/alugueis/ativo", methods=["GET"])
@jwt_required()
def listar_alugueis_ativos():
    ativos = Aluguel.query.filter(Aluguel.ativo == True).all()
    return jsonify([e.to_dict() for e in ativos])

@bp.route("/alugueis/<int:id>", methods=["PATCH"])
@jwt_required()
def mudar_estado_equipamento(id):
    aluguel = Aluguel.query.get_or_404(id)
    if aluguel.ativo == False:
        return jsonify({"erro": "O aluguel já esta inativo"}), 400
    if aluguel.ativo == True:
        aluguel.ativo = False
        equipamento = Equipamento.query.get(aluguel.equipamento_id)
        equipamento.em_uso = False
        db.session.commit()
        return jsonify(aluguel.to_dict())

@bp.route("/alugueis/relatorio/equipamentos", methods=["GET"])
@jwt_required()
def pesquisar_equipamento():
    
    resultado = db.session.query(
        Aluguel.equipamento_id,
        func.count(Aluguel.id).label("total")
    ).group_by(Aluguel.equipamento_id).order_by(func.count(Aluguel.id).desc()).all()
    return jsonify([{"equipamento_id": r[0], "total_alugueis": r[1]} for r in resultado])

@bp.route("/alugueis/relatorio/receita", methods=["GET"])
@jwt_required()
def relatorio_receita():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
    resultado = db.session.query(
    func.sum(Aluguel.valor_total)
    ).filter(
    Aluguel.data_inicio >= data_inicio,
    Aluguel.data_fim <= data_fim
    )
    
    valor_total = db.session.scalar(resultado)
    return jsonify({"receita_total": valor_total or 0.0})

@bp.route("/alugueis/relatorio/clientes", methods=["GET"])
@jwt_required()
def relatorio_clientes():
    resultado = db.session.query(
    Aluguel.cliente_id,
    func.count(Aluguel.id).label("total")
    ).group_by(Aluguel.cliente_id).order_by(func.count(Aluguel.id).desc()).all()
    return jsonify([{"cliente_id": r[0], "total_alugueis": r[1]} for r in resultado])
