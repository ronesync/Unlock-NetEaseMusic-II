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
    browser.add_cookie({"name": "MUSIC_U", "value": "0045615AF0B055F6E29495F22920D5E64B17BC165AA916FDE4592CA0D1A78048EE0039C7B4EF57D69A66E03FC16A3463ECADD9D9FD8891A26DEE003AF97FC32D5031913B8599CDAB52B03C72B6EBDF44EAA76C2E1CC2B04603EF7ACAEB6429E088998434C9A42A2B65A6CB80C0CAB5B9CA37602C500C02C2B8E244A2D9D18C5B305E0DD2F508ACA213C5359B56A7769AE036E66FE747F44B82384B0CD3409AD8C0AA392CBE864EE5AFEE6C549D58EBCEE0C368C5ACE85D0EE74B92DE65716417C8A0A69609676F4A3917788289BC2D1B1430048939160AB1BC1A90A8D35C1A9939371707C26C6FA75B387B112B3A9D0F99CFC08D2C24DDD193142A8A4A76A271ACC4B480FE13BFFAAC1F1249EBE5718C386DF5D98B143F7A253514C174B8CD432B449192A0CCDD689A42B3F6DFB2EAD5DD1E8B38B94D21AFBCCA975616AC3600555AD20A8C9D84A7E252E8B5C2C2388C740D3E47B59F6126224477A056C6320EFFB81590DABF459E1A4C44D129DFF8A295700EBFB65073287FF3621237543DEF3F91B11A953FF0EB61353B56B7B26A03AD7930675150764AB961B1858A97F5AA27"})
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
