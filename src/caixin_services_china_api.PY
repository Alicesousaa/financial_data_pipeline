# ======================
# IMPORTA  BIBLIOTECAS
# ======================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

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
   
        driver.get("https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596")
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
            EC.presence_of_element_located((By.ID, "eventHistoryTable596"))
        )

        # Encontra o botão "Ver mais" e clica repetidamente até que não haja mais botões
        while True:
            try:
                btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.newBtn.toggleButton"))
                )
                btn.click()
                # Aguarda os novos dados carregarem
                time.sleep(2)  
            except:
                # Quando não houver mais botão, encerra o loop
                break  

        # Extrai os dados da tabela
        # Ignora cabeçalho e pega apenas as linhas de dados
        rows = driver.find_elements(By.CSS_SELECTOR, "#eventHistoryTable596 tr")[1:]  
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
        df = pd.DataFrame(data)

        # se nao houver dados, avisa
        if df.empty:
            print("Nenhum dado foi coletado.")
        # se houver dados, mostra os dados
        else:
            print("Dado coletado:")
            # Mostra as primeiras linhas
            print(df.head())  

            # Salva o DataFrame como CSV
            output_folder = r"C:\Users\alice\Documents\Projeto_suzano\extracao_dados\data"
            os.makedirs(output_folder, exist_ok=True) 
            output_file = os.path.join(output_folder, 'caixin_services_china_selenium.csv')

            # Salva o DataFrame como CSV codificado em UTF-8 com BOM
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Arquivo salvo em: {output_file}")

    finally:
        driver.quit()


get_caixin_selenium()
