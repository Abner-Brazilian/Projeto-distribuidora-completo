from flask import Blueprint, jsonify, request 
from database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint("usuario", __name__)

@bp.route("/login", methods=["POST"])
def login():
    nome_usuario= request.json.get("nome_usuario", None)
    senha = request.json.get("senha", None)
    if nome_usuario!= "test" or senha != "test":
        return jsonify({"msg": "nome de usuarios ou senha invalido!!"}), 401

    access_token = create_access_token(identity=nome_usuario)
    return jsonify(access_token=access_token)


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
