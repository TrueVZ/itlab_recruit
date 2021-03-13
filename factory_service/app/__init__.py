from flask import Flask
from celery import Celery
from config import Config
from app.extensions import db, migrate, ma
from .models import *


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    return app


def make_celery(app=None):
    app = app or create_app()
    _celery = Celery("app", broker=app.config["CELERY_BROKER_URL"])
    _celery.conf.update(app.config)
    TaskBase = _celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
    return _celery
