from marshmallow import Schema, fields


class  SedeSchema(Schema):
    id = fields.Int(attribute="id_sede")
    nombre = fields.String(attribute="nombre")
    fabrica = fields.String(attribute="fabrica")


sede_schema = SedeSchema()
sedes_schema= SedeSchema(many=True)