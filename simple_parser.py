from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
import time
from fake_useragent import UserAgent
import json
import re

start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument(f'--user-agent={UserAgent.random}')
options.page_load_strategy = 'eager'
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options)

list_dict = []

for count in range (1, 10):
    url = f'https://www.avito.ru/novosibirsk/odezhda_obuv_aksessuary?p={count}'
    driver.get(url=url)
    html = BeautifulSoup (driver.page_source, 'lxml')
    list_article = [i for i in html.find_all('h3', class_='styles-module-root-TWVKW')]
    list_article_text = [i.text for i in list_article]
    list_div = [i for i in html.find_all('div', class_='iva-item-title-py3i_')]
    list_div_link = [i.find('a')['href'] for i in list_div]
    list_price = [re.sub(r'\D', '', i.text) for i in html.find_all('strong', class_='styles-module-root-LIAav')]
    for name, link, price in zip(list_article_text, list_div_link, list_price):
        list_dict.append({
            'Наименование' : name,
            'Ссылка' : 'https://www.avito.ru' + link,
            'Цена' : price
        })

driver.quit()
with open ('test.json', 'w', encoding='utf-8') as js:
    json.dump(list_dict, js, ensure_ascii=False, indent=4)


print (time.time() - start)





