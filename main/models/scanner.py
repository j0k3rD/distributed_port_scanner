#Modelo de la base de datos de los escaneos
from .. import db
from sqlalchemy.ext.hybrid import hybrid_property

class Scanner(db.Model):
    __tablename__ = 'scanners'
    __id = db.Column('id', db.Integer, primary_key=True)
    __scanner_type = db.Column('scanner_type', db.String(255))
    __ip = db.Column('ip', db.String(255))
    __port = db.Column('port', db.String(255))
    __created_at = db.Column('create_at', db.DateTime, nullable=False)
    __user_id = db.Column('user_id', db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='scanner')

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