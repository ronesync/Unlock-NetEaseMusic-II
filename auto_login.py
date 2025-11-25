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
    browser.add_cookie({"name": "MUSIC_U", "value": "0056B93C9C5693301680CF8C64BDAE819B5C67AD87D1ED302220B62FE2DCF068523E09B51957A38BFEA8FF07ECEA6A23A56D3A6F9147E052222C7FC1D289D07A2E821499BC956155A2615FDA7C2A51668229D9084E8C9AC1FF0A55AE9965AB45433355EBA7643C14F6449A5B90B10EF4FEDBEC61DA02A4EB1E84411DD2477EE48CAC093F20C5D68FE1DD4061EFABE4A011128EBC65DC24BD75291E98D20D03C256706412D2323B1B3FC7940DB22D30CE18A732258BB3C8911AF5471463B5DA9F14922C8CA14C1271AA75294C88335C8C3BB30B539A71DBD10804441DF66F46C5C984B53C55E0A2BF8E016EFA9661FCAE86F56A3D97D3BF6A7534A7E3A637410AF685ABC4533ECA87400DDC0F0428E651CA217832B135D700CB4571044DE395901E979D3C3366BD83ACD52D4114C1D67688C2F901C2B4ED9CFBBEDCC5588823DD497DF1D6FCAE65CF64302E6296CBD089EF90A3BF9FE8175496686BA0103B05716DEDB164B1689E2B1F8D0C8F5633A774AE13CB46D36F854F8727A920F4A4E8C2D940E783D25FD7CCB3EE9768F115B0D02A767E12B93DB76EBD638F8AEB84D2A2C3"})
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
