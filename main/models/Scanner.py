#Modelo de la base de datos de los escaneos
from .. import db

class Scanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255))
    port = db.Column(db.String(255))

    def __repr__(self):
        return f"Scanners('{self.ip}', '{self.port}')"

def to_json(self):
    return {
        'id': self.id,
        'ip': self.ip,
        'port': self.port
    }

@staticmethod
def from_json(json):
    id = json.get('id')
    ip = json.get('ip')
    port = json.get('port')
    return Scanner(id=id, ip=ip, port=port)