from datetime import datetime,timedelta
import pandas as pd
import requests
import json
from sql_functions import insert_data





#  função que calcula as rotas
def calcular_rota(cidade,estado,origem,destino, API_KEY, registros):

    mode_list = ['walking', 'driving', 'bicycling', 'transit']

    for mode in mode_list:

        try:
            url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origem}&mode={mode}&destination={destino}&key={API_KEY}'
            response = requests.get(url)
            result = json.loads(response.text)
            if result['status']=='OK':
                distancia_km = result['routes'][0]['legs'][0]['distance']['text'].split(' km')[0]
                tempo_min = result['routes'][0]['legs'][0]['duration']['text'].split(' mins')[0]
                partida = result['routes'][0]['legs'][0]['start_address']
                chegada = result['routes'][0]['legs'][0]['end_address']
                lat_inicial = result['routes'][0]['legs'][0]['start_location']['lat']
                lng_inicial = result['routes'][0]['legs'][0]['start_location']['lng']
                lat_final = result['routes'][0]['legs'][0]['end_location']['lat']
                lng_final = result['routes'][0]['legs'][0]['end_location']['lng']


                mode_map = {
                            'walking': 'CAMINHANDO',
                            'driving': 'DIRIGINDO',
                            'bicycling': 'PEDALANDO',
                            'transit': 'TRANSPORTE PÚBLICO'
                        }

                registros.append({
                    'CIDADE':cidade,
                    'ESTADO':estado,
                    'ORIGEM': origem,
                    'DESTINO': destino,
                    'DISTANCIA_KM': distancia_km,
                    'MODO': mode_map[mode],
                    'TEMPO_MINUTOS': tempo_min,
                    'LAT_INICIAL': lat_inicial,
                    'LNG_INICIAL': lng_inicial,
                    'LAT_FINAL': lat_final,
                    'LNG_FINAL': lng_final
            })
                     
        except Exception as e:
            print(f"Erro ao calcular rota: {e}")



if __name__ == "__main__":

    print('RECUPERANDO OS DADOS DA API')
    # recuperando a API_KEY do google
    with open('api_keys/google_api_key.txt', "r") as api_key:
        API_KEY = api_key.read().strip() 

    print('RECUPERANDO OS DADOS DE ROTAS')
    # Lendo um dicionario com possíveis rotas
    with open('utils/address.json', "r") as address_json:
        address = json.load(address_json)

    origem_dict = address['origin_dict']
    destino_dict = address['destino_dict']

    registros = []
    for estado, cidades in origem_dict.items():
        for cidade in cidades:
            origem_list = origem_dict[estado][cidade]
            destino_list = destino_dict[estado][cidade]
            for origem, destino in zip(origem_list, destino_list):
                print(f'CALCULANDO ROTA PARA {origem}: {destino}')
                calcular_rota(cidade,estado,origem,destino, API_KEY, registros)

    dados = pd.DataFrame(registros)

    print('CONECTANDO AO BANCO DE DADOS')

    print('INSERINDO OS DADOS')
    table='DIRECTIONS'
    insert_data(dados,table)
