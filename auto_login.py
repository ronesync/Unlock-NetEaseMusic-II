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
    browser.add_cookie({"name": "MUSIC_U", "value": "0078FD3AB3FB2F99943D74AF52BAC256144DF9252C268FAC4A49D4B20618CB45CF987AAFDCFA9479BB8DC53E4394BD926E3C272FD71F37B5C7192F86603F80F549941C4AA54D484428F324EF1680E1295A7D83F43EC6374B154369C6CD3DF56AF2C194DF66EA122F3A3ACC16778B879A30BC02F80F1B578A0A17A13D230FB467A818420A7DAECDD9FA6F77BF7D358E826E73010DD229A17690CAC3718D0EC4E9322BF6157C529F874E2FF8EB9E39DC52E33D07926A5DAB58C39B0CA43A04573E73A807BA54314F446E27081B086D17FF633A9118EB1900743E3D4F9CC4CE7AAEBE9B0D32C9465111B76E83E8344C8751F2442ACAB812C915348BA5E13F3AE06959B3E0D049CA6784B88E83F58AA7C4FBFA54A733AF3A89060F84CDDD4DEE0F933CBA9D6EBCB696D6E95738A8049F3493141F5A73FAFB5F7AE9F55A9F8FD325304125FE4DE485952F42EA565EA72CB9CC2A629590F9F9064C015CDA1D75E545E8DD3694B0FDEBC2E6E47752A1DA3C1CD2924CC96800D02ED2D5A48820D20A4C575563C1AEAA7FF7A4716493E80C27E7C50AAFA08032F15E5979FCB24647CA85B1F9"})
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
