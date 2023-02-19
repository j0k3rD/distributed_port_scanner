class Config():
    #Celery
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    TASK_SERIALIZER = 'json'
    RESULT_SERIALIZER = 'json'
    CELERY_ENABLE_UTC = True
