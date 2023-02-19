from main.repositories import UserRepository
from main.services.services import Service

repository = UserRepository()

class UserService(Service):
    '''
    Clase que representa el servicio de la entidad User

    param:
        - Service: Clase que hereda de la interfaz Service
    '''

    def add(self, model):
        return repository.create(model)
        
    def get_all(self):
        return repository.find_all()

    def get_by_id(self, id):
        return repository.find_by_id(id = id)

    def get_by_mac(self, mac):
        '''
        Método que obtiene un usuario por su id de discord

        param:
            - discord_id: id de discord del usuario
        return:
            - User: Objeto de tipo User
        '''
        return repository.find_by_mac(mac = mac)