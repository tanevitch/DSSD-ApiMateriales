from marshmallow import Schema, fields

class  SedesReservadasSchema(Schema):
    id = fields.Int(attribute="id")
    #id_pedido = fields.String(attribute="id_pedido")
    #fecha_reserva = fields.DateTime(attribute="fecha_reserva")
    fecha_entrega_sedes = fields.DateTime(attribute="fecha_entrega_sedes")
    marco_material = fields.String(attribute="marco_material")
    marco_cantidad = fields.Int(attribute="marco_cantidad")
    patillas_material = fields.String(attribute="patillas_material")
    patillas_cantidad = fields.Int(attribute="patillas_cantidad")
    estuche_material = fields.String(attribute="estuche_material")
    escuche_cantidad = fields.Int(attribute="escuche_cantidad")
    lentes_material = fields.String(attribute="lentes_material")
    lentes_cantidad = fields.Int(attribute="lentes_cantidad")

sede_reservada_schema = SedesReservadasSchema()
sedes_reservadas_schema = SedesReservadasSchema(many=True)