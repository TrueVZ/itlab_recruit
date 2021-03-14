from app.extensions import ma
from app.models import Factory, Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


class FactorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Factory
        load_instance = True

    products = ma.Nested(ProductSchema, many=True)


products_schema = ProductSchema(many=True, only=("name", "count", "shop_id"))
products_task_schema = ProductSchema(many=True, only=("name", "count"))
factory_schema = FactorySchema(only=("name", "products"))
