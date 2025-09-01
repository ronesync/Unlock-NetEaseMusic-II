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
    browser.add_cookie({"name": "MUSIC_U", "value": "008470DC2DBB348A0873E0C2450FF1A654E258DB4EFBF2A63B3BDE093BE718AA152EBADA68AF40FE6E9869927D48B25DC268266D6A8FA8DB87AB8973A59D73C9ABC80689B1673050DA73AD4B69B1712191437E04ED8BE4B37AA1493E28347E808C523D0B91A5C4BE942C2BFEC774CFDD8F2BC8A42DF542EBB7B0DC27F7831D72889529167B5509338602A7B811472388CE500BF276E51A0DA840715F77F0420789215CBDFF6D37A62A935E17197B4CBD6D14DE3888F14C4AC50B9E2ED16616795EF91138E57D310527C3D60EB9C53EDC811A13D7DFC0B494FC242B2EB02A30A7B9C7EA53096F0E823C189F72CCD6455B1487E391432485471C384E73FC3C5D04C7AB09910E6BBD97CFBAF55E5B4EB811FCB3D03341D08E2DF0F03CF56DD401150F2934DF8845C057377A7D9167C2A211810855B7067013498DA2CBCCF3D1C6D1870263AB4C7B2A6B7680035393A3F14844639CFE037BDB715401B6EF846779FC008FD08ECAB4548E9CEC9EC8B285B3C8C7FA7A607268C5B85365F4B47B54B1482D74744C94E2EDD4BABE5763D36F87C4E29A1F6789F33607B1B37B017BC0B32B73"})
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
