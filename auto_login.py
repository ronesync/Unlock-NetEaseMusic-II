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
    browser.add_cookie({"name": "MUSIC_U", "value": "007CB30319E38AC76A7AE878B431D303B98D2993D217A1171F772CEEDCD87E80A19D3419DD9F33C7C85C582CB7EC76B129E64E9B6AE05444B850EE065DFB38DCDEDEAC8BEFD3F23B74037D132179A3CDD03648539A30A0298A37720E489946DFD93315CEEEA30067F7C3B1D39D60E53624F01C24B200A36A0EBB4CB6B3F6BE50B2F6E3398DEA83563BF600BB45101CF6312BA5E903BFBB8C425D95F50500CDE23534D08D9A6B1A76B752F6AC267CF886471F70C58FD012A78AC767D7B9E6D61DCF64EBDEF32FB9473127A4087F150BBB2A859A62CDA39D915E14D5164CD9A1E819A85E6DDF918089F6551FB1DD198C84995EABE25B318A164AC6F27FE2CF6C8D858355B7C4957555392291EB92D5F120108158B9F68729ECD507219E1F5203044D563C90759A1F6266AC6610711E2D9134F78DC93D546B686E383B344D2C1433D7ED7BF97E095D5ECFC0201618FA5A45985FB913CDFF3B09DFB95051800695B6CF26522B965CFAAF76A2C8603782F15CA9D8A8FF615B74E87EA57FAEC897C914F8E3D0A8354234451E85E9C2FD03E9CE0F2A610FC4DDF17973BFE39132E4189107"})
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
