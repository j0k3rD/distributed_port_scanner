from .. import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'users'
    __id = db.Column('id', db.Integer, primary_key=True)
    __mac = db.Column('mac', db.String(255), unique=True, nullable=False)
    __created_at = db.Column('create_at', db.DateTime, nullable=False)

    scanner = db.relationship('Scanner', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'User({self.__id}{self.__mac})'

    @hybrid_property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @hybrid_property
    def mac(self):
        return self.__mac
    
    @mac.setter
    def mac(self, mac):
        self.__mac = mac
    
    @hybrid_property
    def created_at(self):
        return self.__created_at
    
    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at