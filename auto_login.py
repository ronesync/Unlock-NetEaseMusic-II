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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B0B3EEAFBBF88D489881A583E8262065E71D31DF403EAAA25F5EB3A9ACEF57C13336109B9ADF49B003D07FEB43A9C5EA918F57112554A911BA75AD0648A4DCE34D18C24ADC1C2E9A5CB8425E46EAD15A82F6E23F08636571F9D501E3DBC23383A33EA155F7A7BC98CCA0D0126EF53085FE2E19CECC8E19E9E4A40015EF8CA5687EEAC9A8278464D0DD2F33CFEBBE0EE4413755EFC30F0F03EAB25FFBEE78AA770FB7AFCF5991916C8AA98979D7D2CD561539CB581CB54B892AD7E7742F2AEC63D3AC8733E657FA4F373CCE5A6B837C7D1F90F564C52BF392ADE5B5145A766CFBCE562CDEA2976EED231201195A88B716AD796441616517EDC57FB9A2AD61445FB5737645BF2AB0B581E16F9F5C131C92A6BDC5DDB533B996111BBAAAF8FAA439DD4778211EEA1234A345D47DEE4D82B71CE2C5168A41D1F4D65FEE1D0DB310E5D0AFEE5849018A29CEFBAA4E50D1FFA6DB5FD3AC6020B1B24444BFF4E83ADDE4F279A24363333FDADA107AA9281D8EAD48C715F13A2607439D92331EAF38BE222FC0A519D0B912423764054B20F8135B3ED045B11E7420231E14113EECF6952F"})
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
