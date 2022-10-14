from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

auth = Blueprint('login', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"Error": "Usuario o contraseña inválido"}), 401

    token = create_access_token(identity=username)
    return jsonify(token=token)


    