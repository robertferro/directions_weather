import streamlit as st
import pandas as pd
import datetime
import duckdb
from extract_directions import calcular_rota
from extract_climate import forecast_climate,current_weather



def retrying_data(table):
    con = duckdb.connect(database='analytics.db') 
    consulta = f"SELECT * FROM DIRECTIONS_WEATHER.{table}"
    resultado = con.execute(consulta)
    df = pd.DataFrame(resultado.fetchdf())
    con.close()
    return df

def insert_data(df,table):
    con = duckdb.connect(database='analytics.db') 
    con.register('dados', df)
    con.execute(f"INSERT INTO DIRECTIONS_WEATHER.{table} SELECT * FROM dados;")
    con.close()


st.title("DIRECTIONS WEATHER")


with open('api_keys/google_api_key.txt', "r") as api_key:
    API_KEY = api_key.read().strip() 


with open('api_keys/weather_api_key.txt', "r") as api_key:
    API_KEY_weather = api_key.read().strip() 

# Barra lateral
st.sidebar.title("Opções")
opcao = st.sidebar.selectbox("Selecione a opção", ["Calculo de Rota", "Previsão do Tempo","Ver Registros"])


#############################
##### CALCULO DE ROTA #######
#############################
if opcao == "Calculo de Rota":
    # Solicitar informações do usuário
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    origem = st.text_input("Origem")
    destino = st.text_input("Destino")
    
    registros = []
    table='DIRECTIONS'
    if st.button("Calcular Rota"):
        calcular_rota(cidade, estado, origem, destino, API_KEY, registros)
        st.success("Rota calculada com sucesso!")

        # Exibir resultados em um DataFrame do Pandas
        if registros:
            df = pd.DataFrame(registros)
            st.subheader("Resultados da Rota")
            st.dataframe(df)
            insert_data(df,table)

        else:
            st.warning("Nenhum registro disponível - Insra uma rota válida")


#############################
##### PREVISAO DO TEMPO #####
#############################
elif opcao=="Previsão do Tempo":
    
    opcao_previsao = st.sidebar.selectbox("Selecione o tipo de previsão", ["Previsão Real time", "Previsão 5 dias"])
    
    if opcao_previsao == "Previsão 5 dias":
        st.success('Previsão 5 dias')
        registros = []
        table='FORECAST_WEATHER'
        cidade = st.text_input("Cidade")
        if st.button("Ver previsão"):
            forecast_climate(cidade,API_KEY_weather,registros)
            st.success("Previsão calculada com sucesso")
            if registros:
                df = pd.DataFrame(registros)
                st.subheader("Previsão do tempo")
                st.dataframe(df)
                insert_data(df,table)
            else:
                st.warning("Nenhum registro disponível - Insira uma cidade válida")
    
    elif opcao_previsao == "Previsão Real time":
        st.success('Previsão Real time')
        registros = []
        table='CURRENT_WEATHER'
        cidade = st.text_input("Cidade")
        if st.button("Ver previsão"):
            data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            current_weather(cidade,API_KEY_weather,registros,data)
            st.success("Previsão calculada com sucesso")
            if registros:
                df = pd.DataFrame(registros)
                st.subheader("Previsão do tempo")
                st.dataframe(df)
                insert_data(df,table)
  
               
            else:
                st.warning("Nenhum registro disponível - Insira uma cidade válida")


#############################
##### CONSULTA AO BANCO #####
#############################
elif opcao=="Ver Registros":

    opcao_visualizacao = st.sidebar.selectbox("Selecione o dado que deseja visualizar ", ["Rotas","Registros de previsão real time","Registros de previsão 5 dias"])
    
    if  opcao_visualizacao == "Rotas":
        table='DIRECTIONS'
        df = retrying_data(table)
        st.dataframe(df)
        
    
    elif opcao_visualizacao == "Registros de previsão real time":
        table='CURRENT_WEATHER'
        df = retrying_data(table)
        st.dataframe(df)
    
    elif opcao_visualizacao == "Registros de previsão 5 dias":

        table='FORECAST_WEATHER'
        df = retrying_data(table)
        st.dataframe(df)