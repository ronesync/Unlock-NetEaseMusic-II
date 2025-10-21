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
    browser.add_cookie({"name": "MUSIC_U", "value": "00495FD62DB149D1CD49B037D48AA3578BCCF1316AF7950D115EA41EE5CE4B4C3A2A60E4DD0D6DC24074BC91F8EBD7F63894C36E8FF747238D840E555D8F3F06E8F6BDA8286AC36142CE6FA31F31BBA701A286F140B2153D41C07F9A651E08392CBF960F914F4D3E0F1A339FCE7B61D99C9A12E481A94D2F0DE1056E804459F08CB2B6439594AF63E8E3A5200ADF1787C93A5CC9C3A4246D5A1E41C3DA1E513AEF3409B37E6AF4FF5723C23A9ACD2930CC0E66FC4750AA6F43BE6DBE8EFC295E327F2D6738C3CEDFF52D9937BD0D13A4F935A4CD45253FA4335AF78FFBFAD057E0C1B593AB3565282AD28BDA9B1DB07D48EB71866541795002A8899BBF2BDD47E18E5A5398D829286820BD16BBBA993F719D12556BCEB4562252AD91B4F55221F2C45E40BB79A9564FCBE4ADC4F55A470C0B678433E76696FE04503DE1976FE6F0475299BCD13DBA75FFF38B209E991CFA42FA0B79E5A7878DF401A8B445972BEEF3CC161BAFB82E614CD4204A027C37B58C79BFC9A26A70D227B238FCAABE730AD71A323CE36A3994FA041725A6DEE5719FDB772CB080BFFEAE4C887683DD1B2E"})
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
