import google.generativeai as genai
import Pyro4

genai.configure(api_key="")
modelo = genai.GenerativeModel('gemini-2.0-flash')

def servidor2(respuesta_texto, respuesta_barrio):
    try:
        client = Pyro4.Proxy("PYRO:GeminiClient2@100.89.141.78:9091")
        print("Conectado exitosamente")
        resultado = client.lista_productos(respuesta_texto, respuesta_barrio)
        return resultado
    except Pyro4.errors.CommunicationError as e:
        print(f"Error al conectar : {e}")
        return f"Error de conexión: No se pudo contactar al servidor de recetas."

@Pyro4.expose
class GeminiClient:
    def consulta(self, input_text, input_barrio):
        print(f"Recibida consulta: '{input_text}'")
        
        respuesta = modelo.generate_content(f"Necesito que me des la lista de ingredientes y la receta breve de {input_text}")
        respuesta_texto = respuesta.text
        return servidor2(respuesta_texto, input_barrio)

daemon = Pyro4.Daemon(host="0.0.0.0", port=9090)
uri = daemon.register(GeminiClient, objectId="GeminiClient")

print("Servidor Pyro4 iniciado correctamente")
print("Escuchando en: 0.0.0.0:9090")
print(f"URI de conexión: {uri}")
print("Servidor listo para recibir consultas")

daemon.requestLoop()
