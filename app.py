from main import create_app
from dotenv import load_dotenv
from main import db

app, celery = create_app()
app.app_context().push()

load_dotenv()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)