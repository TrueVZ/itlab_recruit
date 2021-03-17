from app import ma
from app.models import User, Purchase, Check


class PurchaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Purchase
        load_instance = True


class CheckSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Check
        load_instance = True

    purchases = ma.Nested(
        PurchaseSchema, many=True, only=("id", "name", "price", "count", "category")
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("checks",)

    checks = ma.Nested(CheckSchema, many=True)


user_schema = UserSchema(only=("id", "username"))
users_schema = UserSchema(many=True, only=("id", "username"))
check_schema = CheckSchema()
checks_schema = CheckSchema(many=True)
purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
