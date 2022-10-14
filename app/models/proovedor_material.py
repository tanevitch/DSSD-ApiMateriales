from app.db import db

proovedor_material= db.Table('proovedor_material',
    db.Column('id_proovedor', db.Integer(), db.ForeignKey('proovedor.id_proovedor'), primary_key=True),
    db.Column('id_material', db.Integer(), db.ForeignKey('material.id_material'), primary_key=True),
    db.Column('stock', db.Integer())
)