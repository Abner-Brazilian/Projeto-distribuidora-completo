from flask import Blueprint, jsonify, request 
from database import db
from models import Equipamento
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint("equipamentos", __name__)

@bp.route("/equipamentos", methods=["POST"])
@jwt_required()
def adicionar_equipamento():
    dados = request.get_json()
    if not dados.get("nome"):
        return jsonify({"erro": "Não é possível cadastrar equipamento sem nome"}), 400
    if not dados.get("valor_diario"):
        return jsonify({"erro": "Não é possível cadastrar equipamento sem valor_diario"}), 400
    if not isinstance (dados.get("valor_diario"), (int, float)):
        return jsonify ({"erro": "O valor diario deve ser um numero"}), 400

    novo_equipamento = Equipamento(
        nome=dados["nome"],
        descricao=dados["descricao"],
        categoria=dados["categoria"],
        valor_diario=dados["valor_diario"])
       
    db.session.add(novo_equipamento)
    db.session.commit()
    return jsonify(novo_equipamento.to_dict()), 201


@bp.route("/equipamentos", methods=["GET"])
@jwt_required()
def listar_equipamentos():
    equipamentos = Equipamento.query.all()
    return jsonify([e.to_dict() for e in equipamentos])
   

@bp.route("/equipamentos/buscar", methods=["GET"])
@jwt_required()
def buscar_por_nome_equipamento():
    nome = request.args.get("nome")
    equipamento_procurado = Equipamento.query.filter(Equipamento.nome.ilike(f"%{nome}%")).all()
    return jsonify([e.to_dict() for e in equipamento_procurado])


@bp.route("/equipamentos/<int:id>/status", methods=["PATCH"])
@jwt_required()
def editar_status(id):
    equipamento = Equipamento.query.get_or_404(id)
    dados = request.get_json()
    if dados.get("em_uso") is None:
        return jsonify({"erro": "Campo em_uso é obrigatório"}), 400
    
    equipamento.em_uso = dados["em_uso"]
    db.session.commit()
    return jsonify(equipamento.to_dict())

@bp.route("/equipamentos/<int:id>/valor", methods=["PATCH"])
@jwt_required()
def editar_valor_diario(id):
    equipamento = Equipamento.query.get_or_404(id)
    dados = request.get_json()
    if not dados.get("valor_diario"):
        return jsonify({"erro": "Não é possível editar o valor do equipamento sem o valor do equipamento"}), 400
    if not isinstance (dados.get("valor_diario"), (int, float)):
        return jsonify ({"erro": "O valor diario deve ser um numero"}), 400
    equipamento.valor_diario = dados["valor_diario"]
    db.session.commit()
    return jsonify(equipamento.to_dict())

@bp.route("/equipamentos/<int:id>/categoria", methods=["PATCH"])
@jwt_required()
def editar_categoria(id):
    equipamento = Equipamento.query.get_or_404(id)
    dados = request.get_json()
    if not dados.get("categoria"):
        return jsonify({"erro": "Não é possível editar a categoria equipamento sem a nova categroia do equipamento"}), 400
    if isinstance (dados.get("categoria"), (int, float)):
        return jsonify ({"erro": "A categoria deve ser um texto"}), 400
    equipamento.categoria = dados["categoria"]
    db.session.commit()
    return jsonify(equipamento.to_dict())

@bp.route("/equipamentos/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_equipamento(id):
    equipamento = Equipamento.query.get_or_404(id)
    if equipamento.em_uso is True:
        return jsonify({"erro": "Não é possível deletar um equipamento que está em uso"}), 400
    db.session.delete(equipamento)
    db.session.commit()
    return jsonify("Equipamento deletado com sucesso!")