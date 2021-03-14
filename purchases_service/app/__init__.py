from flask import Flask
from flasgger import Swagger
from flasgger.utils import apispec_to_template
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
    title="PurchasesService API",
    version="0.0.1",
    openapi_version="2.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(routes.bp)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    template = apispec_to_template(
        app=app, spec=spec, definitions=[CreateCheckSchema, CheckSchema, UserSchema]
    )
    app.config["SWAGGER"] = {"uiversion": 3}
    swag = Swagger(app, template=template)
    return app
