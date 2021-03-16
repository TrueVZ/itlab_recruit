import pytest

from app import create_app
from app import db as _db
from app.models import *


@pytest.fixture(scope="session")
def app(request):
    app = create_app(testing=True)

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return testing_client


@pytest.fixture(scope="session")
def db(app):

    _db.app = app
    _db.create_all()

    return _db


@pytest.fixture(scope="function")
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
