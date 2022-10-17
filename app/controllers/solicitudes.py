from datetime import datetime
import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db

from app.models.material import Material
from app.models.pedido import Pedido
from app.models.proovedor import Proovedor
from app.models.renglon import Renglon

solicitudes = Blueprint('solicitudes', __name__, url_prefix='/solicitudes')

@solicitudes.route("/nueva", methods=["POST"])
@jwt_required()
def nueva_solicitud():
    get_jwt_identity()

    materiales_cantidades = request.json.get("materiales")
    fecha_lanzamiento = request.json.get("fecha_lanzamiento")

    if (not materiales_cantidades or not fecha_lanzamiento):
        return jsonify({"Error": "Solicitud inválida"}), 400
    
    renglones= []
    for id_material in materiales_cantidades:
        material= Material.buscarPorId(id_material)
        proovedor= Proovedor.buscarProovedorDeMaterial(material)
        if (proovedor.stock_material == 0):
            return jsonify({"Error": f"No se puede satisfacer el pedido del material {material.nombre}"}), 400

        proovedor.stock_material-= materiales_cantidades[id_material]
        db.session.merge(proovedor)
        renglones.append(
            Renglon(
                proovedor,
                material,
                materiales_cantidades[id_material]
                ))

    nuevo_pedido= Pedido("2000", renglones)
    if (nuevo_pedido.fecha_entrega >= datetime.strptime(fecha_lanzamiento, "%Y-%m-%d %H:%M:%S")):
        return jsonify({"Error": f"No se puede satisfacer el pedido. La fecha de entrega estimada es el {nuevo_pedido.fecha_entrega}"}), 400

    
    db.session.add(nuevo_pedido)
    db.session.commit()
    return jsonify(nuevo_pedido.toJSON()), 200

