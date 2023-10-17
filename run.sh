#!/bin/bash

# Instala os requisitos a partir do arquivo requirements.txt
echo "Instalando os requisitos..."
pip install -r requirements.txt

# Verifica se o arquivo analytics.db existe no diretório
echo "Verificando se o arquivo analytics.db já existe"
if [ -f "analytics.db" ]; then
  echo "O arquivo analytics.db já existe."
  streamlit run main.py
else
  echo "O arquivo analytics.db não existe. Criando o banco de dados..."
  python create_database.py
  echo "Banco de dados criado com sucesso."
  
  echo "Extraindo dados climáticos..."
  python extract_climate.py
  echo "Dados climáticos extraídos e inseridos no banco com sucesso."
  
  echo "Extraindo direções..."
  python extract_directions.py
  echo "Direções extraídas e inseridas no banco com sucesso."
  
  echo "Iniciando a aplicação Streamlit..."
  streamlit run main.py
fi
