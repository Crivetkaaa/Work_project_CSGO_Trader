from selenium import webdriver
import pickle
from config import domain

def create_cookies(url, filename):
    browser = webdriver.Chrome(executable_path='googlewebdriver\chromedriver.exe')

    browser.get(url)
    input("Are you ready?")

    if 'CS_cookies' == filename:
        token = browser.get_cookie("PHPSESSID")['value']

        with open('CS_cookies', 'w') as f:
            f.write(token)

    else:
        pickle.dump(browser.get_cookies(), open(filename,"wb"))

    browser.close()

create_cookies('https://steamcommunity.com', 'steam_cookies')
create_cookies(f'https://{domain}/ru', 'CS_cookies')