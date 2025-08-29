import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
import os
from openai import OpenAI
from datosapp import ContadorCalorias
import re


class ClasePrincipal:
    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.texto_imagen = None
        self.resultado_final = None
        self.calorias = None

    def obtener_texto_imagen(self):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cpu")

        if self.ruta_imagen.startswith('http'):
            raw_image = Image.open(requests.get(self.ruta_imagen, stream=True).raw).convert('RGB')
        else:
            raw_image = Image.open(self.ruta_imagen).convert('RGB')

        # Caption incondicional
        inputs = processor(raw_image, return_tensors="pt").to("cpu")
        out = model.generate(**inputs, max_new_tokens=1000)  # Limita a 20 tokens
        self.resultado_final = processor.decode(out[0], skip_special_tokens=True)



    def obtener_resultado_final(self):
      
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key="HF_TOKEN"
        )

        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.1:fireworks-ai",
            messages=[
                {
                    "role": "user",
                    "content": "¿Cuántas calorías tiene una receta de " + self.resultado_final + "?" + " Responde solo con el número de calorías y en Castellano."
                }
            ],
        )

        self.calorias = completion.choices[0].message.content
        match = re.search(r"</think>\s*(\d+)", str(self.calorias))
        ContadorCalorias.agregar_calorias_consumidas(int(match.group(1)))

        


    def mostrar_resultados(self):
            print("Texto imagen:", self.resultado_final)
            print("Resultado final:", self.calorias)