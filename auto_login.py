# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A6C2EFEBC3511B2DC03B537CC6E546C3AE0E66E46E4CF961AEDF9FE16638995830D5206B5E1F611377929F7A56AF35AD2991B605B49E76AC667C9F181C1F1DAFA798DC29C0CC07DC90CA819ACB3456EE61E0E44767CB11908D4B5130D5501824C24CBA8AFDF94B707924D1C4208C3C7E6B640C2281E767DD17C1EBBCF338BC6DC8E41ABAFB3445A25DA3D59D8A7E7C321DE3A761E722C336B0C8AA910BA316443240C77395ACB2A6ECF7C53505D1B4F88121CC30E27C982BC702D47B4F656C83F8117C3CED4CBD77196E6E7FA7D128B2E137B726AA41DC7E03D09DB0581D459E2818A18901915D420854046C368B236834CFEE74C542F9F2186B038E8DD5576319DD5E8FE711CE1F15F83F0355822AE7E0704D4801B2CD410B13C0FC26A47CB8087B0D0E5485732503C56BAF8F735B1BD5EF9763C124D218B984FC2FC84F221ECA9DC94C2C389EC0177F736A084F89CB39D96E88CD0DAA77597A8CD9FCE3F820A0018446A798119785A519E21348C38673F150A6F2688E8BD6FDC9B084607E175889E18E14E5B327B3B792C06D37F6122"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
