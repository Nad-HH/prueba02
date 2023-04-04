import mysql.connector

#datos de acceso para conectarnos a la base de datos:

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='serviciogerencial'
)

