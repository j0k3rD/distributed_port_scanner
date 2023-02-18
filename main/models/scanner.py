#Modelo de la base de datos de los escaneos
from .. import db
from sqlalchemy.ext.hybrid import hybrid_property

class Scanner(db.Model):
    __id = db.Column(db.Integer, primary_key=True)
    __scanner_type = db.Column(db.String(255))
    __ip = db.Column(db.String(255))
    __port = db.Column(db.String(255))
    __created_at = db.Column(db.DateTime, nullable=False)
    __user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backpopulates='scanners')

    def __repr__(self):
        return f"Scanners('{self.__id}, '{self.__scanner_type}', '{self.__ip}', '{self.__port})"

    @hybrid_property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id
    
    @hybrid_property
    def scanner_type(self):
        return self.__scanner_type
    
    @scanner_type.setter
    def scanner_type(self, scanner_type):
        self.__scanner_type = scanner_type
    
    @hybrid_property
    def ip(self):
        return self.__ip
    
    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @hybrid_property
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, port):
        self.__port = port

    @hybrid_property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at

    @hybrid_property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id