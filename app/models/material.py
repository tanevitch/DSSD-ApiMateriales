
from app.db import db

class Material(db.Model):
    __tablename__ = 'material'
    id_material= db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    descripcion = db.Column(db.String(100), nullable = False)


    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion= descripcion
      