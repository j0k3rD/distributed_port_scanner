from main.repositories.scanner_repository import ScannerRepository
from main.services.services import Service

repository = ScannerRepository()

class ScannerService(Service):
    '''
    Clase que representa el servicio de la entidad Scanner

    param:
        - Service: Clase que hereda de la interfaz Service
    '''

    def add(self, model):
        return repository.create(model)
        
    def get_all(self):
        return repository.find_all()

    def get_by_id(self, id):
        return repository.find_by_id(id = id)

    def get_by_user_id(self, user_id):
        '''
        Método que obtiene un curso por su url

        param:
            - user_id: Id del usuario
        return:
            - model: Modelo de la entidad Search
        '''
        return repository.find_by_user_id(user_id = user_id)