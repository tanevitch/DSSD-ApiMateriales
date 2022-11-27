from datetime import timedelta
import random
from app.db import db

class SedesReservadas(db.Model):
    __tablename__ = 'sedes_reservadas'
    id = db.Column(db.Integer(), primary_key = True)
    #id_pedido = db.Column(db.Integer(), nullable = False)
    #fecha_reserva = db.Column(db.DateTime, nullable = False)
    fecha_entrega_sedes = db.Column(db.DateTime, nullable = False)
    estado = db.Column(db.String(255), nullable = True)
    marco_material = db.Column(db.String(255), nullable = True)
    marco_cantidad = db.Column(db.Integer(), nullable = True)
    patillas_material = db.Column(db.String(255), nullable = True)
    patillas_cantidad = db.Column(db.Integer(),nullable = True)
    estuche_material = db.Column(db.String(255), nullable = True)
    escuche_cantidad = db.Column(db.Integer(),nullable = True)
    lentes_material = db.Column(db.String(255), nullable = True)
    lentes_cantidad = db.Column(db.Integer(), nullable = True)

    def __init__(self, fecha_entrega_sedes,estado,marco_material,marco_cantidad,patillas_material,patillas_cantidad,estuche_material,escuche_cantidad,lentes_material,lentes_cantidad):
        #self.id_pedido = id_pedido
        #self.fecha_reserva = fecha_reserva
        #self.fecha_entrega_sedes = fecha_reserva + timedelta(days=random(10,90))
        self.fecha_entrega_sedes = fecha_entrega_sedes
        self.estado = estado
        self.marco_material = marco_material
        self.marco_cantidad = int(marco_cantidad)
        self.patillas_material = patillas_material
        self.patillas_cantidad  = int(patillas_cantidad)
        self.estuche_material = estuche_material
        self.escuche_cantidad = int(escuche_cantidad)
        self.lentes_material = lentes_material
        self.lentes_cantidad = int(lentes_cantidad)


        

    @classmethod 
    def all(cls):
        return cls.query.all()
