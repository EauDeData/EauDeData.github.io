import csv
import requests
from bs4 import BeautifulSoup
base_url = 'https://revista.dgt.es'
# Lista de URLs de tests a scrapear (se pueden obtener dinámicamente leyendo la página principal)
test_urls = [
    "https://revista.dgt.es/es/test/Test-num-{}.shtml".format(x) for x in range(220, 400)

]

# Archivo CSV de salida
with open('preguntas_dgt.csv', 'w', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["imagen", "pregunta", "opcion_a",  "opcion_b",  "opcion_c", "respuesta_correcta"])  # encabezados

    for url in test_urls:
        print('Url:', url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text)

        # Cada pregunta suele estar en un <h4> con clase, opciones en <ul>

        preguntas = soup.find_all('article', class_='test')  # Ej. estructura de la revista
        print('Num preguntes:', len(preguntas))
        # (Si cambia el HTML, ajustar selectores según inspección)
        for div in preguntas:
            # Extraer texto de la pregunta
            pregunta = div.find('h4', class_='tit_not').get_text(strip=True)
            imurl = base_url + div.find('figure').find('img')['src']

            # Extraer opciones A, B, C
            opciones = [li.get_text(strip=True) for li in div.find_all('li')]
            # Extraer respuesta correcta
            respuesta = div.find('div', class_='content_respuesta').find('p')
            respuesta_text = respuesta.get_text(strip=True).replace('Respuesta correcta', '').strip()

            writer.writerow([imurl, pregunta] + opciones + [respuesta_text])
