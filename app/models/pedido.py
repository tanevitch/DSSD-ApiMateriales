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
    fecha_necesaria_entrega = db.Column(db.DateTime, nullable = False)
    fecha_entrega = db.Column(db.DateTime, nullable = False)
    renglones = relationship(Renglon, backref=db.backref('pedidos'))
    estado= db.Column(db.String(50), nullable= False)

    def __init__(self,fecha_necesaria_entrega, renglones):
        self.fecha_necesaria_entrega = datetime.strptime(fecha_necesaria_entrega, "%Y-%m-%d")
        self.fecha_generacion_pedido= datetime.now()
        self.fecha_entrega= self.fechaEntregaRandom()
        self.renglones = renglones
        self.estado= "pendiente"

    def fechaEntregaRandom(self):
        return inicio + (final - inicio) * random.random()

    @classmethod
    def buscarPorId(cls, id):
        return cls.query.get(id)

    def toJSON(self):
        return {
            "id_pedido": self.id_pedido,
            "fecha_generacion_pedido": self.fecha_generacion_pedido,
            "fecha_entrega": self.fecha_entrega.strftime('%Y-%m-%d'),
            "estado": self.estado,
            "pedidos": [renglon.toJSON() for renglon in self.renglones]
        }