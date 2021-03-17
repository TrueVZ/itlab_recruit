from marshmallow import Schema, fields, validate


class CreatePurchaseSchema(Schema):
    name = fields.String()
    count = fields.Integer(strict=True, validate=validate.Range(min=1))


class CreateCheckSchema(Schema):
    shop = fields.String()
    payment = fields.String()
    purchases = fields.Nested(CreatePurchaseSchema(many=True))
