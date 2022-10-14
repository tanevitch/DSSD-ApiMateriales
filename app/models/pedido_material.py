from app.db import db

pedido_material= db.Table('pedido_material',
    db.Column('id_pedido', db.Integer(), db.ForeignKey('pedido.id_pedido'), primary_key=True),
    db.Column('id_material', db.Integer(), db.ForeignKey('material.id_material'), primary_key=True)
)