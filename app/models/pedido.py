from datetime import datetime
from sqlalchemy.orm import relationship

from app.db import db
from app.models.material import Material
from app.models.pedido_material import pedido_material

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id_pedido = db.Column(db.Integer(), primary_key = True)
    fecha_generacion_pedido = db.Column(db.DateTime, nullable = False)
    fecha_entrega = db.Column(db.DateTime, nullable = False)
    proovedor_id= db.Column(db.Integer, db.ForeignKey('proovedor.id_proovedor'))
    solicitante_id= db.Column(db.Integer, db.ForeignKey('user.id_usuario'))
    materiales = relationship(Material, secondary=pedido_material, backref=db.backref('pedidos'))

    def __init__(self, nombre, materiales, proovedor_id, solicitante_id):
        self.nombre = nombre
        self.fecha_generacion_pedido= datetime.now()
        self.materiales= materiales
        self.proovedor_id = proovedor_id
        self.solicitante_id = solicitante_id