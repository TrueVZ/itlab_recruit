from marshmallow import Schema, fields


class CreatePurchaseSchema(Schema):
    name = fields.String()
    count = fields.Integer()
    category = fields.String()
    price = fields.Integer()


class CreateCheckSchema(Schema):
    total = fields.Integer()
    shop = fields.String()
    payment = fields.String()
    purchases = fields.Nested(CreatePurchaseSchema(many=True))
