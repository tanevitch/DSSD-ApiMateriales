from sqlalchemy.orm import relationship
from app.db import db
from app.models.material import Material

class Renglon(db.Model):
    __tablename__ = 'renglon_pedido'
    id_renglon_pedido = db.Column(db.Integer(), primary_key = True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'))
    pedido = relationship("Pedido", backref=db.backref("renglon"))

    id_proovedor= db.Column(db.Integer, db.ForeignKey('proovedor.id_proovedor'))
    proovedor = relationship("Proovedor", backref=db.backref("renglon"))

    id_material =  db.Column(db.Integer, db.ForeignKey('material.id_material'))
    material = relationship("Material", backref=db.backref("renglon"))

    cantidad= db.Column(db.Integer, nullable=False)

    def __init__(self, proovedor, material, cantidad):
        self.proovedor= proovedor
        self.material= material
        self.cantidad= cantidad
