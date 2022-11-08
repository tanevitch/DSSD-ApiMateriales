from marshmallow import Schema, fields

from app.schemas.renglon import RenglonSchema

class  PedidoSchema(Schema):
    id = fields.Int(attribute="id_pedido")
    fecha_generacion_pedido= fields.String(attribute="fecha_generacion_pedido")
    fecha_entrega= fields.String(attribute="fecha_entrega")
    renglones = fields.Nested(RenglonSchema, many=True)
    estado = fields.String(attribute="estado")

pedido_schema = PedidoSchema()
