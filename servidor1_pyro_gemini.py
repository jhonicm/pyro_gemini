import google.generativeai as genai
import Pyro4
import datetime

genai.configure(api_key="AIzaSyCsrBqrDdsYCInT9TXFm80Z1Mu2sI0Ki5E")
modelo = genai.GenerativeModel('gemini-2.0-flash')

def servidor2(respuesta_texto, respuesta_barrio):
    try:
        client = Pyro4.Proxy("PYRO:GeminiClient2@100.89.141.78:9091")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Conectado exitosamente a 172.17.44.32:9091")
        resultado = client.lista_productos(respuesta_texto, respuesta_barrio)
        
        print(f"[{current_time}] Respuesta recibida del servidor 172.17.44.32:9091")
        return resultado
    except Pyro4.errors.CommunicationError as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Error al conectar con 172.17.44.32:9091: {e}")
        return f"Error de conexión: No se pudo contactar al servidor de recetas."

@Pyro4.expose
class GeminiClient:
    def consulta(self, input_text, input_barrio):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Recibida consulta: '{input_text}'")
        
        respuesta = modelo.generate_content(f"Necesito que me des la lista de ingredientes y la receta breve de {input_text}")
        respuesta_texto = respuesta.text
        return servidor2(respuesta_texto, input_barrio)

daemon = Pyro4.Daemon(host="0.0.0.0", port=9090)
uri = daemon.register(GeminiClient, objectId="GeminiClient")

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"[{current_time}] Servidor Pyro4 iniciado correctamente")
print(f"[{current_time}] Escuchando en: 0.0.0.0:9090")
print(f"[{current_time}] URI de conexión: {uri}")
print(f"[{current_time}] Servidor listo para recibir consultas")

daemon.requestLoop()