from main.repositories.repository import Create, Delete, Read, Update 
from main.models import UserModel
from .. import db

# TODO: Implementar delete en caso de agregar administrador para eliminar cursos.
class UserRepository(Create, Read):
    '''
    Clase que representa el repositorio de la entidad User

    param:
        - Create: Clase que hereda de la interfaz Create
        - Read: Clase que hereda de la interfaz Read
        - Update: Clase que hereda de la interfaz Update
    '''
    def __init__(self):
        self.__type_model = UserModel

    @property
    def type_model(self):
        return self.__type_model
    
    def create(self, model: db.Model):
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        model = db.session.query(self.type_model).all()
        return model

    def find_by_id(self, id: int) -> db.Model:
        model = db.session.query(self.type_model).filter_by(id=id).first() 
        return model

    def find_by_mac(self, mac: str) -> db.Model:
        model = db.session.query(self.type_model).filter(self.type_model.mac == mac).first()
        return model