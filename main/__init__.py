from celery import Celery
from flask import Flask
from .config import Config
from .models import db
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os


api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Base de datos
    #Si la base de datos no existe, se crea
    if not os.path.exists(os.getenv('DATABASE')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE')+os.getenv('DATABASE_NAME'))
    
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')

    db.init_app(app)

    #Agregar Resources
    import main.resources as resource

    api.add_resource(resource.ScannerResource, '/scanner/<id>')
    api.add_resource(resource.ScannersResource, '/scanners')


    #Agregamos las Blueprints
    from .views import app as main_blueprint
    app.register_blueprint(main_blueprint)

    celery = Celery(__name__)
    celery.config_from_object(Config)

    from . import views
    return app