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
        exclude = ("products", )

    products = ma.Nested(ProductSchema, many=True)


class PurchaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Purchase
        load_instance = True


purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
shop_schema = ShopSchema(only=("name", "id", "address", "phone"))
shops_schema = ShopSchema(only=("name", "id"), many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
purchase_out_schema = PurchaseSchema(only=("name", "price", "count"))
