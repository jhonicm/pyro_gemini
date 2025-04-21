import Pyro4
import base64

client = Pyro4.Proxy("PYRO:GeminiClient@192.168.100.66:9090")
input_text = input("Escribe el platillo: ")
input_barrio = input("Escribe el sector donde vives: ")
respuesta = client.consulta(input_text, input_barrio)
# Crear un archivo.pdf con la respuesta Crear un archivo.pdf con la respuesta
respuesta_decoded = base64.b64decode(respuesta['data'])
with open("respuesta.pdf", "wb") as f:
    f.write(respuesta_decoded)
