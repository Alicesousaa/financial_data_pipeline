from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as py
import pandas as pd

import time



chrome_options = Options()
# Adicionar estas opções para contornar erros SSL
chrome_options.add_argument('--headless=new')
# definir navegador
navegador = webdriver.Chrome()
#definindo site
navegador.get('https://br.investing.com/currencies/usd-cny-historical-data') 

select_periodo = navegador.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]')
select_periodo.click()

select_periodo = navegador.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]')
select_periodo.click()
time.sleep(1) 
select_dta = navegador.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]')
select_dta.click()
time.sleep(2)
py.click(x=706, y=875)
time.sleep(2)
py.click(x=676, y=580)
time.sleep(1) 
py.click(x=681, y=641)
time.sleep(1)
py.scroll(11900) 
time.sleep(2)
py.click(x=641, y=655)
time.sleep(2) 
py.click(x=634, y=658)
time.sleep(2) 
py.click(x=697, y=654)

select_dta = navegador.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]')
select_dta.click()


    # Extrair os dados da tabela
tabela = WebDriverWait(navegador, 20).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="common-table medium js-table"]'))
    )
    
    # Converter a tabela para DataFrame
dados = pd.read_html(tabela.get_attribute('outerHTML'))[0]
    
    # Renomear e selecionar colunas
dados.columns = ['Data', 'Último', 'Abertura', 'Máxima', 'Mínima', 'Vol.', 'Var%']
dados_finais = dados[['Data', 'Último', 'Abertura', 'Máxima', 'Mínima', 'Vol.']]
dados_finais.columns = ['data', 'fechar', 'aberto', 'alto', 'baixo', 'volume']
    
    # Salvar em CSV
dados_finais.to_csv('dados_historicos_usd_cny.csv', index=False)
print("Dados salvos com sucesso!")
print(dados_finais.head())

navegador.quit()


