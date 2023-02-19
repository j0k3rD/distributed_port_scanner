from main.services.user_service import UserService

service = UserService()

class UserValidate():
    '''
    Clase que valida los datos de la entidad User
    '''

    def validate_user(self, id):
        '''
        Función que valida si el usuario existe

        param:
            - id: id del usuario
        return:
            - Función: Si el usuario existe
            - Error: Si el usuario no existe
        '''
        def decorator(function):
            def wrapper(*args, **kwargs):
                if service.get_by_id(id):
                    return function(*args, **kwargs)
                return 'User not found', 404
            return wrapper
        return decorator

    def get_user(self, mac):
        '''
        Función que valida si el usuario existe

        param:
            - discord_id: id de la busqueda
        return:
            - Función: Si el usuario existe
            - Error: Si el usuario no existe
        '''
        def decorator(function):
            def wrapper(*args, **kwargs):
                if service.get_by_mac(mac):
                    return function(*args, **kwargs)
                return f'User not found by MAC, {mac}', 404
            return wrapper
        return decorator