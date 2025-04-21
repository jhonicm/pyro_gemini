import google.generativeai as genai
import Pyro4
import os
import json
from fpdf import FPDF

genai.configure(api_key="")
modelo = genai.GenerativeModel('gemini-2.0-flash')
ruta_completa = ""

def crear_pdf(datos_json):
    global ruta_completa

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, datos_json['Titulo'], ln=True, align='C')
            self.ln(10)

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, title, ln=True, align='L')
            self.ln(5)

        def chapter_body(self, items, numbered=False):
            self.set_font('Arial', '', 12)
            for idx, item in enumerate(items, start=1):
                if numbered:
                    self.multi_cell(0, 8, f"{idx}. {item}", align='L')
                else:
                    self.multi_cell(0, 8, f"- {item}", align='L')  
            self.ln(5)

        def lugares_compra(self, lugares_dict):
            self.set_font('Arial', '', 12)
            for producto, lugar in lugares_dict.items():
                self.multi_cell(0, 8, f"- {producto}: {lugar}", align='L') 
            self.ln(5)

    
    pdf = PDF()
    pdf.add_page()

    
    pdf.chapter_title("Ingredientes:")
    pdf.chapter_body(datos_json['Ingredientes'])

    pdf.chapter_title("Lugares de Compra:")
    pdf.lugares_compra(datos_json['Lugares de compra'])

    pdf.chapter_title("Preparación:")
    pdf.chapter_body(datos_json['preparacion'], numbered=True)

    filename = "Encebollado_Ecuatoriano.pdf"

    
    pdf.output(filename)
    ruta_completa = os.path.abspath(filename)
    print(f"✅ PDF guardado en:\n{ruta_completa}")

        
def obtener_bytes():
    try:
        with open(ruta_completa,"rb") as a:
            data = a.read()
        return data
    except FileNotFoundError:
        print("Ruta no encontrada")

@Pyro4.expose
class GeminiClient3:
    def informe(self, respuesta):
        respuesta = modelo.generate_content(
            f"Necesito que con toda la informacion me crees un informe en JSON puro (sin texto adicional) con la siguiente estructura: {{'Titulo': str, 'Ingredientes': list, 'Lugares de compra': dict, 'preparacion': list}}. Del siguiente texto: {respuesta}"
        )

    
        try:
            start = respuesta.text.find('{')
            end = respuesta.text.rfind('}') + 1
            json_clean = respuesta.text[start:end]

            informe_dict = json.loads(json_clean)
            print("✅ JSON válido recibido y convertido a objeto Python.")
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"⚠️ Otro error inesperado: {e}")
            return None
        crear_pdf(informe_dict)
        informe_pla = obtener_bytes()
        return informe_pla

daemon = Pyro4.Daemon(host="0.0.0.0", port=9092)
uri= daemon.register(GeminiClient3,objectId="GeminiClient3")
daemon.requestLoop()
