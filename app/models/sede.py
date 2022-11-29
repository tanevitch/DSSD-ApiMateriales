
from app.db import db
from datetime import datetime, timedelta

class Sede(db.Model):
    __tablename__ = 'sede'
    id_sede= db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    fabrica = db.Column(db.String(255), nullable = False)


    def __init__(self, nombre, fabrica):
        self.nombre = nombre
        self.fabrica= fabrica

    @classmethod
    def buscarPorId(cls, id):
        return cls.query.get(id)

    @classmethod 
    def all(cls):
        return cls.query.all()
