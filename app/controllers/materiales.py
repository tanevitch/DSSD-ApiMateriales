from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.material import Material

materiales = Blueprint('materiales', __name__, url_prefix='/materiales')


@materiales.route("/", methods=["GET"])
def protected():
    return jsonify([ material.toJSON() for material in Material.all()]), 200


