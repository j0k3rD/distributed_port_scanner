from main.repositories.repository import Create, Delete, Read, Update
from main.models import ScannerModel
from .. import db

# TODO: Implementar delete en caso de agregar administrador para eliminar cursos.
class ScannerRepository(Create, Read, Update):
    '''
    Clase que representa el repositorio de la entidad Search

    param:
        - Create: Clase que hereda de la interfaz Create
        - Read: Clase que hereda de la interfaz Read
        - Update: Clase que hereda de la interfaz Update
    '''
    def __init__(self):
        self.__type_model = ScannerModel
    
    def create(self, model: db.Model):
        db.session.add(model)
        db.session.commit()
        return model

    def find_all(self):
        model = db.session.query(self.__type_model).all()
        return model

    def find_by_id(self, id: int) -> db.Model:
        model = db.session.query(self.__type_model).filter_by(id=id).first() 
        return model

    def find_by_user_id(self, user_id: int) -> db.Model:
        model = db.session.query(self.__type_model).filter(self.__type_model.user_id == user_id).order_by(self.__type_model.id.desc()).first()
        return model

    def update(self, model: db.Model):
        db.session.commit()
        return model