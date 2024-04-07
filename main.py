import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

key_pharse = "inurl:/home/game?gameCategoryId=0"
links_casa = []

driver = webdriver.Chrome()

driver.get("https://www.google.com.br")

try:
    campo_de_busca = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]')))
    campo_de_busca.send_keys(key_pharse, Keys.ENTER)
    
    driver.implicitly_wait(5)
    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(5):
        body.send_keys(Keys.END)
        time.sleep(1)
    driver.implicitly_wait(3)
    try:
        while True:
            body.send_keys(Keys.END)
            mais_detalhes = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="botstuff"]/div/div[4]/div[4]/a[1]')))
            mais_detalhes.click()
    except:
        pass

finally:
    # Encontrar os elementos de resultado de pesquisa (links)
    elementos_links = driver.find_elements(By.TAG_NAME, "a")

    # Iterar sobre os links encontrados
    for elemento in elementos_links:
        # Obter o URL do link
        url = elemento.get_attribute('href')
        
        # Verificar se o URL contém o termo pesquisado usando expressão regular
        if url != None:
            if re.search(r'/home/game\?gameCategoryId=0', url):
                # Se sim, adicionar à lista de links
                links_casa.append(url)
                print("------------------Link encontrado!")
            else:
                print("Link Descartado!")
    driver.quit()



if len(links_casa) > 0:
    arquivo = open("finded_links.txt", "w")
    for links in links_casa:
        arquivo.writelines(links+"\n")
    arquivo.close()
