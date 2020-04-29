from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
import json

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.get('https://www.mvideo.ru/')
assert "М.Видео - " in driver.title

hits =[]
while hits == []: # пришлось сделать еще один цикл внешний, потому что при всплывающем окне теряется фокус по сетам
    elems = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='gallery-layout']")))
    for elem in elems:
        if elem.find_element_by_class_name('h2').text == 'Хиты продаж':
            while True:
                try:
                    button = elem.find_element_by_class_name('sel-hits-button-next')
                    button.click()
                except:
                    try:
                        owindow = driver.find_element_by_class_name('tooltipster-close')
                        owindow.click()
                        break
                    except:
                        #pass
                        button = elem.find_element_by_class_name('sel-hits-button-next')
                        button.click()
                try:
                    elem.find_element_by_xpath("//a[@class='next-btn sel-hits-button-next disabled']")
                    break
                except:
                    pass
            items = elem.find_elements_by_class_name('sel-product-tile-title')
            for item in items:
                hit = item.find_element_by_xpath("//a[@data-product-info]").get_attribute('data-product-info')
                jhit = json.loads(hit)
                hits.append(jhit)
pprint(hits)
client = MongoClient('localhost', 27017)
db = client['selenium']
collection = db.mvideo
collection.insert_many(hits)
