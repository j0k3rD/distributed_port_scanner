from main import create_app
from dotenv import load_dotenv
import os

app = create_app()

load_dotenv()

# os.system('celery -A main.tasks worker --loglevel=INFO -c 3')

if __name__ == '__main__':
    app.run(debug=True)