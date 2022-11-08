from marshmallow import Schema, fields

from app.schemas.proovedor import ProovedorSchema
from app.schemas.material import MaterialSchema

class  RenglonSchema(Schema):
    proovedor= fields.Nested(ProovedorSchema)
    material= fields.Nested(MaterialSchema)
    cantidad = fields.Int(attribute="cantidad")

renglon_schema = RenglonSchema()
renglones_schema = RenglonSchema(many=True)
