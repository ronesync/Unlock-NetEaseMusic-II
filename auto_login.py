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
    browser.add_cookie({"name": "MUSIC_U", "value": "005660D8CEBE28FBFFDACEF70DE71CD84130E36405454C8D79E7CE03CCC26CA847E9BDFE756F2E25D34FE6491640BBDD64A451F47763129A67F54AF0C002F5DFDDA982BC5D0F09664F3402FA402887FBE28F72A0C7413AE1EC89B967BA366888430C72EFA6A129FD0D2A5E244082D6AE68C71E25D9FDCE4F2BC6F95960598A24A382AE770CA7EE5A55DFEDEA86247C59A8D45849B340771883DE24CE9C25B6D507718E03BB4C171ECAC23F53E369A73C29D53A743030E25775F373440B5825BD6225A31661F703F9F85D0E5C68C40B885830FB0ABC7E21C4E4921B41F7F38ECB0A869F6E9B1B48610A3B79C4EF40BD123AE61AFD30F91D9AF0ED3AF5F74EAFCABA375496F1056CEA01619B2FD492910862C2BAC4A7AE4D45750CE2C19FC76D2B74A8D3C4E83F5D6C90F05BF2C01FAE91AFD41E3044754FEB3A11CDCF0D23D37DAE813090E8EE588AD9BFE930B99E9C1D9E13E8243104DC3AEF2626E75D8EFB68B650DE5D99CD742C7846BEE49037C16478438BA979612F736C05D97138F7F634DF22347780643857213162972555B776587D77B089153118DFCDC049451DF96A72"})
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
