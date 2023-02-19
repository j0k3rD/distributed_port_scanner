from main.services.scanner_service import ScannerService

service = ScannerService()

class ScannerValidate():
    '''
    Clase que valida los datos de la entidad Scanner
    '''

    def validate_scanner(self, id):
        '''
        Función que valida si la busqueda existe

        param:
            - id: id de la busqueda
        return:
            - Función: Si la busqueda existe
            - Error: Si la busqueda no existe
        '''
        def decorator(function):
            def wrapper(*args, **kwargs):
                if service.get_by_id(id):
                    return function(*args, **kwargs)
                return 'Scanner not found by id, {id}', 404
            return wrapper
        return decorator

    def get_by_user_id(self, user_id):
        '''
        Función que valida si la busqueda existe

        param:
            - user_id: id del usuario
        return:
            - Función: Si la busqueda existe
            - Error: Si la busqueda no existe
        '''
        def decorator(function):
            def wrapper(*args, **kwargs):
                if service.get_by_user_id(user_id):
                    return function(*args, **kwargs)
                return f'Scanner not found by user_id, {user_id}', 404
            return wrapper
        return decorator