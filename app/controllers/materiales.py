from flask import Blueprint, jsonify
from app.models.material import Material
from app.schemas.material import materiales_schema

materiales = Blueprint('materiales', __name__, url_prefix='/materiales')


@materiales.route("", methods=["GET"])
def todos():
    resp = materiales_schema.dump(Material.all())
    return resp, 200
