from marshmallow import Schema, fields
from app.schemas.material import MaterialSchema

class  ProovedorSchema(Schema):
    id = fields.Int(attribute="id_pedido")
    cantidad = fields.Int(attribute="cantidad")
    tipo = fields.String(attribute="tipo")
    stock_restante = fields.Int(attribute="stock_material")
    vende = fields.Nested(MaterialSchema)

proovedor_schema = ProovedorSchema()
