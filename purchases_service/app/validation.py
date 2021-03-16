from marshmallow import Schema, fields


class CreatePurchaseSchema(Schema):
    name = fields.String()
    count = fields.Integer()


class CreateCheckSchema(Schema):
    shop = fields.String()
    payment = fields.String()
    purchases = fields.Nested(CreatePurchaseSchema(many=True))
