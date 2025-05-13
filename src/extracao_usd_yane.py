# Imporação de bibliotecas necessárias
import requests
import pandas as pd
from datetime import datetime

# Função para obter os dados históricos de USD/CNY
def get_usd_cny_data(api_key, start_date='1991-01-01'):
    # Definindo a data final como o dia atual
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    # Definindo o endpoint da API da Alpha Vantage
    url = f'https://www.alphavantage.co/query'
    
    # Parâmetros da consulta
    params = {
        'function': 'FX_MONTHLY',   # Função de dados mensais
        'from_symbol': 'USD',       # Moeda de origem
        'to_symbol': 'CNY',         # Moeda de destino
        'apikey': api_key,          # Chave da API para autenticação
        'outputsize': 'full'        # Isso retornar o histórico completo
    }

    # Fazendo a solicitação à API
    response = requests.get(url, params=params)
    data = response.json()  # Convertendo a resposta em formato JSON

    # Extraindo e processando os dados
    time_series = data.get('Time Series FX (Monthly)', {})  # Obtendo a série temporal mensal
    
    # Convertendo os dados em um DataFrame
    df = pd.DataFrame(time_series).transpose()  # Transpondo para que as datas sejam as linhas

    # Verificando se a chave '5. volume' existe antes de adicionar a coluna 'volume'
    if '5. volume' in df.columns:
        df = df[['1. open', '2. high', '3. low', '4. close', '5. volume']]  # Selecionando colunas relevantes
    else:
        df = df[['1. open', '2. high', '3. low', '4. close']]               # Sem volume

    # Renomeando as colunas para o formato desejado
    df.columns = ['aberto', 'alto', 'baixo', 'fechar', 'volume'] if '5. volume' in df.columns else ['aberto', 'alto', 'baixo', 'fechar']   # Renomeando as colunas
    
    # Convertendo os índices para datas
    df.index = pd.to_datetime(df.index)        # Convertendo o índice para o tipo datetime
    df = df.reset_index()                      # Resetando o índice para que as datas sejam uma coluna
    df = df.rename(columns={'index': 'data'})  # Renomeando a coluna de índice para 'data'

    # Filtrando os dados para o período desejado
    df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]  # Filtrando entre as datas especificadas

    return df  # Retornando o DataFrame com os dados filtrados


# Chave
api_key = 'ELUGE0PWVIMRDQRK'  # Substitua pela sua chave de API

# Obtendo os dados
usd_cny_data = get_usd_cny_data(api_key)  # Chamando a função 


usd_cny_data.to_csv(r'C:\Users\alice\Documents\Projeto_suzano\extracao_dados\data\usd_cny_data_alpha_vantage.csv', index=False)

 # Salvando os dados em um arquivo CSV
