from datetime import datetime,timedelta
import pandas as pd
import requests
import json
import duckdb
from sql_functions import insert_data


def current_weather(cidade,API_KEY_weather,registros,data):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&APPID={API_KEY_weather}'
    weather_data = requests.get(url)

    current_weather = weather_data.json()

    city = current_weather['name']
    lat = current_weather['coord']['lat']
    lng = current_weather['coord']['lon']
    tempo = current_weather['weather'][0]['description']
    temperatura = current_weather['main']['temp']
    sensacao = current_weather['main']['feels_like']
    temperatura_min = current_weather['main']['temp_min']
    temperatura_max = current_weather['main']['temp_max']
    umidade = current_weather['main']['humidity']


    if "rain" in tempo:
        precipitacao_1h = current_weather['rain']['1h']
        try:
            precipitacao_3h = current_weather['rain']['3h']
        except:
            precipitacao_3h = ' '
    else:
        precipitacao_1h = ' '
        precipitacao_3h = ' '


    registros.append( {
                        'DATA':data,
                        'CIDADE':city,
                        'TEMPO': tempo,
                        'TEMPERATURA': temperatura,
                        'SENSACAO_TERMICA': sensacao,
                        'TEMPERATURA_MINIMA': temperatura_min,
                        'TEMPERATURA_MAXIMA': temperatura_max,
                        'UMIDADE': umidade,
                        'PRECIPITACAO_1H': precipitacao_1h,
                        'PRECIPITACAO_3H': precipitacao_3h,
                        'LAT': lat,
                        'LNG': lng
                }) 

def forecast_climate(city,API_KEY_weather,registros_forecast):
        try:
            print(f'OBTENDO AS PREVISOES PARA {city}')
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY_weather}'
            weather_data = requests.get(url)
            forecast_weather = weather_data.json()



            
            for i in range(len(forecast_weather['list'])):

                if forecast_weather['cod']=='200':
                    data = forecast_weather['list'][i]['dt_txt']
                    cidade = forecast_weather['city']['name']
                    lat = forecast_weather['city']['coord']['lat']
                    lng = forecast_weather['city']['coord']['lat']
                    temperatura = forecast_weather['list'][i]['main']['temp']
                    sensacao = forecast_weather['list'][i]['main']['feels_like']
                    temperatura_min = forecast_weather['list'][i]['main']['temp_min']
                    temperatura_max = forecast_weather['list'][i]['main']['temp_max']
                    umidade = forecast_weather['list'][i]['main']['humidity']
                    tempo = forecast_weather['list'][i]['weather'][0]['description']
                    probabilidade_chuva = forecast_weather['list'][i]['pop']*100 
                    
                    if "rain" in tempo:
                        precipitacao_3h = forecast_weather['list'][i]['rain']['3h']
                    else:
                        precipitacao_3h = ' '


                    registros_forecast.append( {
                                        'DATA': data,
                                        'CIDADE':cidade,
                                        'TEMPO': tempo,
                                        'TEMPERATURA': temperatura,
                                        'SENSACAO_TERMICA': sensacao,
                                        'TEMPERATURA_MINIMA': temperatura_min,
                                        'TEMPERATURA_MAXIMA': temperatura_max,
                                        'UMIDADE': umidade,
                                        'PROBABILIDADE_CHUVA':probabilidade_chuva,
                                        'PRECIPITACAO_3H_MM': precipitacao_3h,
                                        'LAT': lat,
                                        'LNG': lng
                                }) 
        except Exception as e:
            print(f"Erro ao calcular rota: {e}")


if __name__ == "__main__":
    # recuperando a API_KEY do wheather
    with open('api_keys/weather_api_key.txt', "r") as api_key:
        API_KEY_weather = api_key.read().strip() 

    with open('utils/cities.json', "r") as cities_json:
        cities = json.load(cities_json)

    registros_forecast=[]
    for city in cities['cities']:
        forecast_climate(city,API_KEY_weather,registros_forecast)

    dados = pd.DataFrame(registros_forecast)

    print('CONECTANDO AO BANCO DE DADOS')

    print('INSERINDO OS DADOS')
    table='FORECAST_WEATHER'
    insert_data(dados,table)
