from celery import Celery
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(__name__)

celery.config_from_object(Config)

from . import views

if __name__ == '__main__':
    app.run(debug=True)