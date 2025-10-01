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
    browser.add_cookie({"name": "MUSIC_U", "value": "003E079844B18249BE8B4F09DA828567D5919EDFFAE325C9DDBC94657A26609F775EA786056362E12E2BF238AB6C6527A009993F25F0B1876E8BD4CFE223A083EA4137107B8DE08C776508B8E3B6EB96534DE9C1098229B85B5C027370FC78BCAE0685DF935DA501EF73CD7C432544F9DCFEAC30CDB3DF6AFD31A5BB1E15ECDAC1A1E847DD4691F16BE06FC41A54145D9E5E3547D821FCB9998F3AC98B234ADF359B37452820C34A90D5BAB40D100E1CE87EFE3AB85DCCB5D63176968A53952150BAD5DEE59327D39E628B9124F537AFB3FD7BE158F10EF701CB7BA749471E2CC3733171C18DF33FF2A4AB9B779C6B79684731A4B81AAD1AC6EC6C221A19838615BBB2DF3015AC951D8593B09B2A106922B310913AB580BF0B0A81D8B1E875AC0805FCA8F409CAE2E03724CF38D53196F270E2B63F70D45D3265746E8A5A5191AFDA96FCC42A12212AEE2D900751BB4A0B5AF8337B85D0E622FFEB9AF2BC29A2391481752094D8A1DDD7A0E3D55E06B11229E42A83836237DDA9F5C64B25440347CBF2FB9EA0AB340485CC51BACBB7403635B90F10D5F1F576E0E45757678FCA9A"})
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
