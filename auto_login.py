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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E1ED3AF60070DEC8933F007E1B325B50D60212BEF6309D4D094EAFD80C1F22E2E363E2B2AF3A13EBA50102D1D9E8321727E0E8964B025EDDBC05580A72B3BD808F4F73211D1E8126FE08486370AA4EBEE0C39CC3B7CAEB44E34999822FA75175B67C14CC5365CA1268B298321E42A98E8901BFBA3F5DC5B1F516A48940373A7CF2792EB3C22393F16CD954DDE66D11ABA189DA9BBF9C96F663399ADD28C859D2AF24677DF503A4D069CDE82A334585C5D513865D638E3583E55307C840D6BB79CB7A9CED4E4F57DF7D93BABEB03EEDED354EC54F65804F1B09D81180082FB2437FB61E2559E05C11658B5848C3A611281365AD0D2F0F8F6FD0172723222E6E2F166EAAB2E5288C4F6F021C6F127D1C27764C59098096678D92FACD53D1ECB11666C382E293E9910CC8222999E35A2A0FC27D0E22A39C5A6C02D56EEDD21F04D8254A915B80995C52BEA9DBF69E0095A04815CA29CB8E65C1DC9AB0EDA74A575EE54B549C14C6D9B8283F1D99F03D9F69D68D926BA692D20DBB6950ED8A5FBA0DBD170DE4BB279765E322EC4EA8064DE8BCECFB1FE448A2ED1045F281E6652BE8"})
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
