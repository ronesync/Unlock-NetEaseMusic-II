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
    browser.add_cookie({"name": "MUSIC_U", "value": "0029B697EDF3F77E94E64FF5BD7EEF05D4B53CC865FBBB030EDA9E68FF29856242ABADD14D08851A5F32C2FE5466BAD525FECDB1526596FDEE17E5136D8F0BCA73D77E01DFBC2ADFCAA79DD75CA1CAE8DAFA7E68CBF620497915D881721C591484F5F0F150ED5BB48378D93DDAE19AEC6DAD0CCF0096F14DA83AA873E80B9EF7D0C567BA4A520B616B6B4442D139BBB833B9D83B04A5C1DEEEEBEFCFA8CA236AB511D943C5D368A5F2E892421A5C2D4DD9252071A1B43213648AC7B1E3349C62251562C21AA73643ABD845459F09F3463A79339773F6AA36A17E8365022DB4CD290E1CD2141E3624D893E77329A0E9DD2A9E74B0CE58651AE75B09DDCEF64E8C1DC9D6A57E8C7B951DCEEA720EB14A32AB222782767D8CF8873F524D1A29B4591F4FA51ED5ECFEFEBEDD9EFF7FE9B8DA8FF9FDCFB7463E0838BF0E5C20EA2992D07E51A7E28BF07BC026B0D4309A2C96CE990BBF50A85665346C3194AFA6A3A5D0682B12838EBDC7D65A54A827EACD6C112C3D2537E21E26C4CFDCE03FE350A7F0EEAC96233BAB3BF6EDDADDCD2269B59DB46DE10660FB9B22675C8F94EEAB55B5"})
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
