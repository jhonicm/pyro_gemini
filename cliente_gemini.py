import Pyro4
import base64

client = Pyro4.Proxy("PYRO:GeminiClient@192.168.100.66:9090")

input_text = input("Escribe el platillo: ")
input_barrio = input("Escribe el sector donde vives: ")

respuesta = client.consulta(input_text, input_barrio)

if respuesta and 'data' in respuesta:
    try:
        respuesta_decoded = base64.b64decode(respuesta['data'])
        with open("respuesta.pdf", "wb") as f:
            f.write(respuesta_decoded)
        print("El archivo 'respuesta.pdf' ha sido recibido y guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
else:
    print("No se recibió el archivo.")
