import mysql.connector
import pymongo
from pprint import pprint

def main():
    # 1. Conexión MySQL
    mysql_conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='bd_gasolineras',   # Ajusta al nombre real de tu BD
        port=3306
    )
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    # 2. Conexión MongoDB
    mongo_client = pymongo.MongoClient(
        "mongodb+srv://root:01qwerty@cluster0.5jh8u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    mongo_db = mongo_client["bd_gasolineras_mongo"]  # Ajusta al nombre real de tu BD en Mongo

    # 3. Validar Provincias
    print("=== PROVINCIAS ===")
    mysql_cursor.execute("SELECT * FROM provincias")
    provincias_mysql = mysql_cursor.fetchall()
    provincias_mongo = list(mongo_db["provincias"].find({}))

    print(f" MySQL -> {len(provincias_mysql)} registros")
    print(f" Mongo -> {len(provincias_mongo)} documentos")
    if provincias_mysql:
        print(" Ejemplo MySQL:", provincias_mysql[0])
    if provincias_mongo:
        print(" Ejemplo Mongo:", provincias_mongo[0])
    print("-"*40)

    # 4. Validar Municipios
    print("=== MUNICIPIOS ===")
    mysql_cursor.execute("SELECT * FROM municipios")
    municipios_mysql = mysql_cursor.fetchall()
    municipios_mongo = list(mongo_db["municipios"].find({}))

    print(f" MySQL -> {len(municipios_mysql)} registros")
    print(f" Mongo -> {len(municipios_mongo)} documentos")
    if municipios_mysql:
        print(" Ejemplo MySQL:", municipios_mysql[0])
    if municipios_mongo:
        print(" Ejemplo Mongo:", municipios_mongo[0])
    print("-"*40)

    # 5. Validar Localidades
    print("=== LOCALIDADES ===")
    mysql_cursor.execute("SELECT * FROM localidades")
    localidades_mysql = mysql_cursor.fetchall()
    localidades_mongo = list(mongo_db["localidades"].find({}))

    print(f" MySQL -> {len(localidades_mysql)} registros")
    print(f" Mongo -> {len(localidades_mongo)} documentos")
    if localidades_mysql:
        print(" Ejemplo MySQL:", localidades_mysql[0])
    if localidades_mongo:
        print(" Ejemplo Mongo:", localidades_mongo[0])
    print("-"*40)

    # 6. Validar Carburantes
    print("=== CARBURANTES ===")
    mysql_cursor.execute("SELECT * FROM carburantes")
    carburantes_mysql = mysql_cursor.fetchall()
    carburantes_mongo = list(mongo_db["carburantes"].find({}))

    print(f" MySQL -> {len(carburantes_mysql)} registros")
    print(f" Mongo -> {len(carburantes_mongo)} documentos")
    if carburantes_mysql:
        print(" Ejemplo MySQL:", carburantes_mysql[0])
    if carburantes_mongo:
        print(" Ejemplo Mongo:", carburantes_mongo[0])
    print("-"*40)

    # 7. Validar Rótulos
    print("=== ROTULOS ===")
    mysql_cursor.execute("SELECT * FROM rotulos")
    rotulos_mysql = mysql_cursor.fetchall()
    rotulos_mongo = list(mongo_db["rotulos"].find({}))

    print(f" MySQL -> {len(rotulos_mysql)} registros")
    print(f" Mongo -> {len(rotulos_mongo)} documentos")
    if rotulos_mysql:
        print(" Ejemplo MySQL:", rotulos_mysql[0])
    if rotulos_mongo:
        print(" Ejemplo Mongo:", rotulos_mongo[0])
    print("-"*40)

    # 8. Validar Estaciones
    #    Aquí la estructura en Mongo es más compleja (con los campos anidados).
    print("=== ESTACIONES ===")
    mysql_cursor.execute("SELECT * FROM estaciones")
    estaciones_mysql = mysql_cursor.fetchall()
    estaciones_mongo = list(mongo_db["estaciones"].find({}))

    print(f" MySQL -> {len(estaciones_mysql)} registros")
    print(f" Mongo -> {len(estaciones_mongo)} documentos")
    if estaciones_mysql:
        print(" Ejemplo MySQL:", estaciones_mysql[0])
    if estaciones_mongo:
        print(" Ejemplo Mongo (estructura anidada):")
        pprint(estaciones_mongo[0])  # pprint para ver la jerarquía más clara
    print("-"*40)

    # 9. Cierre de conexiones
    mysql_cursor.close()
    mysql_conn.close()
    mongo_client.close()

if __name__ == "__main__":
    main()
