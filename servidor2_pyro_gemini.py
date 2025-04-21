import google.generativeai as genai
import Pyro4

genai.configure(api_key="")
modelo = genai.GenerativeModel('gemini-2.0-flash')

def servidor3(respuesta):
    try:
        client = Pyro4.Proxy("PYRO:GeminiClient3@100.70.161.85:9092")
        print("Conectado exitosamente")
        return client.informe(respuesta)
        
    except Pyro4.errors.CommunicationError as e:
        print(f"Error al conectar : {e}")
        return f"Error de conexión: No se pudo contactar al servidor de recetas."

@Pyro4.expose
class GeminiClient2:
    def lista_productos(self, respuesta, barrio):
        respuesta2 = modelo.generate_content(f"Necesito que con la lista de ingredientes de la siguiete receta, busques los mejores lugares para comprar cada producto en {barrio} Ecuador, debes especificar especificamente el nombre de los lugares: {respuesta}")
    
        respuesta_l=servidor3(respuesta+"\n"+respuesta2.text)
        #print(respuesta2.text)
        print(type(respuesta_l))    
        return respuesta_l
daemon = Pyro4.Daemon(host="0.0.0.0", port=9091)
uri= daemon.register(GeminiClient2,objectId="GeminiClient2")
daemon.requestLoop()
