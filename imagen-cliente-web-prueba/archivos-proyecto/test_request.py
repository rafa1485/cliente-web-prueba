import requests

url_servicio_mezcla_optima = 'http://localhost:8000/problema_mezcla'
data = '{"valor1":"1", "valor2":"2"}'

respuesta = requests.post(url_servicio_mezcla_optima, json=data)
print('La respuesta del servicio de Mezcla Óptima fue:')
print(respuesta)
