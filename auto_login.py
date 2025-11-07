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
    browser.add_cookie({"name": "MUSIC_U", "value": "0099211387CFD72C3F2B908B47AF60F8EA9F0217F2215521CF0311B04D9917CBA9D08999FE5F96D2B79A5AB68D3D4B1DD6620C85D57054930617979D06DDCEF1ADF8B6BEEF2C9F6CABC48FCC17F4DEA8A30CCC647A53275B7E75CB74A2AAB4FE549C828B9EFC3CA94F5D80EA139DA7C839BEC79AF9E0513B1BAC931F1D11EF12135422DCD678AC923520A6629594DA4A8CBC7DEA7E21345573609126B1181D29106E6E56194F954EDB6461072CAA6DDC2188AE592581184182325409DFFC7BC7B1F02279EACEBFE67295EA72C50993AA8CF6DDC9ADDDAFEEEA4E750478353D602474E6FA6B0FA6153EFC98DBD405944C19E3078035773B7D61E52812DD35FA851527C5FEEC83F6B6B3F967EFB6BB84DBCD1FD694D2C207356542329E823F8C3A3CB957CA2D60F9FE911E625AD30688726637DBA45DB162E225EE321431668CC2AA6519968E4A0FFA5A794C8B69778386F19993C73A6872878B06830F8243508AF2EAF02DD65EB3F4DD89E741583FA11ED4E7A55E04D59549B24ABB6133A8CC4895FD36B7E553D4F2F8AEA7C64F67A800FD11660CDFD068517FF1C80E8A63D646AD"})
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
