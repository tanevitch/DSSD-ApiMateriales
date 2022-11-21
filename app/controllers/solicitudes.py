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
from app.models.sedes_reservadas import SedesReservadas
from app.schemas.pedido import pedido_schema
from app.schemas.renglon import renglones_schema
from app.schemas.sedes_reservadas import sedes_reservadas_schema

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
        if (proovedor.stock_material < int(materiales_cantidades[id_material])):
            productos_sin_stock.append(
                Renglon(
                    proovedor,
                    material,
                    int(materiales_cantidades[id_material])
                )
            )


    if (productos_sin_stock):
        return jsonify(
            {
                "id": None,
                "detalle": renglones_schema.dump(productos_sin_stock),
                "fecha_entrega": None
            }
        ), 400

    
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

    if (nuevo_pedido.fecha_entrega > datetime.strptime(fecha_necesaria_entrega, "%Y-%m-%d")):
        fecha_entrega= pedido_schema.dump(nuevo_pedido)["fecha_entrega"].split()[0]

        return jsonify(
            {
                "id": None,
                "detalle": f"La fecha de entrega puede ser para el {fecha_entrega}",
                "fecha_entrega": fecha_entrega
                
            }), 400


    db.session.add(nuevo_pedido)
    db.session.commit()
    return jsonify({
                "id": pedido_schema.dump(nuevo_pedido)["id"],
                "detalle": pedido_schema.dump(nuevo_pedido),
                "fecha_entrega": pedido_schema.dump(nuevo_pedido)["fecha_entrega"].split()[0]
            }), 200

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

@solicitudes.route("/fabricacion", methods=["POST"])
@jwt_required()
def fabricacion_solicitud():
    get_jwt_identity()
    inicio_disponibilidad = request.json.get("inicio_disponibilidad")
    fecha_reserva = request.json.get("fecha_reserva")
    id_pedido = request.json.get("id_pedido")

    if (not fecha_reserva):
        return jsonify({"Error": "Solicitud inválida"}), 400
    
    # CONSULTAR POR FECHAS
    if (fecha_reserva < inicio_disponibilidad):
        return jsonify(
            {
                "id": None,
                "detalle": f"La fecha de reserva puede ser anterior a {inicio_disponibilidad}",
                "fecha_reserva": fecha_reserva
            }), 400

    #  INTENTAR EFECTUAR PEDIDO
    try:
        nueva_reserva = SedesReservadas.append(SedesReservadas(
            id_pedido = id_pedido,
            fecha_reserva = fecha_reserva
        ))
    except:
        return jsonify(
        {
            "id": None,
            "detalle": f"id pedido es incorrecto"
        }), 400

    db.session.add(nueva_reserva)
    db.session.commit()
    return jsonify({
                "id": sedes_reservadas_schema.dump(nueva_reserva)["id"],
                "detalle": sedes_reservadas_schema.dump(nueva_reserva),
                "FechaEntregaSedes": sedes_reservadas_schema.dump(nueva_reserva)["fecha_entrega_sedes"].split()[0]
            }), 200