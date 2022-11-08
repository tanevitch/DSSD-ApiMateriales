from datetime import datetime
import json
from random import randint
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db
from app.models.material import Material
from app.models.pedido import Pedido
from app.models.proovedor import Proovedor
from app.models.renglon import Renglon
from app.schemas.pedido import pedido_schema
from app.schemas.renglon import renglones_schema

solicitudes = Blueprint('solicitudes', __name__, url_prefix='/pedidos')

  


@solicitudes.route("/nuevo", methods=["POST"])
@jwt_required()
def nueva_solicitud():
    get_jwt_identity()
    materiales_cantidades = request.json.get("materiales")
    fecha_necesaria_entrega = request.json.get("fecha_necesaria_entrega")
    if (not materiales_cantidades or not fecha_necesaria_entrega):
        return jsonify({"Error": "Solicitud inválida"}), 400
    
    # CONSULTAR POR STOCK
    productos_sin_stock = []
    for id_material in materiales_cantidades:
        material= Material.buscarPorId(id_material)
        proovedor= Proovedor.buscarProovedorDeMaterial(material)
        if (proovedor.stock_material < materiales_cantidades[id_material]):
            productos_sin_stock.append(
                Renglon(
                    proovedor,
                    material,
                    int(materiales_cantidades[id_material])
                )
            )
    if (productos_sin_stock):
        return [
                {
                    "error": "No se puede satisfacer el pedido, algunos proovedores no cuentan con el stock suficiente"
                },
                {
                    "detalle": renglones_schema.dump(productos_sin_stock)
                }
                
        ], 400

    
    #  INTENTAR EFECTUAR PEDIDO
    renglones= []
    for id_material in materiales_cantidades:
        material= Material.buscarPorId(id_material)
        proovedor= Proovedor.buscarProovedorDeMaterial(material)
        renglones.append(
            Renglon(
                proovedor,
                material,
                int(materiales_cantidades[id_material])
                ))
        proovedor.stock_material-= int(materiales_cantidades[id_material])
        db.session.merge(proovedor) 
    
    nuevo_pedido= Pedido(renglones)
    
    if (nuevo_pedido.fecha_entrega >= datetime.strptime(fecha_necesaria_entrega, "%Y-%m-%d")):
        return [{
                    "error": "No se puede satisfacer el pedido en los plazos requeridos, la fecha de entrega estimada es posterior a la solicitada",
                },
                {
                    "detalle": nuevo_pedido.fecha_entrega.date()
                }], 400

    db.session.add(nuevo_pedido)
    db.session.commit()
    return pedido_schema.dump(nuevo_pedido), 200

@solicitudes.route("/consultar/<int:id>", methods=["GET"])
@jwt_required()
def consultar_solicitud(id):
    get_jwt_identity()
    solicitud= Pedido.buscarPorId(id)
    if (not solicitud):
        return jsonify({"Error": f"No hay un pedido con id {id}"}), 404
    
    # Simulación de reprogramación de fecha_entrega
    if (randint(0,5)==3):
        solicitud.fecha_entrega= solicitud.fechaEntregaRandom()
        if (solicitud.fecha_entrega >= solicitud.fecha_necesaria_entrega):
            solicitud.estado= "cancelada"
            return jsonify({"Error": f"No se puede satisfacer el pedido. La fecha de entrega estimada es el {solicitud.fecha_entrega}"}), 400

    db.session.add(solicitud)
    db.session.commit()
    return pedido_schema.dump(solicitud), 200