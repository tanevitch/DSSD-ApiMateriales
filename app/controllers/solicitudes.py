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
from app.schemas.sedes_reservadas import sede_reservada_schema
from datetime import datetime, date, timedelta
import random

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

@solicitudes.route("/cancelar", methods=["POST"])
@jwt_required()
def cancelar_solicitud():
    get_jwt_identity()
    id = request.json.get("idPedido")
    id_reserva = request.json.get("idPedidoSede")
    solicitud= Pedido.buscarPorId(id)
    solicitud2 = SedesReservadas.buscarPorId(id_reserva)
    if (not solicitud):
        return jsonify({"Error": f"No hay un pedido con id {id}"}), 404
    if (solicitud2):
        #return jsonify({"Error": f"No hay un reserva de sede con id {id}"}), 404
        solicitud2.estado = "CANCELADO"
        db.session.merge(solicitud2)
    
    
    solicitud.estado= "CANCELADO"
    db.session.merge(solicitud)
    
    db.session.commit()
    return jsonify("Se cancelaron los pedidos"), 200
    #return pedido_schema.dump(solicitud), 200

@solicitudes.route("/fabricacion", methods=["POST"])
@jwt_required()
def fabricacion_solicitud():
    get_jwt_identity()
    #id_pedido = request.json.get("idPedido")
    fecha_reserva = request.json.get("fecha_reserva_sede")
    fecha_lanzamiento = request.json.get("fecha_necesaria_entrega")# es fecha de lanzamiento
    pedido_fabricacion = request.json.get("pedido_fabricacion")
    

    if (not fecha_reserva):
        print("Soliciud invalida. Falta fecha reserva")
        return jsonify({"Error": "Solicitud inválida"}), 400

    fecha_entrega_sedes = datetime.strptime(fecha_reserva, "%Y-%m-%d") + timedelta(days=30)

    if (not fecha_lanzamiento):
        print("Soliciud invalida. Falta lanzamiento")
        return jsonify({"Error": "Solicitud inválida"}), 400

    if (fecha_entrega_sedes > datetime.strptime(fecha_lanzamiento, "%Y-%m-%d") ):
        print("fecha_entrega_sedes")
        print(fecha_entrega_sedes)

        print("fecha_lanzamiento")
        print(datetime.strptime(fecha_lanzamiento, "%Y-%m-%d"))
        print(fecha_lanzamiento)


        print("Entrega sedes es mayor a fecha lanzamiento")
        return jsonify(
            {
                "id": None,
                "detalle": f"La fecha de entrega debe ser anterior a {fecha_lanzamiento}",
                "fecha_reserva": fecha_reserva
            }), 400

    
    #  INTENTAR EFECTUAR PEDIDO
    try:
        
        nueva_reserva = SedesReservadas(fecha_entrega_sedes = fecha_entrega_sedes,estado = "CONFIRMADO", marco_material = pedido_fabricacion["materialMarcos"], marco_cantidad = pedido_fabricacion["cantidadMarcos"],patillas_material = pedido_fabricacion["materialPatillas"],patillas_cantidad = pedido_fabricacion["cantidadPatillas"],estuche_material = pedido_fabricacion["materialEstuche"],escuche_cantidad = pedido_fabricacion["cantidadEstuche"],lentes_material= pedido_fabricacion["materialLentes"],lentes_cantidad = pedido_fabricacion["cantidadLentes"])
        print(nueva_reserva)
       
        # nueva_reserva = SedesReservadas.append(SedesReservadas(
            
        #     fecha_reserva = fecha_reserva
        #))
    except:
        print("catched!")
        print(type(fecha_entrega_sedes))
        print(fecha_entrega_sedes)
        return jsonify(
        {
            "id": None,
            "detalle": f"id pedido es incorrecto"
        }), 400

    db.session.add(nueva_reserva)
    db.session.commit()
    print("-*/-*/RESERVA-*/-*/-")
    print(nueva_reserva.id)
    #return sede_reservada_schema.dump(nueva_reserva), 200
    #"id": sede_reservada_schema.dump(nueva_reserva)["id"],
   
    return jsonify({
                "id": nueva_reserva.id,
                "fecha_entrega_sedes": fecha_entrega_sedes,
                "detalle": sede_reservada_schema.dump(nueva_reserva),
                "estado":"CONFIRMADO"
            }), 200

#http://localhost:5000/pedidos/consultarFabricacion/

@solicitudes.route("/consultarFabricacion", methods=["POST"])
@jwt_required()
def consultar_fabricacion():
    get_jwt_identity()
    print (request.json)
    id = request.json.get("idPedidoSede")
    solicitud= SedesReservadas.buscarPorId(id)
    
    if (not solicitud):
        return jsonify({"Error": f"No hay una reserva de fabricación con id {id}"}), 404

    if solicitud.fecha_entrega_sedes <= datetime.today():
        solicitud.estado = "FINALIZADO"
        db.session.commit()

    return jsonify({"estado": solicitud.estado}), 200

#http://localhost:5000/pedidos/modificarFechaFabricacion/1/2030-03-30
@solicitudes.route("/modificarFechaFabricacion/<int:id>/<string:fecha>", methods=["GET"])
def modificar_fecha_entrega(id,fecha):
    solicitud= SedesReservadas.query.get(id)
    if (not solicitud):
        return jsonify({"Error": f"No hay una reserva de fabricación con id {id}"}), 404
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    solicitud.fecha_entrega_sedes=fecha
    solicitud.estado="ATRASADO"
    db.session.commit()
    
    return pedido_schema.dump(solicitud), 200

#http://localhost:5000/pedidos/terminarFabricacion/
@solicitudes.route("/terminarFabricacion/<int:id>", methods=["GET"])
def terminar_fabricacion(id):
    solicitud= SedesReservadas.query.get(id)
    if (not solicitud):
       return jsonify({"Error": f"No hay una reserva de fabricación con id {id}"}), 404
    solicitud.fecha_entrega_sedes=datetime.today()
    solicitud.estado="FINALIZADO"
    db.session.commit()

    return pedido_schema.dump(solicitud), 200

#http://localhost:5000/pedidos/confirmarFabricacion/

@solicitudes.route("/confirmarFabricacion", methods=["POST"])
@jwt_required()
def confirmar_fabricacion():
    get_jwt_identity()
    print (request.json)
    id = request.json.get("idPedidoSede")
    solicitud= SedesReservadas.buscarPorId(id)
    
    if (not solicitud):
        return jsonify({"Error": f"No hay una reserva de fabricación con id {id}"}), 404

   
    solicitud.estado = "CONFIRMADO"
    db.session.commit()

    return jsonify({"estado": solicitud.estado}), 200

