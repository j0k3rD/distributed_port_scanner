class Config():

    SECRET_KEY = "justasecretkey"

    #Celery
    BROKER_URL = 'redis://localhost:6379/0'
    RESULT_BACKEND = 'redis://localhost:6379/0'
    TASK_SERIALIZER = 'json'
    RESULT_SERIALIZER = 'json'
    CELERY_ENABLE_UTC = True

    #Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False