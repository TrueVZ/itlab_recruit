import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_USER = os.environ.get("DB_USER") or "user"
DB_PASS = os.environ.get("DB_PASS") or "hackme"
DB_NAME = os.environ.get("DB_NAME") or "shop-app"
DB_HOST = os.environ.get("DB_HOST") or "localhost"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hackme"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    DEBUG = True


class ProdConfig(Config):
    ENV = "prod"
    DEBUG = False


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True


class Test(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
