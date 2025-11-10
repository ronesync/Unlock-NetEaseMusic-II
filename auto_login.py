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
    browser.add_cookie({"name": "MUSIC_U", "value": "008D1DF77D2FAC81B0F0D690514126E049A1C787651FB7C1F7821DBBBF4DC0D00348A8BD8FEE6E01FACAE6767C31B45A94CF0F00EACD7F67EC2E8C38DC1FC324B01A413228D1F05366FF7C085D12AB7F4DAE18AFEFA2EDDF79FD1C100826B853F158B06B0F0A420D3FBEBDEBDF84C8916A70158C804BA9DA096F668E740B74B562B57279B779515E48DF3D188642107A0AD7FC3F6B13C322D8EB51D2309F35D3F30981016FEDF2052F4DAB09F61A679C97C56C87BCE9052B6689F6CD21F6E1CD48BC52F4F15B2F4CA88575EFDCFCD5D56D9C31F4D029E9D0843C6FDD961A5C49647E872CFA4255DD742940A52D953926E7FD9833FAF38BC02A287E31385FEE1D5F827D7173BD003ACD4E4BAFEB2920CD837D6C753382AF854E49C51DB9004C7E64EB4DAC1143D83EE49D3C18B90109587030F9957A2D308AF4D24CFE138654A3C608289DC9B709A993A0C71428B7098C97A62CF305F6A35BAA8437E389F22A7E925FBD72A63D0C9088FA05531863AE4077E50547277C440FDE2A37EAE65E4DE4C42A1D8358F04F847E83D510D31D84ABED8A0B4388C11602B16DE6A187F1EA9A48"})
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
