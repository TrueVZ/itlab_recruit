from flask import Flask
from .config import DevConfig, Test
from app.extensions import db, migrate, ma
from .models import *

import app.routes


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(routes.bp)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    return app
