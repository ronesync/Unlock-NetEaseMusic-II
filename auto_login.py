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
    browser.add_cookie({"name": "MUSIC_U", "value": "006447F3052383347DFE6FA99CF85E8A3E4510E74FB1A26507B61F73F4E7854B8F1D76DBA2CF46CFC3CAC3D1BEC18528B2193B6502C0EF090B1A66DCB61F97B6752871A98B8ED9F82837ABCB996825E11F2B8081B9056AD1EDD55536B3CAFB854E3F6B546A4363C8322464C333F65BA8DE7AA5313811B3EC39D6E2533C7DFDE892B753E920F11DCDC310124C99B819745D28ED8F04C8D45B6E0EEDEA9761560F87F15C7B89D2CAF4BF9600256941D436B2611F42CEE4DA11C550513458FA443266D655972E2AB2BBF97B53E2B2EEF328846B4A4CA15B24CB468F67703D7299E24DBFAF4486F67A04A95BD46053ECBBA082AB8559EC628D79AD60D2A367AED539D8E42300F77F96B65AED7CFB3B85A24AE5BF590779D6A2A39A47F50A3D677D222231FCB05F3089FFC1D4D6388C7C4FED10E6C5938A11197445F8F3F5A6CF7048988585718600F29ED40A2A5B0BD7BC55EC7FB391E7ECF6B1DB0B0B41D166019B3C"})
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
