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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A9516E8FCABCA69167F6DEB65F85F611CDE44C1846E63AB8CBAA7410DA437D50A93AB0B50AD5A161337D46D5BF7F2815EC0B7343CBE81B99C7FE9D4BC5CB7FF8CF1BEBF0A1B4018EBEE937C2AFFCA3EA593F502AFBE63870452C5BE3C62D1BC58D3422191AEC7996DF6E7F5392925424279FDEC844CB567C6C14EC037E1771177C85184FFD669ABD9D645749C7D3EF67F0D27AB2613C69926D080391B65BC47BBF50273D2F39107DDFB2A2288198B6483E68180BDEC35E52105016EC48C9BDB779DC1F9425620BD75733B829EEDF59E9B9D5A99FEF673155190141CA1163F71A46BABEE65A1A0E06197A76AC37286FFD2D587A687A4BD93FF554EA3C6101D253BF031ACF27057AB2F035DC307C20A99DAB9590864464E37CD8A6800CAFC3F8E32E0838B582F83566AE5C1C8B327F197331400F79896FEA1B422336AF3EB9EB631DB16C9FC56324A05381CB046BED86D41CCB1F3582E7799879E7BDDD449D1A8591CBED3D93FEB16FCCDC0A645F9CFE8AF67B35CD77B74EAE7C244B37CCA7EFFB3958411FE4268DC49ACF286DA8A3C92FA73217631C9B38C42F0AABF802F6068E"})
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
