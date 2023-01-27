#Guardar el resultado del escaneo en base de datos
import mysql.connector
import sys

#Conectar a la base de datos
mydb = mysql.connector.connect( host="localhost",
                                user="root",
                                password="root",
                                database="port_scanning" )

#Crear cursor
mycursor = mydb.cursor()

#Crear tabla
mycursor.execute("CREATE TABLE IF NOT EXISTS port_scanning (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(255), port VARCHAR(255))")

#Guardar los datos en la base de datos
ip = sys.argv[1]
port = sys.argv[2]
sql = "INSERT INTO port_scanning (ip, port) VALUES (%s, %s)"
val = (ip, port)
mycursor.execute(sql, val)
mydb.commit()

#Cerrar conexion
mydb.close()