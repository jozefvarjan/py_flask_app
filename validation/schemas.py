from marshmallow import Schema, fields 

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    format = fields.Str(required=True)
    year = fields.Int(required=True)
    price = fields.Float(required=True)
   

class ItemUpdateSchema(Schema):
    id = fields.Str(required=True)


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


