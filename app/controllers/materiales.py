from flask import Blueprint, jsonify
from app.models.material import Material
materiales = Blueprint('materiales', __name__, url_prefix='/materiales')


@materiales.route("", methods=["GET"])
def todos():
    resp = jsonify([material.toJSON() for material in Material.all()])
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp, 200
