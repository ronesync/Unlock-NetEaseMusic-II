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
    browser.add_cookie({"name": "MUSIC_U", "value": "0009FD1E134FAD629A1DB37DD6B97E931F8FC06B2C791B6B431EB05FF5D4F8FF2B83B84BF3E1E60A154C18C5DC55C8F8E9A22C1CC2ADD81119825855C3FA4DD432239E0EF5CB7C9CFEE74C1B403A02EA71136ABB99F677DC6F8D0D9D78AE3796668CE02A4D106F440238D0CEA38EABCF9C3E1484D105A38F75C0AD4E527232FA3DFFD16BBD934EF5C50D72825240077FE94E48F5A6AF224AE85ED38FC62FA4A48834EDB231324767658C148BA4C6D132B97643B4A37CDFE6446AE7EC773FEAF953748BBBF7EFAA0EBA8DA4238E8329E6D2AF2A04188EA74D23B57A35667FDC7962E3A026D2B524DC10A4B41AA0099F9835A9228F4AA4C05C0C2EA9F0C2D61489FE09BCE419B1D017AB762D72CCF098730CE288295F194F1059483728D12881E567D11D17FDE7E9A45E5CBF1EF604C109F303D7EFC8D80F0499C6D5120C3C3ACBBA4B20AB02CA4723185270054201042C1C3546AF1443DD5CA30535D6BFCC14AE6AB54D682C81FF3C65BF2D671BF714AEA215EF29ABA2A3280B7CD63D8339508B2AB3EA1DF59A85CEDFC39CBA82516A418C179F71A387259A62BBA4E341D15AD802"})
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
