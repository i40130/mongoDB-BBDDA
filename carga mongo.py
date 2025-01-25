import mysql.connector
import pymongo
import json


# Ejemplo de conexión MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='bd_gasolineras',
    port=3306
)

mysql_cursor = mysql_conn.cursor(dictionary=True)


mysql_cursor.execute("SELECT * FROM provincias")
provincias = mysql_cursor.fetchall()  # Lista de diccionarios

# Ejemplo de conexión Mongo
mongo_client = pymongo.MongoClient(
    "mongodb+srv://root:01qwerty@cluster0.5jh8u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tls=True,
    tlsAllowInvalidCertificates=True
)
mongo_db = mongo_client["bd_gasolineras_mongo"]

estaciones_collection = mongo_db["estaciones"]
provincias_collection = mongo_db["provincias"]
municipios_collection = mongo_db["municipios"]
localidades_collection = mongo_db["localidades"]
rotulos_collection = mongo_db["rotulos"]
carburantes_collection = mongo_db["carburantes"]


# Guardar a JSON (opcional si lo deseas)
with open("provincias.json", "w", encoding="utf-8") as f:
    json.dump(provincias, f, ensure_ascii=False, indent=4)

# Insertar en MongoDB
if provincias:
    # Limpia la colección antes, si quieres:
    provincias_collection.delete_many({})
    # Inserta todos
    provincias_collection.insert_many(provincias)


mysql_cursor.execute("SELECT * FROM municipios")
municipios = mysql_cursor.fetchall()

# JSON
with open("municipios.json", "w", encoding="utf-8") as f:
    json.dump(municipios, f, ensure_ascii=False, indent=4)

# Mongo
if municipios:
    municipios_collection.delete_many({})
    municipios_collection.insert_many(municipios)

mysql_cursor.execute("SELECT * FROM localidades")
localidades = mysql_cursor.fetchall()

with open("localidades.json", "w", encoding="utf-8") as f:
    json.dump(localidades, f, ensure_ascii=False, indent=4)

if localidades:
    localidades_collection.delete_many({})
    localidades_collection.insert_many(localidades)


mysql_cursor.execute("SELECT * FROM carburantes")
carburantes = mysql_cursor.fetchall()

with open("carburantes.json", "w", encoding="utf-8") as f:
    json.dump(carburantes, f, ensure_ascii=False, indent=4)

if carburantes:
    carburantes_collection.delete_many({})
    carburantes_collection.insert_many(carburantes)


mysql_cursor.execute("SELECT * FROM rotulos")
rotulos = mysql_cursor.fetchall()

with open("rotulos.json", "w", encoding="utf-8") as f:
    json.dump(rotulos, f, ensure_ascii=False, indent=4)

if rotulos:
    rotulos_collection.delete_many({})
    rotulos_collection.insert_many(rotulos)

query_estaciones = """
SELECT
    e.idEstacion,
    e.idRotulo,
    r.nomRotulo,
    e.codigoPostal,
    e.direccion,
    e.margen,
    e.longitud,
    e.latitud,
    e.horario,
    e.esTerrestre,
    l.idLocalidad,
    l.nomLocalidad,
    m.idMunicipio,
    m.nomMunicipio,
    p.idProvincia,
    p.nomProvincia
FROM estaciones e
JOIN localidades l ON e.idLocalidad = l.idLocalidad
JOIN municipios m ON l.idMunicipio = m.idMunicipio
JOIN provincias p ON m.idProvincia = p.idProvincia
JOIN rotulos r ON e.idRotulo = r.idRotulo
"""

mysql_cursor.execute(query_estaciones)
estaciones_bruto = mysql_cursor.fetchall()  # lista de diccionarios

query_tarifas = """
SELECT 
    t.precio, 
    t.fecha,
    c.idCarburante,
    c.nomCarburante
FROM tarifas t
JOIN carburantes c ON t.idCarburante = c.idCarburante
WHERE t.idEstacion = %s
"""

def obtener_tarifas_de_estacion(id_estacion, cursor):
    cursor.execute(query_tarifas, (id_estacion,))
    rows = cursor.fetchall()
    tarifas_list = []
    for row in rows:
        tarifas_list.append({
            "carburante": {
                "idCarburante": row["idCarburante"],
                "nomCarburante": row["nomCarburante"]
            },
            "fecha": row["fecha"],   # Podrías convertir a date si quisieras
            "precio": row["precio"]
        })
    return tarifas_list

estaciones_transformadas = []

for est_row in estaciones_bruto:
    id_estacion = est_row["idEstacion"]
    # Llamamos a la función de tarifas
    tarifas_est = obtener_tarifas_de_estacion(id_estacion, mysql_cursor)
    
    estacion_doc = {
        "idEstacion": est_row["idEstacion"],
        "idRotulo":   est_row["idRotulo"],
        # El mapping no lo muestra, pero si quisieras "nomRotulo", podrías añadirlo:
        # "nomRotulo":  est_row["nomRotulo"], 
        "codigoPostal": est_row["codigoPostal"],
        "direccion":  est_row["direccion"],
        "margen":     est_row["margen"],
        "longitud":   est_row["longitud"],
        "latitud":    est_row["latitud"],
        "horario":    est_row["horario"],
        # Convertimos esTerrestre a booleano
        "esTerrestre": bool(est_row["esTerrestre"]),
        
        # Embedded sub-documentos:
        "localidad": {
            "id": est_row["idLocalidad"],
            "nomLocalidad": est_row["nomLocalidad"]
        },
        "municipio": {
            "id": est_row["idMunicipio"],
            "nomMunicipio": est_row["nomMunicipio"]
        },
        "provincia": {
            "id": est_row["idProvincia"],
            "nomProvincia": est_row["nomProvincia"]
        },
        
        # Listado de tarifas
        "tarifas": tarifas_est
    }
    
    estaciones_transformadas.append(estacion_doc)

# Volcado a JSON
with open("estaciones.json", "w", encoding="utf-8") as f:
    json.dump(estaciones_transformadas, f, ensure_ascii=False, indent=4)

# Insertar en Mongo
# (Primero, si procede, vacía la colección)
estaciones_collection.delete_many({})  

if estaciones_transformadas:
    estaciones_collection.insert_many(estaciones_transformadas)
