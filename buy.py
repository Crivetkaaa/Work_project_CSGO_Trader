from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import time
from config import domain

class VARS:
    restart_delay = 1800
    set_count = 99

def load_cookies(driver, filename):
    driver.delete_all_cookies()

    with open(filename, 'rb') as file:
        for cookie in pickle.load(file):
            driver.add_cookie(cookie)
        
    driver.refresh()

options = webdriver.ChromeOptions()
options.headless = True

browser = webdriver.Chrome(
    executable_path='googlewebdriver/chromedriver.exe', options=options)

browser.get(f'https://{domain}/ru/withdraw/csgo_pro')
browser.maximize_window()
browser.delete_all_cookies()

with open('CS_cookies', 'r') as f:
    browser.add_cookie({'name':'PHPSESSID', 'value': f.read(), 'domain':domain})
browser.refresh()

def load_all():
    max_count_elems = 0
    while True:
        mas_prices = browser.find_elements(By.XPATH, '//div[@class = "skins_item_other_requests_list"]//li[2]/span[1]')
        if len(mas_prices) == max_count_elems and len(mas_prices) != 0:
            break

        max_count_elems = len(mas_prices)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    browser.execute_script("window.scrollTo(0, 0);")

    return mas_prices

while True:
    print('start round')
    time.sleep(3)
    
    mas_prices = load_all()

    mas_entry_field = browser.find_elements(By.XPATH, '//div[@class = "skins_item_other_requests_list"]//li[2]/span[1]//ancestor::div[@class = "skins_row_item_unit"]//div[@class = "skins_item_cost"]/input')
    mas_start_button = browser.find_elements(By.XPATH, '//div[@class = "skins_item_other_requests_list"]//li[2]/span[1]//ancestor::div[@class = "skins_row_item_unit"]//div[@class = "skins_item_actions"]/button')
    mas_count_field = browser.find_elements(By.XPATH, '//div[@class = "skins_item_other_requests_list"]//li[2]/span[1]//ancestor::div[@class = "skins_row_item_unit"]//div[@class = "skins_item_counter_row"]/input')
    
    print('Count items:',len(mas_prices))
    for i in range(len(mas_prices)):
        print('Item', i)
        try:
            new_price = int(mas_prices[i].text) + 1
            mas_entry_field[i].clear()
            mas_entry_field[i].send_keys(str(new_price))
            mas_count_field[i].clear()
            mas_count_field[i].send_keys(str(VARS.set_count))
            ActionChains(browser)\
            .click(mas_start_button[i])\
            .perform()

        except Exception as ex:
            print('Error buy', ex)

        try:
            time.sleep(1)
            browser.find_element(By.XPATH, '/html/body/div[35]/div/button').click()
        except: pass

        try:
            browser.find_element(By.XPATH, '//*[@id="saveTradeLing"]').click()
        except: pass

    time.sleep(VARS.restart_delay)

    browser.refresh()
    load_all()

    """
    try:
        browser.find_element(By.XPATH, '//*[@id="stop_all"]').click()
        time.sleep(3)
        browser.find_element(By.XPATH, '/html/body/div[35]/div/button[1]').click()
        time.sleep(1)
        browser.find_element(By.XPATH, '/html/body/div[35]/div/button').click()
    except:
        print("Can't stop all")
    """
    
    mas_stop_button = browser.find_elements(By.XPATH, '//button[@class = "skins_item_button stop stop_item"]')
    
    for i in range(len(mas_stop_button)):
        try:
            ActionChains(browser)\
            .click(mas_stop_button[i])\
            .perform()
        except Exception as ex:
            print('Error stop buying', ex)

        try:
            time.sleep(1)
            browser.find_element(By.XPATH, '/html/body/div[35]/div/button').click()
        except: pass

    time.sleep(3)    
    
    browser.refresh()