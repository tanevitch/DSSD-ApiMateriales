from app.db import db
from sqlalchemy.orm import relationship

from app.models.material import Material
from app.models.proovedor_material import proovedor_material

class Proovedor(db.Model):
    __tablename__ = 'proovedor'
    id_proovedor = db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(100),nullable  = False)
    tipo = db.Column(db.String(50),nullable  = False)
    materiales_en_stock= relationship(Material, secondary=proovedor_material, backref=db.backref('proovedor'))

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo= tipo
