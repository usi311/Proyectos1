# jokes/services.py
import requests

def obtener_chistes_jokeapi():
    url_jokeapi = 'https://v2.jokeapi.dev/joke/Any'
    respuesta = requests.get(url_jokeapi)
    if respuesta.status_code == 200:
        chiste = respuesta.json()
        if 'joke' in chiste:
            return chiste['joke'], chiste['category'], chiste['type']
        elif 'setup' in chiste and 'delivery' in chiste:
            return f"{chiste['setup']} {chiste['delivery']}", chiste['category'], chiste['type']
    return 'No se pudo obtener un chiste en este momento', None, None

