from flask import Flask
from .config import DevConfig, Test
from app.extensions import db, migrate, ma


def create_app(testing=False):
    app = Flask(__name__)
    return app