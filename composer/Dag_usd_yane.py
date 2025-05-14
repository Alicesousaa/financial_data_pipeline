# Importações necessárias
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import os
import logging

def get_usd_cny_data(**kwargs):
# Função para obter os dados históricos de USD/CNY

    try:
        # Minha chave da API (uso uma válida e com cota disponível)
        api_key = 'ELUGE0PWVIMRDQRK'
        start_date = '1991-01-01'
        end_date = datetime.today().strftime('%Y-%m-%d')

        # Faço a requisição à API da Alpha Vantage
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'FX_MONTHLY',
            'from_symbol': 'USD',
            'to_symbol': 'CNY',
            'apikey': api_key,
            'outputsize': 'full'
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
                # Filtrando os dados para o período desejado
        df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

        # Defino o caminho de destino no bucket do Composer
        data_hoje = datetime.today().strftime('%Y_%m')
        output_path = f'/home/airflow/gcs/data/usd_cny_{data_hoje}.csv'

        # Certifico que o diretório existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Salvo o CSV no bucket
        df.to_csv(output_path, index=False)
        logging.info(f"Dados salvos com sucesso em {output_path}")

    except Exception as e:
        logging.error(f"Erro ao extrair/salvar os dados: {e}")
        raise


# Parâmetros padrão da DAG
default_args = {
    'owner': 'alice',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definição da DAG
with DAG(
    dag_id='extrair_usd_cny_para_gcs',
    default_args=default_args,
    description='Extrai dados USD/CNY da Alpha Vantage e salva no bucket do Composer (GCS)',
    schedule_interval='@monthly',
    catchup=False,
    tags=['cambio', 'api', 'alpha_vantage', 'composer'],
) as dag:

    # Tarefa única: extrai os dados e salva no GCS automaticamente
    extrair_dados = PythonOperator(
    task_id='extrair_usd_cny',
    python_callable=get_usd_cny_data,
)


    extrair_dados