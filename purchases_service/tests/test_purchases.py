class TestUser:
    def test_create_user(self, app, session):
        res = app.post("/api/user/create", json=dict(username="test1"))
        print(res)
        assert res.status_code == 200
        assert res.json["id"] == 1
        assert res.json["username"] == "test1"

    def test_get_user_by_id(self, app, session):
        app.post("/api/user/create", json=dict(username="test1"))
        res = app.get("/api/user/1")
        assert res.status_code == 200
        assert res.json["id"] == 1
        assert res.json["username"] == "test1"

    def test_all_users(self, app, session):
        app.post("/api/user/create", json=dict(username="test1"))
        app.post("/api/user/create", json=dict(username="test2"))
        res = app.get("/api/user")
        assert res.status_code == 200
        assert res.json["users"][0]["id"] == 1
        assert res.json["users"][1]["id"] == 2
