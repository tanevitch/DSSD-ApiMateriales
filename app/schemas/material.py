from marshmallow import Schema, fields


class  MaterialSchema(Schema):
    id = fields.Int(attribute="id_material")
    nombre = fields.String(attribute="nombre")
    descripcion = fields.String(attribute="descripcion")

material_schema = MaterialSchema()
materiales_schema= MaterialSchema(many=True)