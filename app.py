from main import create_app
from dotenv import load_dotenv
import os
from multiprocessing import Process

app = create_app()

load_dotenv()

if __name__ == '__main__':
    app.run(debug=True)