from flask import Blueprint, jsonify
from app.models.material import Material
materiales = Blueprint('materiales', __name__, url_prefix='/materiales')


@materiales.route("/", methods=["GET"])
def todos():
    return jsonify([material.toJSON() for material in Material.all()]), 200
