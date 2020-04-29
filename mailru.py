from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime

months = {'Янв': '01',
     'Фев': '02',
     'Мар': '03',
     'Апр': '04',
     'Май': '05',
     'Июн': '06',
     'Июл': '07',
     'Авг': '08',
     'Сен': '09',
     'Окт': '10',
     'Ноя': '11',
     'Дек': '12'}


def mail_parse(driver):
    item = {}
    item['sender'] = driver.find_element_by_tag_name('strong').text
    dt = driver.find_element_by_class_name('readmsg__mail-date').text.split()[1:]
    dt[1] = months[dt[1]]
    item['mdate']  = (datetime.strptime('-'.join(dt), '%d-%m-%Y-%H:%M'))
    item['subject'] = driver.find_element_by_class_name('readmsg__theme').text
    mytext = driver.find_element_by_xpath("//div[@id='readmsg__body']").text
    item['text'] = mytext
    return item

qty = int(input('Введите количество писем которое надо скачать:  '))

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://m.mail.ru/login')
assert "Вход — Почта Mail.Ru" in driver.title

elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')
elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')

elem.send_keys(Keys.RETURN)

mail = driver.find_element_by_class_name('messageline__link')

n=1
letters = []

while n <= qty:
    driver.get(mail.get_attribute('href'))
    links = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@class='readmsg__text-link']"))) # использую Xpath
    # а не CLASS_NAME - потому что в Xpath можно строго по полному перечню классов в а не по вхождению как в CLASS_NAME
    letter = mail_parse(driver)
    letters.append(letter)
    mail = links[-1]
    if mail.text != 'Следующее':
        print(f'Всего имеетcя {n} писем')
        break
    n += 1

pprint (letters)
client = MongoClient('localhost', 27017)
db = client['selenium']
collection = db.mailru
collection.insert_many(letters)