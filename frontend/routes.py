try:
    from flask import app, Flask, request
    from flask_restful import Resource, Api, reqparse
    import redis
    from tasks import scan_ports_python
    from celery import Celery
except Exception as e:
    print("Error: {}".format(e))

#-------- Settings --------#
app = Flask(__name__)
api = Api(app)

#-------- Redis --------#
redis = redis.Redis(host='localhost', port=6379, db=0)

#-------- Celery --------#
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'


#-------- Routes --------#
class Controller(Resource):
    def get(self):
        return "Hello World!"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ipv4', type=str, help='IPv4')
        parser.add_argument('port', type=str, help='Port')
        args = parser.parse_args()
        ipv4 = args['ipv4']
        port = args['port']
        scan_ports_python.delay(ipv4, port)
        return "Scanning..."

api.add_resource(Controller, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
