import random
from app.db import db

class SedesReservadas(db.Model):
    __tablename__ = 'sedes_reservadas'
    id = db.Column(db.Integer(), primary_key = True)
    id_pedido = db.Column(db.Integer(), nullable = False)
    fecha_reserva = db.Column(db.DateTime, nullable = False)
    fecha_entrega_sedes = db.Column(db.DateTime, nullable = False)

    def __init__(self, id_pedido, fecha_reserva):
        self.id_pedido = id_pedido
        self.fecha_reserva = fecha_reserva
        self.fecha_entrega_sedes = fecha_reserva + random(10,90)

    @classmethod 
    def all(cls):
        return cls.query.all()
