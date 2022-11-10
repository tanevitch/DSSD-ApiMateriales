
from app.db import db
from datetime import datetime, timedelta

class Sede(db.Model):
    __tablename__ = 'sede'
    id_sede= db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    fabrica = db.Column(db.String(255), nullable = False)
    inicio_disponibilidad = db.Column(db.DateTime, nullable = False)
    fin_disponibilidad = db.Column(db.DateTime, nullable = False)


    def __init__(self, nombre, fabrica, inicio_disponibilidad, fin_disponibilidad):
        self.nombre = nombre
        self.fabrica= fabrica
        self.inicio_disponibilidad = inicio_disponibilidad
        self.fin_disponibilidad = fin_disponibilidad

    @classmethod
    def buscarPorId(cls, id):
        return cls.query.get(id)

    @classmethod 
    def all(cls):
        return cls.query.all()
