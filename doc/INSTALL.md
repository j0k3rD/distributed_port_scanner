<h3>Install</h3>

1. Create a new folder named *`project`*: ``` mkdir project ```
2. Into the folder create a Python Enviroment: ``` python3 -m venv project ```
3. Start enviroment: ```source /project/bin/activate/```
4. Clone the repository into the enviroment.

5. **Celery:**
  - Install [Celery](https://pypi.org/project/celery/)
  - In Ubuntu: ```
    sudo pip install celery```
6. **Redis:**
  - Install [Redis](https://redis.io/docs/getting-started/installation/)
  - In Ubuntu: ```
    sudo apt install redis```
7. **Django:**
  - Install [Django](https://docs.djangoproject.com/en/4.1/topics/install/)
  - In Ubuntu: ```
    sudo apt install python3-django```
8. **NMap:**
  - Install [Nmap](https://phoenixnap.com/kb/how-to-install-nmap-ubuntu)
  - In Ubuntu: ```
    sudo apt-get install nmap```
9. Inside the project directory run: ```
    pip install -r requirements.txt```
10. Then run run: ```
    python3 manage.py migrate``` 
11. In another terminal run: ```
    redis-server```
12. In a second terminal run: ```
    python3 manage.py runserver ```
13. Finally in a third terminal run: ```
    celery -A distributed_scanner worker -B -l info```
14. Open *0.0.0.0:8000//* in your browser.
15. Make your owns scanners :D
