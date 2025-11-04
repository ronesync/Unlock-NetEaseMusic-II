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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D33B874C63217F80B20E5C472B922AD5979D278BF7280397883735C59308329D5F0F464907EC496FA2D19218A302428959AD517D475C70979051D4F0AA8F4E4ED10FBD5579CED2B0F2ED51F73B365CC03B6FCD00E538F89397845B38AFF8B412E10D1899899C67B78E8C9B02A6D20DA4090C7893BE35D86860F285DD848EF55F0765704028402B5F19EA67F34DFBC267A9E652BE6748D26F81BA872C5D32BE6A689366B1972898DF86DF2AB3A454C1232A5EF0094BDEA34441B0502121BD8BE22EA9DBE5FB59AC436C529998E11A6B30D41C1D5BCB889CE26425CD64B1D760382ECD59FFEF7EE5C7A411757383D1D30473E75F0550BCCC59D6C99A112071A49898006C6E6B981D359468E2538CA74A74F8CD829BD5F35B2139C05B23DB233C15AA639376C7EDA27E835D0D0AAEE537766F6893E2D36127F7F9A10D12A80CFE4E594406A50F192FF0B6A594936A4C6EAB328D59AD88292B00873D7342DFDD03797821C2129F86CF1828A7DD317A9982916DE675B906A2BE9749CDE1255D72AD12E5274A57CFFC98127668B339054E9A9D88EAB8DCC6D285D300AF67C28DA2F773"})
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
