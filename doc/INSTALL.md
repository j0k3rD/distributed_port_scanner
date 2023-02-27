<h3>Install</h3>

- 1 - Download or clone the repository to your local environment.
- 2 - **Celery:**
  - Install [Celery](https://pypi.org/project/celery/)
  - In Ubuntu: ```
    sudo pip install celery```
- 3 - **Redis:**
  - Install [Redis](https://redis.io/docs/getting-started/installation/)
  - In Ubuntu:```
    sudo apt install redis```
- 4 - **Django:**
  - Install [Django](https://docs.djangoproject.com/en/4.1/topics/install/)
  - In Ubuntu: ```
    sudo apt install python3-django```
- 5 - Inside the project directory run: ```
    pip install -r requirements.txt```
- 6 - Then: ```
    python3 manage.py migrate``` 
- 6 - Finally Run: ```
    python3 manage.py runserver```
- 7 - Then Run in another terminal: ```
    celery -A distributed_scanner worker -B -l info```
- 8 - Open *127.0.0.1:8000/scanner/list/* in your browser.
- 9 - Make your owns scanners :D
