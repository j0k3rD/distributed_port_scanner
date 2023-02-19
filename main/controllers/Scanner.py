from flask_restful import Resource
from flask import request
from main.services import ScannerService, UserService
from main.map import ScannerSchema, UserSchema


class Scanner(Resource):
    '''
    Clase que representa el controlador de la entidad Search

    param:
        - Resource: Clase de la cual hereda
    '''

    def __init__(self):
        self.__schema = ScannerSchema()
        self.__service = ScannerService()

    def get(self, id):
        '''
        Función que obtiene un busqueda por su id

        args:
            - id: id de la busqueda
        return:
            - Busqueda en formato json o error 404
        '''
        return self.__schema.dump(self.__service.get_by_id(id)), 201
            
    '''
    TODO: Implementar delete y put en caso de agregar administrador.     
    def delete(self, id):
        pass

    def put(self, id):
        pass
    '''


class Scanners(Resource):
    '''
    Clase que representa el controlador de la entidad Searchs

    param:
        - Resource: Clase de la cual hereda
    '''
    def __init__(self):
        self.__schema = ScannerSchema()
        self.__user_service = UserService()
        self.__user_schema = UserSchema()
        self.__service = ScannerService()

    def get(self):
        '''
        Función que obtiene todos las busquedas

        return:
            - Lista de busquedas en formato json
        '''
        model = self.__schema.dump(self.__service.get_all(), many=True)
        return model, 201

    def post(self):
        '''
        Función que guarda la busqueda

        return:
            - Busqueda en formato json
        '''
        # Json values
        user_json = request.json
        mac = user_json['mac']

        page_json = request.json
        scanner_type = page_json['scanner_type']
        ip = page_json['ip']
        port = page_json['port']
        result = page_json['result']

        @self.__user_validate.get_user(mac)
        def validater():
            user = self.__user_schema.dump(self.__user_service.get_by_mac())
            data = {
                "mac": user_json['mac'],
                "scanner_type": scanner_type,
                "ip": ip,
                "port": port,
                "result": result,
                "user_id": user["id"]
            }
            model = self.__schema.load(data)
            return self.__schema.dump(self.__service.add(model)), 201

        return validater()