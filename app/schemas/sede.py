from marshmallow import Schema, fields


class  SedeSchema(Schema):
    id = fields.Int(attribute="id_sede")
    nombre = fields.String(attribute="nombre")
    fabrica = fields.String(attribute="fabrica")
    inicio_disponibilidad = fields.DateTime(attribute="inicio_disponibilidad")
    fin_disponibilidad = fields.DateTime(attribute="fin_disponibilidad")

sede_schema = SedeSchema()
sedes_schema= SedeSchema(many=True)