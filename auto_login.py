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
    browser.add_cookie({"name": "MUSIC_U", "value": "00721106021764AD0332F1DA576ADE4B0744DE69D010B306D9F25CFED6DCFA49CB658CA40CD387C1A5087D1D9EDCE8919F25931DA0B6DBC6B6F4E3656DB134AB584072CD13D9577E712049D8085A95501BF32CEBA5C5419EC6BA9F362685976C386A14D6F24A6D30FB941EE352059B97FF4CF6EF383CD18065869EC31D19F08442D0B7DDA302D25D03DB05E843FED4F6F9D470281D80159A3031916C66D6EC22904FE43F092D9A73D3EC930ED215C918C12250AB8B0F80B6EC96638E452350C2E1DFD59E487DC9A13ED6A84DAF7126BE18068EEDC0C24D317426B3111FAC4C0A0B85734CA56E25A0AFD9C961D6F75FA2D0649EA358B61E8A0965E808FDDB53DEA9DC26746250C65CBA82482DAA34C3DB44CF8E698CE939DB04E981FA3B2B2A34C4A017B5688C6A8043B223AA7954364B7D2F79988E8808109ADA53794F4E365EB2F040154DEDEC33D5871310A282DFCA79ECD2B2135DB11513D0C22D05A26B51A9DA6593CA1863F065A3CF4BCD220B751F5B8121816F48BFE2C231A475594873B6E751DC31EB6943F34D7E8C5CE9F9A0FE75538887B68929EB016230EF97081899"})
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
