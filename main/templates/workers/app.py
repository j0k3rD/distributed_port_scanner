import os

def create_celery():
    os.system('celery -A main.tasks worker --loglevel=INFO -c 3')

if __name__ == '__main__':
    create_celery()