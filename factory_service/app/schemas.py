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
