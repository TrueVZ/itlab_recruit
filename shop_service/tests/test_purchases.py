import random

random.seed(1)


class TestShop:
    def test_create_shop(self, app, session):
        res = app.post("/api/shop/create", json=dict(name="test1", address="some address", phone="+7912"))
        assert res.status_code == 200
        assert res.json["name"] == "test1"
        assert res.json["address"] == "some address"

    def test_error_create_shop(self, app, session):
        res = app.post("/api/shop/create", json=dict(name="test1", address="some", phone=1234))
        assert res.status_code == 422

    def test_create_product(self, app, session):
        app.post("/api/shop/create", json=dict(name="test1", address="some address", phone="+7912"))
        products = []
        for i in range(5):
            products.append(dict(name=f"product{i}", price=random.randint(0, 100000), description="test", category="category1"))
        res = app.post("/api/shop/1/product", json=dict(products=products))
        assert res.status_code == 200

    def test_get_shop_notfound(self, app, session):
        res = app.get("/api/shop/1")
        assert res.status_code == 404

    def test_get_product_category(self, app, session):
        app.post("/api/shop/create", json=dict(name="test1", address="some address", phone="+7912"))
        res = app.post("/api/shop/1/product", json=dict(products=products))
