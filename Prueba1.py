import csv
import requests

API_KEY = '7ffd42e227834a98a88f30d229187111'  # Reemplazar con la clave del API de ipgeolocation

def obtener_pais_por_ip(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    pais = datos.get("country_name", "Desconocido")
    return pais

def buscar_ips_en_archivo(archivo):
    filas_nuevas = []
    with open(archivo, 'r') as csv_file:
        lector = csv.reader(csv_file)
        encabezados = next(lector)  # Leer los encabezados del CSV
        encabezados.append("Ubicación")  # Agregar encabezado para la nueva columna
        filas_nuevas.append(encabezados)  # Agregar los encabezados a la lista de filas nuevas

        for fila in lector:
            nueva_fila = fila.copy()  # Copiar la fila existente
            direccion_ip = obtener_direccion_ip(fila)
            if direccion_ip:
                pais = obtener_pais_por_ip(direccion_ip)
                nueva_fila.append(pais)  # Agregar el país a la nueva fila
            else:
                nueva_fila.append("")  # Si no se encuentra una dirección IP, dejar el campo de ubicación vacío
            filas_nuevas.append(nueva_fila)  # Agregar la nueva fila a la lista de filas nuevas

    with open(archivo, 'w', newline='') as csv_file:
        escritor = csv.writer(csv_file)
        escritor.writerows(filas_nuevas)

def obtener_direccion_ip(fila):
    import re
    patron = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    for elemento in fila:
        coincidencias = re.findall(patron, elemento)
        if coincidencias:
            return coincidencias[0]
    return None

ruta_archivo_csv = input("Introduce la ruta al archivo CSV: ")

buscar_ips_en_archivo(ruta_archivo_csv)


