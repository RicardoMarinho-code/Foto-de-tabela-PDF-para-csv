from pdf2image import convert_from_path
import cv2
import pytesseract
import os
import base64
import json
import urllib.request
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ricardo.marinho\Documents\Diretoria\credentials.json"

pdf_archive = 'Imigrante 80000.011156 2024-31 of_2025_053_com_anexo.pdf'

"""
Define a qualidade que vai ser gerada

DPI é a nitidez da foto, já que temos que transformar a página inteira em foto para a leitura da tabela.
A DPI que usarei será 300. Mas também pode ser 100 ou 600, isso depende necessidade.

first_page e last_page definem o intervalo das páginas que usaremos, então
já que temos apenas a segunda página, first_page e last_page=2

"""

pages = convert_from_path(pdf_archive, dpi = 600, first_page=2, last_page=2, poppler_path=r"C:\Poppler\poppler-24.08.0\Library\bin")
page = pages[0]

#salva a foto como "tabela.png"
page.save("tabela.png", "PNG")

img = cv2.imread("tabela.png", 0) #0 significa foto em preto e branco

"""
Renderiza a foto 
isso é uma técnica chamada limiarização (ou treshoding)

cv2.threshold separa os pixels da foto em preto ou branco

150 significa as cores, onde:
pixels menores de 150 serão tratados como preto
pixels maiores ou igual a 150 serão tratados como branco

cv2.THRESH_BINARY: Tipo de limiarização. Nesse modo, a imagem fica binária:
Menor que 150 → 0 (preto).
Maior ou igual a 150 → 255 (branco).

faremos isso porque o OCR trabalha melhor com fotos mais nítidas, então renderizar as fotos
é melhor para o tratamento desses dados
"""
_, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

#salva a foto depois de processada
cv2.imwrite("tabela_thresh.png", thresh)

with open("tabela_thresh.png", "rb") as image_file:
    image_content = base64.b64encode(image_file.read()).decode('utf-8')

api_key = "8335f9f98baeccc75313eec0f23a4fc86415be5b"

# Montar a requisição para a Vision API
url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
request_body = {
    "requests": [
        {
            "image": {
                "content": image_content
            },
            "features": [
                {
                    "type": "DOCUMENT_TEXT_DETECTION"
                }
            ]
        }
    ]
}

# Converter o corpo da requisição para JSON e codificar
request_data = json.dumps(request_body).encode('utf-8')

# Fazer a requisição HTTP
req = urllib.request.Request(url, data=request_data, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode('utf-8'))
        # Extrair o texto
        texto = response_data["responses"][0]["fullTextAnnotation"]["text"] if "fullTextAnnotation" in response_data["responses"][0] else ""
        print("Texto extraído com Google Cloud Vision API:")
        print(texto)
except urllib.error.HTTPError as e:
    print(f"Erro na requisição: {e}")
    print(e.read().decode('utf-8'))

# Inicializar o cliente da Google Cloud Vision
client = vision.ImageAnnotatorClient()

# Carregar a imagem pré-processada
with open("tabela_thresh.png", "rb") as image_file:
    content = image_file.read()

# Criar o objeto de imagem para a API
image = vision.Image(content=content)

# Fazer a requisição de OCR
response = client.document_text_detection(image=image)

# Extrair o texto
texto = response.text_annotations[0].description if response.text_annotations else ""

#transforma a foto em texto
texto = pytesseract.image_to_string(thresh)
print(texto)