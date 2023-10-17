# DIRECTIONS_WEATHER OVERVIEW

Este projeto tem como objetivo extrair informações referentes a clima e trânsito usando as seguintes APIs:
 
 - https://openweathermap.org/api
 - https://developers.google.com/maps/documentation/directions/overview

1. Coleta e tratamento dos dados:
 - foi realizada por meio das APIs citadas anteriormente usando python

2. Modelagem de Dados:
 - foram criadas 3 tabelas definidas no script *init.sql* sendo elas: 
    - DIRECTIONS: armazena os daos dos cálculos de rotas
    - FORECAST_WEATHER: armazena dados referentes a previsão do tempo para uma cidade a cada 3 horas para os próximos 5 dias
    - CURRENT_WEATHER: armazena dados referentes a previsão do tempo para uma cidade no momento da busca

3. Execução
 - é necessário clonar o repositório todo o projeto será excutado por meio do arquivo run.sh, por meio de um terminal com os seguintes comandos: **chmod +x run.sh**  e ./run.sh

4. Visualização:
    Os dados já extraídos das APIs e armazenados no banco de dados, podem ser recuperados utilizando uma interface desenvolvida usando o framework streamlit.
 
5. Próximos passos:
 - visando implementar um esquema de ETL mais robusto, poderá ser utilizado apache airflow orquestração de tarefas, bem como um banco de dados como MySQL ou POstgres apra armazenamento de um volume maior de dados.