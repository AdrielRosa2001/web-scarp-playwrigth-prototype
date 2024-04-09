import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules_search_bot.modules import SearchBot
import time

key_pharse = "inurl:/home/game?gameCategoryId=0"
indexers = [
    {
        "indexer": "google",
        "url_search": 'https://www.google.com.br',
        "search_bar": '//*[@id="APjFqb"]',
        "xpath_more": '//*[@id="botstuff"]/div/div[4]/div[4]/a[1]',
        "value_more": 'Mais resultados',
        "captcher": None
    },
    {
        "indexer": "yandex",
        "url_search": 'https://yandex.com/',
        "search_bar": '//*[@id="text"]',
        "xpath_more": '// *[ @aria-label = "Next page"]',
        "value_more": 'next',
        "captcher": {
            "xpath_catcher": '// *[ @aria-describedby = "checkbox-description"]'
        }
    }
]

# indexers = [
#     indexers_old[0]
# ]

links_casa = []
links_filtrados = 0

search_bot = SearchBot()
search_bot.set_key_pharse(key_pharse)

for i in indexers:
    search_bot.set_indexer(i)
    data_return = search_bot.search_terms(quantity_of_pages=None)
    if data_return['filtered_links'] != 0:
        if data_return['home_links'] != 0:
            for i in data_return['home_links']:
                try:
                    index_link = links_casa.index(i)
                    print("Link Descartado! - Link duplicado!")
                except:
                    links_casa.append(i)
                    print("---------------------------- Link encontrado!")
        else:
            print("Nenhum link de casa encontrado!")
        links_filtrados = links_filtrados + data_return['filtered_links']
    else:
        print("Nenhum link filtrado")

search_bot.browser_quit()
    



if len(links_casa) > 0:
    arquivo = open("finded_links.txt", "w")
    for links in links_casa:
        arquivo.writelines(links+"\n")
    arquivo.close()

print(f"------------------------------\nLinks encontrados: {links_filtrados}\nLinks filtrados: {len(links_casa)}\n------------------------------")


