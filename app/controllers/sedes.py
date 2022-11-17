from flask import Blueprint, jsonify
from app.models.sede import Sede
from app.schemas.sede import sedes_schema
from app.schemas.sede import sede_schema


sedes = Blueprint('sedes', __name__, url_prefix='/sedes')


@sedes.route("", methods=["GET"])
def todos():
    resp = sedes_schema.dump(Sede.all())
    return resp, 200

@sedes.route("/<int:id>", methods=["GET"])
def get(id):
    resp = sede_schema.dump(Sede.buscarPorId(id))
    return resp, 200
