import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SearchBot():
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.indexer = None
        self.key_pharse = None

    def search_terms(self, quantity_of_pages) -> dict:
        links_filtrados = 0
        links_casa = []
        attemps_to_locator = 0
        cont_loop = 0
        self.driver.get(self.indexer['url_search'])

        try:
            campo_de_busca = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.indexer['search_bar'])))
            campo_de_busca.send_keys(self.key_pharse, Keys.ENTER)
            
            #self.driver.implicitly_wait(5)
            body = self.driver.find_element(By.TAG_NAME, 'body')
            for i in range(7):
                body.send_keys(Keys.END)
                #self.driver.implicitly_wait(1)
                #self.driver.implicitly_wait(3)
            try:
                
                while True:
                    self.driver.implicitly_wait(0.5)
                    body = self.driver.find_element(By.TAG_NAME, 'body')
                    for i in range(7):
                        body.send_keys(Keys.END)
                    
                    #self.driver.implicitly_wait(0.3)
                    
                    #time.sleep(0.8)
                    #mais_detalhes = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.indexer['xpath_more'])))
                    
                    if quantity_of_pages != None:
                        if cont_loop == quantity_of_pages:
                            break
                    try:
                        mais_detalhes = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.indexer['xpath_more'])))
                        #botao_mostrar_mais = mais_detalhes.find_element(By.XPATH, f".//*[contains(text(), '{self.indexer['value_more']}')]")
                        mais_detalhes.click()
                    except:
                        if attemps_to_locator< 30:
                            if self.indexer['captcher'] != None:
                                try:
                                    captcher = self.driver.find_element(By.XPATH, self.indexer['captcher']['xpath_catcher'])
                                    print("Captcher de segurança encontrado, o script encerrará as buscas!")
                                    break
                                except:
                                    # sem captcher
                                    pass
                                # body = self.driver.find_element(By.TAG_NAME, 'body')
                                # for i in range(7):
                                #     body.send_keys(Keys.END)
                            attemps_to_locator = attemps_to_locator +1
                        else:
                            break
                    cont_loop = cont_loop + 1

            except Exception as error_ocurred:
                print(error_ocurred)

        finally:
            # Encontrar os elementos de resultado de pesquisa (links)
            elementos_links = self.driver.find_elements(By.TAG_NAME, "a")
            links_filtrados = len(elementos_links)

            # Iterar sobre os links encontrados
            for elemento in elementos_links:
                # Obter o URL do link
                url = elemento.get_attribute('href')
                
                # Verificar se o URL contém o termo pesquisado usando expressão regular
                if url != None:
                    if re.search(r'/home/game\?gameCategoryId=0', url):
                        # Se sim, adicionar à lista de links
                        try:
                            index_element = links_casa.index(url)
                            #print("Link Descartado! - Link duplicado!")
                        except:
                            links_casa.append(url)
                            #print("---------------------------- Link encontrado!")
                    else:
                        print("Link Descartado!")
        return {"filtered_links": links_filtrados, "home_links": links_casa}
    
    def set_indexer(self, indexer) -> None:
        self.indexer = indexer

    def set_key_pharse(self, key_pharse) -> None:
        self.key_pharse = key_pharse

    def browser_quit(self) -> None:
        self.driver.close()