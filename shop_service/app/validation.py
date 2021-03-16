from marshmallow import Schema, fields, validate





class CreateProductSchema(Schema):
    name = fields.String()
    price = fields.Integer(strict=True, validate=validate.Range(min=1))
    count = fields.Integer(strict=True, validate=validate.Range(min=1))
    description = fields.String(default=None)
    category = fields.String()


class CreatePurchaseSchema(Schema):
    name = fields.String()
    count = fields.Integer(validate=validate.Range(min=1))


class CreateShopSchema(Schema):
    name = fields.String()
    address = fields.String()
    phone = fields.String()


class DeliveryProductSchema(Schema):
    name = fields.String()
    count = fields.Integer(strict=True)


class BuyInputSchema(Schema):
    shop = fields.String(strict=True)
    user = fields.Integer()
    payment = fields.String()
    purchases = fields.Nested(CreatePurchaseSchema(many=True))


class OutputPurchaseSchema(Schema):
    name = fields.String()
    price = fields.Integer()
    count = fields.Integer()


class BuyOutputSchema(Schema):
    shop = fields.String()
    payment = fields.String()
    total = fields.Integer()
    purchases = fields.Nested(OutputPurchaseSchema(many=True))
