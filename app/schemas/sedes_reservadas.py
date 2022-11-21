from marshmallow import Schema, fields

class  SedesReservadasSchema(Schema):
    id = fields.Int(attribute="id")
    id_pedido = fields.String(attribute="id_pedido")
    fecha_reserva = fields.DateTime(attribute="fecha_reserva")

sede_reservada_schema = SedesReservadasSchema()
sedes_reservadas_schema = SedesReservadasSchema(many=True)