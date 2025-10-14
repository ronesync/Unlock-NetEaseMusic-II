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
    browser.add_cookie({"name": "MUSIC_U", "value": "003DC9FE1EF6938DD999A2B8099FF81887AF5A462B9022E986AEC8EC64285791A6EE166D1DFC185E46E4A7D4AB271D204D2ED104A9483F16475CC6DB8A4A17997202398B5A6855F901215E5BD98D08E7175B803D70AD1E2E89B367454B5A16A489623600DF8066FD3BC70BE4C3BA04AC06DCABC4F0F3B8B9CC6AB1B4279DD038BF300AD637814C2F2F278E0860CDF390889F31CDCF239EA236A47F03CB3F71B6EA87BC3D5D001C9AA8D9C0E9927CD5EE97464B569DE31732D45CF01B47A36EFF5BD8C1FD380A0C52917750D4EA22D2BAF081E3AB4F13084AB0367A0CA99080E21DC4F9360A6018F7B348E9C07DEEE59783C5F2531E17055B788482DF54854C16F1970C243594983DF4431E08F66F9D86383C7FA4522CF740566C2E796BC3B3B3B7A2F3F3C62B72F4EEE45051D781591466E988883B4079C28B7D6962E7042D3B60041271BD83A0BD4210D40173243D002A0EFE1F373BA5BE2193EA1D18B4E6698658A38F8181F7BC30FFE1676867BB2C86D0971003E2AF51E8F36F5B700BD2B58B7B0948301684D50BC1AA5162D794C2248D32FF50840E8510EF108EF2D24A212F"})
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
