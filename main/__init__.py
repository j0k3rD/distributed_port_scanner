from celery import Celery
from flask import Flask
from .config import Config
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    load_dotenv()


    #Cargo la configuracion de la base de datos
    app.config['API_URL'] = os.getenv('API_URL')

    #Base de datos
    # Si no existe el archivo de base de datos crearlo (para SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))
    
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)

    #Agregamos las Blueprints
    from .views import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    #Agregar Resources
    import main.controllers as controller

    api.add_resource(controller.UserController, '/user/<int:id>')
    api.add_resource(controller.UsersController, '/users')
    api.add_resource(controller.ScannerController, '/scanner/<int:id>')
    api.add_resource(controller.ScannersController, '/scanners')
    api.init_app(app)

    celery = Celery(__name__)
    celery.config_from_object(Config)
    celery.conf.update(app.config)

    from main import tasks
    
    return app, celery