from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pickle
from threading import Thread
from queue import Queue
from config import domain


class GLO:
    url_que = Queue()
    time_last_reload = time.time()

    steps_accept_trade = [
        # online shop
        '/html/body/div[46]/div/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/div[{0}]/div[3]/div[2]/button', #принять трейд
        '/html/body/div[49]/div[2]/button[1]', #ок в сплывающем окне
    ]



def load_cookies(driver, filename):
    driver.delete_all_cookies()

    with open(filename, 'rb') as file:
        for cookie in pickle.load(file):
            driver.add_cookie(cookie)
        
    driver.refresh()

def steam_trade():
    opts = webdriver.ChromeOptions()
    opts.add_argument("lang=en-US")

    browser_Steam = webdriver.Chrome(
        options=opts,
        executable_path='googlewebdriver\chromedriver.exe',
    )

    browser_Steam.get('https://steamcommunity.com/')
    load_cookies(browser_Steam, "steam_cookies")

    while True:
        link, name = GLO.url_que.get()
        browser_Steam.get(link)
        try:
            browser_Steam.execute_script("ShowMenu( 'appselect', GetOptionsDivForActiveUser(), 'left' );")
            time.sleep(2)

            # cs javascript:TradePageSelectInventory( UserYou, 730, "2" );
            # dota javascript:TradePageSelectInventory( UserYou, 570, "2" );

            browser_Steam.execute_script('javascript:TradePageSelectInventory( UserYou, 730, "2" );')
            ele = WebDriverWait(browser_Steam, timeout=1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="filter_control"]'))
            )
            ele.send_keys(name)
            time.sleep(2)

            eles = browser_Steam.find_elements(By.CLASS_NAME, 'itemHolder')
            for ele in eles:
                print(ele.get_attribute("style"))
                if ele.get_attribute("style") != 'display: none;':
                    actionChains = ActionChains(browser_Steam)
                    actionChains.double_click(ele).perform()
                    break
            
            browser_Steam.execute_script('ToggleReady( true );')
            ele = WebDriverWait(browser_Steam, timeout=1).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div[1]/span'))
            )       
            ele.click()
            
            time.sleep(2)
            browser_Steam.execute_script('ConfirmTradeOffer();')
            
        except Exception as ex:
            print("Error trade ====================================\n",ex)


Thread(target=steam_trade).start()

browser_CS = webdriver.Chrome(
    executable_path='googlewebdriver\chromedriver.exe')

browser_CS.get(f'https://{domain}/ru/deposit/csgo')
browser_CS.maximize_window()
browser_CS.delete_all_cookies()

with open('CS_cookies', 'r') as f:
    browser_CS.add_cookie({'name':'PHPSESSID', 'value': f.read(), 'domain':domain})
browser_CS.refresh()

while True:
    try:
        this_time = time.time()
        if this_time - GLO.time_last_reload > 300:
            GLO.time_last_reload = this_time
            browser_CS.refresh()
            time.sleep(10)

        try:
            browser_CS.find_element(By.XPATH, '/html/body/div[46]/div/button[1]').click()
            print('Ping error passed')
            time.sleep(10)
            continue
        except: pass

        try:
            browser_CS.find_element(By.XPATH, '//*[@id="complete_trade"]/div[2]/button').click()
        except:
            try:
                browser_CS.find_element(By.XPATH, '//*[@id="trade_canceled"]/div[2]/button').click()
            except: pass

        next_do = False       
        
        for i in range(1, 10):
            try:
                ele = browser_CS.find_element(By.XPATH, GLO.steps_accept_trade[0].format(i))
                if ele.get_attribute("innerHTML").lower() == 'yes, im ready':
                    ele.click()
                    next_do = True
                    break
            except: pass

        time.sleep(2)
        
        if next_do:
            print("Steps done ========================================")

            try:
                # Получаем имя
                name_1 = WebDriverWait(browser_CS, timeout=5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="deposit_buyer_found"]/div[2]/div[1]/div/div[2]/span[2]'))
                ).text
                
                name_2 = WebDriverWait(browser_CS, timeout=5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="deposit_buyer_found"]/div[2]/div[1]/div/div[2]/span[3]'))
                ).text
                
                name = f"{name_1} {name_2}"

                try:
                    name_3 = WebDriverWait(browser_CS, timeout=5).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="deposit_buyer_found"]/div[2]/div[1]/div/div[2]/span[4]'))
                    ).text
                    name += ' ' + name_3
                except:
                    pass
                
                time.sleep(1)

                url_path = '//*[@id="deposit_send_timer"]/a'
                url = browser_CS.find_element(By.XPATH, url_path).get_attribute("href")

                trade_info = (url,name,)
                GLO.url_que.put(trade_info)
                print(trade_info)

                print("Get trade link done")
                    
            except: print('get trade info error')

            close_window = browser_CS.find_element(By.XPATH, '//*[@id="deposit_buyer_found"]/div[1]')
            close_window.click()

        else:
            ele = WebDriverWait(browser_CS, timeout=1).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[46]/div/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/div/div[3]/div/button'))
            )

            if ele.get_attribute("innerHTML").lower() == 'confirm':
                ele.click()            

                try:
                    ele = WebDriverWait(browser_CS, timeout=1).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="complete_trade"]/div[2]/button'))
                    ).click()
                except:
                    ele = WebDriverWait(browser_CS, timeout=1).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="trade_canceled"]/div[2]/button'))
                    ).click()

                print('Confirm ok')
        
    except: pass