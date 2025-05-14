from airflow import DAG
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import time
import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# FUNÇÃO PRINCIPAL

def get_caixin_selenium():


    #  CONFIGURA  NAVEGADOR CHROME
    options = webdriver.ChromeOptions()
    # Executa em modo invisível (novo headless mais estável)
    options.add_argument("--headless=new")  
    # Evita restrições em ambientes protegidos
    options.add_argument("--no-sandbox")      
    # Evita erros de memória compartilhada em containers    
    options.add_argument("--disable-dev-shm-usage") 
    # Cria o serviço do navegador com driver atualizado automaticamente
    service = Service(ChromeDriverManager().install())
    # Inicializa o navegador com as opções configuradas
    driver = webdriver.Chrome(service=service, options=options)

    try:
   
        driver.get("https://br.investing.com/economic-calendar/indian-interest-rate-decision-597")
        time.sleep(3)  # Aguarda o carregamento da página

        # ACEITA OS COOKIES, SE NECESSÁRIO
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            time.sleep(1)
        except:
             # Se o botão não aparecer, ignora
            pass 
        # Aguarda o carregamento da tabela de eventos
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "eventHistoryTable597"))
        )

        # Encontra o botão "Ver mais" e clica repetidamente até que não haja mais botões
        while True:
            try:
                btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.ID, "showMoreHistory597"))
                )
                btn.click()
                # Aguarda os novos dados carregarem
                time.sleep(3)  
            except:
                # Quando não houver mais botão, encerra o loop
                break  

        # Extrai os dados da tabela
        # Ignora cabeçalho e pega apenas as linhas de dados
        rows = driver.find_elements(By.CSS_SELECTOR, "#eventHistoryTable597 tr")[1:]  
        data = []
        # Itera sobre as linhas e extrai os dados
        for row in rows:
            # Encontra todas as colunas da linha
            cols = row.find_elements(By.TAG_NAME, "td")
            # Verifica se a linha tem 4 ou mais colunas
            if len(cols) >= 4:
                data.append({
                    'data': cols[0].text,           # Data
                    'estado_atual': cols[1].text,   # Valor atual
                    'fechar': cols[3].text,         # Valor anterior
                    'previsão': cols[2].text        # Previsão
                })

        # Converte a lista de dicionários em um DataFrame
               # Converte a lista de dicionários em um DataFrame
        df = pd.DataFrame(data)

        if df.empty:
            print("Nenhum dado foi coletado.")
        else:
            print("Dado coletado:")
            print(df.head())

        # Converte a coluna de data para datetime
        df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

        # Filtra apenas os dados a partir de 2012
        df = df[df['data'].dt.year >= 2012]

        # Salva o DataFrame em CSV
        output_folder = '/home/airflow/gcs/data'
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'india.csv')
        df.to_csv(output_file, index=False)




          
    finally:
        driver.quit()


# Default args da DAG
default_args = {
    'owner': 'alice',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='extrair_caixin_para_gcs',
    default_args=default_args,
    description='Extrai dados',
    schedule_interval='@monthly',
    catchup=False,
    tags=['juros', 'india', 'selenium', 'composer'],
) as dag:

    extrair_dados_india = PythonOperator(
        task_id='extrair_caixin_selenium',
        python_callable=get_caixin_selenium,
    )

    upload_para_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_india_para_gcs',
        src='/home/airflow/gcs/data/india.csv',
        dst='juros/india.csv',
        bucket='us-central1-raspagem-suzano-bucket',
    )

    extrair_dados_india >> upload_para_gcs

