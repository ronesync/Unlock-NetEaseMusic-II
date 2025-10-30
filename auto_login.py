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
    browser.add_cookie({"name": "MUSIC_U", "value": "003A335345790061ED19AD3EBB2290D490F98604047860CEADE482FCE26DAB04E67A1D41B105E5A69FFBBC8DC5AD95D4D31E39AAFB71EAECB84FBCEC89C725EECB4DA953F8E865A903B379D65B051E60E08C70E08F59303499730BE4E1D6195F7D6A44F548E836F89E17E8FF4FDA7D68EE78C16471058859EAEAFE511795CE79723709B30E3ECEC083C6D6905427D301A2A9AAF70BF680EA2C7AE98CA1578AF43D32A3F651CC6E52BC78EA89B1A2CF0CF204ECDCAEE5A38166E21BB4195481AE919756FE55AF5F12FE868CAB82C531122D3BEAD0689F250736246FE5EE1DFAF0F9C2E0E774FD566E123649A89EE5B1EDDA2D43EEFF8E2DCD6B264BFC87611C326EC5B741996A88E1AD6236C38172EEEF0816ED47ABBDA63720FFE55AA0096134B98B20A84F79C3F1F11DC22951439290973014E32098A8F917FE2BF4D75BDC55F2ECB114EB96F3A0CFFA0FCFFEE6F18E747F3407E3B8133E8F96150E664387C6C05A10AC0FDEAE0B383C87174E33C6E8D0625BF3321AF5C80962836DDBDB04681F50DEC36DF12391B0297850AF93BBBA9529161E066D0147B7CCD7403713C059AE"})
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
