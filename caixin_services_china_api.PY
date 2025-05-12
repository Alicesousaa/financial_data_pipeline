# Importando as bibliotecas necessárias
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By  
from webdriver_manager.chrome import ChromeDriverManager  
import pandas as pd  
import time

# Definindo a função para coletar dados 
def get_caixin_selenium():

    # Configurando as opções do Chrome
    options = webdriver.ChromeOptions()
    # Executa o navegador em segundo plano, sem abrir uma janela visível
    options.add_argument("--headless")  
    
    # Instala o ChromeDriver e cria um serviço para ele
    service = Service(ChromeDriverManager().install())
    
    try:
        # Inicializa o navegador Chrome com as opções e o serviço configurados
        driver = webdriver.Chrome(service=service, options=options)
        
        # Acessa a página do Índice de Serviços Caixin Chinês
        driver.get("https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596")
        
        # aceita cookies, se o botão aparecer
        try:
            # Clica no botão de aceitar cookies
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            # Espera 2 segundos para garantir que a ação foi concluída 
            time.sleep(2) 
        # senão 
        except:
            # Se o botão não aparecer, ignora o erro e continua
            pass 
        
        # Clica no botão "Mostrar mais" até que todos os dados sejam carregados
        # O loop continua até que não haja mais botões "Mostrar mais" para clicar
        while True:
            # Tenta encontrar o botão "Mostrar mais" e clicar nele
            try:
                # Clica no botão "Mostrar mais"
                driver.find_element(By.CSS_SELECTOR, "a.newBtn.toggleButton").click()  
                # Espera 3 segundos para que os dados sejam carregados
                time.sleep(3) 
            # Se não encontrar o botão
            except:
                # Se não houver mais botões para clicar, sai do loop
                break  
        
        # Extrai os dados da tabela
        # Inicializa uma lista para armazenar os dados extraídos
        data = []  
        # Seleciona todas as linhas da tabela, ignorando o cabeçalho
        rows = driver.find_elements(By.CSS_SELECTOR, "#eventHistoryTable596 tr")[1:] 
        
        # Itera sobre cada linha da tabela
        for row in rows:
             # Encontra todas as células (colunas) na linha
            cols = row.find_elements(By.TAG_NAME, "td") 
            # Verifica se há pelo menos 4 colunas para evitar erros de índice
            if len(cols) >= 4:  
                # Adiciona um dicionário com os dados extraídos à lista
                data.append({
                    'data': cols[0].text,          # A primeira coluna contém a data
                    'estado_atual': cols[1].text,  # A segunda coluna contém o estado atual
                    'fechar': cols[3].text,        # A quarta coluna contém o valor de fechamento (anterior)
                    'previsão': cols[2].text       # A terceira coluna contém a previsão
                })
        
        # Cria um DataFrame a partir dos dados extraídos
        df = pd.DataFrame(data)
        # Reorganiza as colunas na ordem desejada
        df = df[['data', 'estado_atual', 'fechar', 'previsão']]  
         # Salva os dados em um arquivo CSV
        file_path = 'caixin_services_china_selenium.csv'
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"Arquivo salvo em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

        return df  
    #finaliza
    finally:
        # Garante que o navegador seja fechado, independentemente de erros
        driver.quit()  
