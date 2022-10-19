from sqlalchemy.orm import relationship
import random
from datetime import datetime, timedelta

inicio = datetime.now()+ timedelta(days=1)
final =  datetime(2025, 1, 1)

from app.db import db
from app.models.renglon import Renglon

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id_pedido = db.Column(db.Integer(), primary_key = True)
    fecha_generacion_pedido = db.Column(db.DateTime, nullable = False)
    fecha_entrega = db.Column(db.DateTime, nullable = False)
    solicitante_id= db.Column(db.Integer, nullable= False)
    renglones = relationship(Renglon, backref=db.backref('pedidos'))
    estado= db.Column(db.String(50), nullable= False)

    def __init__(self, solicitante_id, renglones):
        self.fecha_generacion_pedido= datetime.now()
        self.fecha_entrega= inicio + (final - inicio) * random.random()
        self.renglones = renglones
        self.solicitante_id = solicitante_id
        self.estado= "pendiente"

    def toJSON(self):
        return {
            "id_pedido": self.id_pedido,
            "fecha_generacion_pedido": self.fecha_generacion_pedido,
            "fecha_entrega": self.fecha_entrega.strftime('%Y-%m-%d'),
            "id_caso": self.solicitante_id,
            "estado": self.estado,
            "pedidos": [renglon.toJSON() for renglon in self.renglones]
        }