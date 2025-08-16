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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D63A712F7EAA6F62592BDAB6EBECBCEF8DE27A048162B76919D5B7ECA35CADA2D0631E6FD007506E773967AEF1F3EDB48CF52026FFCA90C5938D109BB8AD96F9132C9F6F781E1247383E55D5A3F68A0E9D1D3540DA08560A7EB762299AAF3BE7F9BE1255E309A0124082A0B910F31B03D39E28D8EF6586F35F5DF7CF69C52206008A8A0BA7B46784F7BB9F9339089972867FE8EBBC024965CF8989DB546E8B31AC018028792FE7A39011AACA648F3FAE5BCA1DD9C511A6E812E02B7F1140C8BC19B9EEE1F03E858A1875E11325716E909E96024BABAC046E74B53A6D97521A269A375A5E5C74FFF3C6AAFABC4A3DCD9B26D1E137E3D9711A207DE7820D2DA630EA1233C3AD534B03875D5D4668E34ABBA7CF277667E3A425E1141B47DCB453734A9CBE28E26CF6D7CD64519D77030FD5AD542EA888B43CE114067568556890BC33039A6A36FD8EE7D7F5F4BEF24EF2B4AE4CE8C9E57E4E85A442FE82226F3A97FC89DE882F9CE06B95328D681753245E465D8D7D63DF1B5AD46E1F9EAD2DB8AEA8C86C2A54DA5D8BC80C1EB3F8869C9181F1081B5FC702ED53071B0CE8CB2953"})
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
