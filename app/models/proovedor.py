from app.db import db
from sqlalchemy.orm import relationship

class Proovedor(db.Model):
    __tablename__ = 'proovedor'
    id_proovedor = db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(100),nullable  = False)
    tipo = db.Column(db.String(50),nullable  = False)
    stock_material= db.Column(db.Integer(),nullable  = False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id_material') )
    material = relationship("Material", backref=db.backref("parent", uselist=False))

    def __init__(self, nombre, tipo, material, stock_material):
        self.nombre = nombre
        self.tipo= tipo
        self.stock_material = stock_material
        self.material= material

    @classmethod
    def buscarProovedorDeMaterial(cls, material):
        return cls.query.filter(cls.material == material).first()
