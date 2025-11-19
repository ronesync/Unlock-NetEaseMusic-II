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
    browser.add_cookie({"name": "MUSIC_U", "value": "00633BC3CEA99BB8D4C6B8CD573722DE872A676C3BC2698D1E72AC23A5C5E436442835B1E4B0E8EE0BFC6E6A886AED04670FAAD345FA43375F698142F444E47434997AAF80C81C8A18F67AEF4377C893EF7A8F105302C86175A1E4E73C377FFBC19200EE02C17509B92138F0DE477284399839755B4B4C7A2032208B77904F8C015633CB882305B93DD405503F6083E557F8622AF9B57BA072DEB14E617AFD27D39AAA392DF0BE57D649DB8471436AAD01B637688546834773B6D908FC429ABE5A51154E97F9BC8F45AA70622190CDF6C90C305D1BF7D25BA35E0BD09BE2F01EDDCDB2D702E3C497D6680165C981E33E1634DF3131D552012931DCD5FC35EF7D087430047D9280374CFA160EBD7587F24C3E9FF6A74C64E49D0DE29B89121CA607B0A14F15BAFC5889488A6696F1B1115361314DEF7105D04C184790B9475F76FC03EDEFF263D03C0338B6C1EDE25A0EF62B0B2D13889E2CD9B304E42D8D8E596E38CD6817740DEDD0D2602A77DD6B35A3E162195E4BAE445269495730E14C2E97AC8C761DAD14F136927643B9D98DDA35D8D2E1F4CBDE8B4D9BEA74B54F0C4287"})
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
