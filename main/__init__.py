from celery import Celery
from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Agregamos las Blueprints
    from .views import app as main_blueprint
    app.register_blueprint(main_blueprint)

    celery = Celery(__name__)
    celery.config_from_object(Config)

    from . import views
    return app