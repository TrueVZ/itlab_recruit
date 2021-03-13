from app import ma
from app.models import Shop, Purchase, Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


class ShopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shop
        load_instance = True

    products = ma.Nested(ProductSchema, many=True)


class PurchaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Purchase
        load_instance = True
