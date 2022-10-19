from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

proovedores = Blueprint('proveedores', __name__, url_prefix='/proveedores')


@proovedores.route("/", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


