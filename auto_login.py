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
    browser.add_cookie({"name": "MUSIC_U", "value": "00213C05BFCDAD22F1CF8A3E618F30AF6193A4D68FAF6A69F20A9EC88D5C3A44E11691A402B4CD6E8C06E0BF7E44020A82EB6C4F81BF999346B4B59B4EE8646D3386973E68BD21F7C5CB5EB335E8BDA08EE1C3CF480E81A388CEA997AD3CB59604C7DD12E2B37375AA18FEDB4829481F149D6416A8F418382B65B22506D2A4800F088C50B868188A3B07359FC95C730FF96BC03D878C05955D45C0C3EC61964B8B2FF6590F93A109885B3E1AF5C197A39D3EC8C3640A0047861ABE1E3210E2DB4F3426C35318C83D58FEF6E5AFE243BCCC3F89E60AFDA1928E6561F0C15014B25070B63BE0B2C3E6A8946068810FCFCC711DFB4E96F9F6466CC7DE9B3B386D37C585134F0BAE9A93C1D58D9EF01F00C489DDCBAE0B807A8938E5C4F558E04AE95791001848D6A5AE92B3E5F5695932E1301D2CF1CC34CE98CA87A40E36413E68585548E171274B7AB545DFD28A7146FF995B1A80F4CFA90700D01C37265C5453843735254BEE8A8CD1B1E0BC78D27856FAEE5B24B3A56E6468A29C8A06CAE56161D41C1DA1F7CB006497E90D9A7D100CFA7C924DA4B37BED036794D41F6F097257"})
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
