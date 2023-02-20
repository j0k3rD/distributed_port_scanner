from flask_restful import Resource
from flask import request
from main.services import UserService
from main.map import UserSchema
from main.validate import UserValidate


class User(Resource):
    '''
    Clase que representa el controlador de la entidad User

    param:
        - Resource: Clase de la cual hereda
    '''
    def __init__(self):
        self.__schema = UserSchema()
        self.__service = UserService()
        self.__validate = UserValidate()


    def get(self, id):
        '''
        Función que obtiene un usuario por su id

        args:
            - id: id del usuario
        return:
            - Usuario en formato json o error 404
        '''
        @self.__validate.validate_user(id)
        def validater():
            return self.__schema.dump(self.__service.get_by_id(id)), 201
        return validater()
            
    '''
    TODO: Implementar delete y put en caso de agregar administrador.     
    def delete(self, id):
        pass

    def put(self, id):
        pass
    '''


class Users(Resource):
    '''
    Clase que representa el controlador de la entidad Users

    param:
        - Resource: Clase de la cual hereda
    '''
    def __init__(self):
        self.__schema = UserSchema()
        self.__service = UserService()

    def get(self):
        '''
        Función que obtiene todos los usuarios

        return:
            - Lista de usuarios en formato json
        '''
        model = self.__schema.dump(self.__service.get_all(), many=True)
        return model, 201

    def post(self):
        '''
        Función que verifica si un usuario ya existe y lo crea en caso de no existir

        return:
            - Usuario en formato json o usuario ya registrado 201
        '''
        # Json values.
        user_json = request.json
        mac = user_json["mac"]

        # Validate if user already exists.
        if self.__service.get_by_mac(mac):
            return f'User already exists by MAC, {mac}', 202
    
        # Create user.
        data = {
            "mac": mac,
        }
        model = self.__schema.load(data)
        return self.__schema.dump(self.__service.add(model)), 201