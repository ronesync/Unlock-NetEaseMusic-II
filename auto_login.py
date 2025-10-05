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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D92451D10F4851EAD68C1820507EC43592DFD29376D2428321F18F1B5C987ED7803F4A95B498C6BDFD4BE6DC6AB354629B46852B794EEDDB9B25A652CF6DCE297CF1B979B458852C28AF9AA60F4B224E5DA3C69094414EBF1698F1E3CD544C5A0E4344EC8A57DFCC5921D122DF058B87E5BB4F67761A5E4BA5EB7B069D485E1ADBF6F6EA332BBE9550211C3141FEA8AC60C525BD94B313716C86966B1E3D6F97E8469909C5FBC9E201BFA756926A026FA3D7D71F3A2412540516DFAB40C98D0016C90704FAD066F4D1CBC4C52CCB4DB0E1176D4831834AF391A157BC505C679CFDF26A88E67CC88D423520E11A528FFCA42EAD133F77330FFBFEB0D22A2FB7D84C3521705F4DA1CD092E73072340468DA06730F58DD9BB1C99F29353CE24F004471C92432B09E63E58F31F16A1208BFBCA37D2718E074D4D25545B094CA675D326E3146CE88ECB7FEBB61E2C24B645AAD657DAFD56E7B1DD5C3FFBC600ACC6A4919ACBD3915A548369991B4C11D9FAABA0230E5A64A59D177AA34897E8D43E801EA9D174616CE887293506EED2471DA74D65A808B81E861CEE6AA6829AF5DBDB"})
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
