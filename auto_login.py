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
    browser.add_cookie({"name": "MUSIC_U", "value": "0048CCF312BDE3EF5AB3A64B70D21D01EC51C530657A45DCDFB096EE89D3651C9C3DE96039633DAC9769B5459F4E1CDD07A5CF804D1BBF3598D2D0D8D40AC7454FB1DBBC38B700823562DC3DEB72CA42ED3166D1167D506C7C0C4619571151D1D14320FF6A303B7941A8DA781F1068F579227B2BD316DB1C74ED8EE9BD152A33477F3AEB70B719694BB2C48516946FA45A59B49335377FECC59BB2765D519B946A05644DA5EEB2609CFBBC377C4E48C5DD4CB517A597B6558676FBBA0764F7E42FF99C9B1186513C977D2130E23FDD8EB8A093BE725F28CED4FE16D58E2AABA8E21043B4B01AA57F8D7DF5768145758BDFAEB335B5D20F381E8E5F36FD58F005F4B1C86F820E8FC705C437B2282F00CFE612A48F984D031B5DCD1179A5AAEF03F10E95324C53A115C70F6C95A2D82C7BCE887E1141128F930073A0BF38098EB58417E878B520C93CF5234D89453A03875F763EC6DA49A480FA144F9F5DC9AAB45118F52D3EFB577A4FE886CEFB16ECC58238C775F26522799F639B037A6D7E5EA19204ABD04FAF59E06F7AD86F1F5FEFB3"})
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
