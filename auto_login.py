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
    browser.add_cookie({"name": "MUSIC_U", "value": "00938D6591E3133D5B476F09C90555B16F52AF85614B37585CFF888381E0606C46A868B2DFE7DD9E27716191552F16A6C769B4C8E523BA843F0F74162AFA633F880661A41274FEA4364555EB5B1515FB00FCBA42E3606DFCEDEFA480A721C742F7B99A3997456007020F73576DFAFE583B12F1720214CF9B1AF6BEDE1CE59A8709BF0230E8556C2663E9AAA1D630AB7B83DDA0A533DF7FD0D68C6CD12A6955A58A7B127F4DB207AE8F4E7261EA9EDC654F9F4B3002BB6243A7730564A6B87160D678CEB14D336B6C7FF97C842FA5A4FFC03814A7858570E9BAA241B4DFBD1AD78FF3121FBECA9E8D02DD846B87A2AF27F41D13F4242220A729C5E2F711B95A4FD541E906329D9D0739B9C26FF22C4F65455FFB109A4E3E0B33EA751270C40FA62FBA82DFD334ECA73729E5CD20A81BD757293BA605FE7062CD2CD2AA2683CDA65223C9B82892CF5627E41316B976B815D696FDB728B7120635B64722D339A7640CF3A50D89AE8E88D72FB829D20957023E7223741DE01E70356F598AE2CA7E6D87349BD6A0E7C2838D8D637D4674E0D18DE665E9A9BAB9A31315D1D5C0F21F7862"})
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
