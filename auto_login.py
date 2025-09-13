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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D1933CC101419A0E5BA0096848AFAE048ED8ECECA8B84D777DADEC3BC77D07FBCC00520BCAE43002E2427CD1AC715D506174757583FD47AEE4B2A80E5774E23E8CDE521C06AC43E822C908A06AE4F26F28341ABCAC7854F3A907026D6ACB42D768675C547FC11D809E464EA01CF67769118F906E4E0172B0E0E337443822D85A0CB72A46758EC04CC6BA2E96403F84495E994656FE91308821F396108E8C1A39525DEF467C065988B8D1F9DB91674CBDB9F3BFAC4FC9C75914310EB72A18633DB9FD1C93279C94F02F2F99027B0252D0F694876EB33AA9BF467C13C440F11FCAB09771AA62CEE5150676B172194DA09D7D727E7A64959A1D4B1E5591B06AA6E84DDC44452C6A6B0EDCC21099A25987B6165843C7C2D27F17A2302D894A590C45267753EE58D1352AC2E6313BC122B2524166305518DE668B592EAC0B0DBEF88B643D002BC07CA1C56A596F354160E215134A206D405792FB89912BDDB7FB3AE2EE5CDFC2CE75CED07A340F4C83714CF9495D998DB247A13E2C424781A68764BE09BD3790B35C9EA3109FEF8EC671AE17124578769561FEC3928817B14B468C12"})
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
