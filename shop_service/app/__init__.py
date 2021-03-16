from flask import Flask
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from .config import DevConfig, Test
from app.extensions import db, migrate, ma

from .models import *
from .schemas import *
from .validation import *

import app.routes


spec = APISpec(
    title="ShopService API",
    version="0.0.1",
    openapi_version="3.0.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


def load_docstrings(spec, app):
    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == "static":
                continue
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    write_yaml_file(spec)


def write_yaml_file(spec: APISpec):
    with open("docs.yaml", "w") as file:
        file.write(spec.to_yaml())


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object(Test)
    else:
        app.config.from_object(DevConfig)
    app.register_blueprint(routes.bp, url_prefix="/api")
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    load_docstrings(spec, app)
    return app
