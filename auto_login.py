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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F66FFE0F5BB0B7E54036212A5FC5DEBF130F478F8BD61E8AF5F608737A87C442707939B040E659D4CA3EB05BE41604E250266A773465A4E16F2087864CB5353C881CB8B9B00096CE4B607706E451E4FAD96298917DF403ECBD216504F79A37020D8D1E6E71FE1E230998A16FA04E2D2BBAD393A1B31D8C808A59D1A9F37C94C1DE04126C1983E81DB24DAD6A4376EAE6DA6B15750C384957EF6E16D175DD0DC3CDA58823922FEB6EE9A96EAFA065B6DCE88BDD183997155EDFEB054F1DFEF4DD4BC0939F3CEBD6D7111AD69933FDFE2779D4E55090A959EC9465B0D82BE5D3CA124F9559A73744ECD3F898059DD6365BC446DD95E0346549E8033D816E9A15D8E3618B62569401F55E463811044265DDDB4E66AED9CC25BE62EA3EC04423F9DC6BAC8398C34542E9D4F961F22D0C225FB62F1A4640E361F80DD1E1D479B6F99109C6718BB49B325E0F70C1E15D02B8EB95B691215DC7F45CC7053B684F9D476A50E602BDFD53D724E084F8A2746ABEACC354EF396A1CE4BC27D01A82C8DCFF571950A8E98D3377F1C4650DCB93422B61FB73F63846CB3AFC334162791913AC48"})
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
