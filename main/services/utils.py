import requests

#Obtener los datos del escaneo por id
def get_scanner(id):
    url = 'http://localhost:5000/scanners/{}'.format(id)
    response = requests.get(url)
    return response.json()

#Crear un nuevo escaneo
def create_scanner(ip, port):
    url = 'http://localhost:5000/scanners'
    data = {
        'ip': ip,
        'port': port
    }
    response = requests.post(url, json=data)
    return response.json()


#TODO: Esto se guarda para el futuro cuando se implemente un ADMIN.
# #Actualizar los datos del escaneo
# def update_scanner(id, ip, port):
#     url = 'http://localhost:5000/scanners/{}'.format(id)
#     data = {
#         'ip': ip,
#         'port': port
#     }
#     response = requests.put(url, json=data)
#     return response.json()

# #Eliminar los datos del escaneo
# def delete_scanner(id):
#     url = 'http://localhost:5000/scanners/{}'.format(id)
#     response = requests.delete(url)
#     return response.json()