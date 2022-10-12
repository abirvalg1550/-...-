from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_flats_urls():
    """Функция парсит основный сайт циана и собирает url-ссылки на квартиры"""
    # Запуск Selenium
    try:
        driver = webdriver.Chrome(
            executable_path='/-...-/chromedriver')  # ссылка на драйвер для Chrome
    except Exception as ex:
        print(ex)
    else:
        # Постраничный парсинг
        for page_number in range(1, 55):
            url = 'https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=' + \
                  f'{page_number}&region=2'
            driver.get(url=url)
            # Запись html в файл
            # with open(f'index{page_number}.html', 'w') as file:
            #     file.write(driver.page_source)
            i = 0
            try:
                # driver.find_element(By.CLASS_NAME, '_93444fe79c--moreSuggestionsButtonContainer--h0z5t')# .click()
                # Поиск и попытка нажать на кнопку "Показать еще":
                while driver.find_element(By.XPATH, '//*[@id="frontend-serp"]/div/div[5]/div[2]/a'):
                    i += 1
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="frontend-serp"]/div/div[5]/div[2]/a'))).click()
                    if i > 100:
                        break
                print('Clicked!!!!!')
            except Exception as ex:
                print('Can\'t click')
            finally:
                soup = BeautifulSoup(driver.page_source, 'lxml')
                # Поиск всех url-ссылок на квартиры на сайте:
                flats = soup.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
            with open('flats_urls1.txt', 'a') as file:
                for flat in flats:
                    file.write(flat.find('a').get('href') + '\n')
        driver.close()
        driver.quit()


def main():
    get_flats_urls()


if __name__ == '__main__':
    main()
