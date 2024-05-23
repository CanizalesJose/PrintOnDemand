# Esta aplicación es una simple prueba para comprobar el funcionamiento del recurso rest
import requests

# Hacer una solicitud GET al recurso en tu primera aplicación Flask
response = requests.get('http://localhost:5000/rest/orders')

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Extraer los datos de la respuesta (en formato JSON)
    data = response.json()
    print("Datos recibidos:", data)
else:
    print("Error al hacer la solicitud:", response.status_code)