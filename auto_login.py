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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F94E0076FFDD0F37FC3758A963387C0645E20E7E08698722A65922F2FA5CA98D20ED97714F1AECCDB2C1E6BF00DD3CDA2D53725B1DB8FAE90DC2CD30AB1F788036C9AB5966EE157DC3C8FA62B9F5BEE872A6D3E91139E1C299277F8007740444547CB276C312BAECA2D9A70584688A2F46E02137C6F3D3CD3BE1C800F809AC5B7A601E1DB12A520EE345C19C15DE71C84BFF397F6897919E3AA05AA2778A77003A11521A93083D3B960A353D6B81EA83B30655DBBC3C1E8A5C78F9EA8BAF782B6A863C38A5FE96F3B1DB1320B08AFD753C79B27946BF132FB6FC4376D4B5EE6AECDF558E79ACDFCD1B7A918CC05733AAE90C353D97D8A235754D418BC2C23C5FEBFC0672F505C307F7E147834659CC047F64EC2081A76971109B78FC68B39481BA5E859080B8A186B2A92E260B644459BCBD786F482153B0539C6C946D06E85FC2A059FC52C6F308B05DFC154B1A3CE0CE5E3C2B642586F239C91DD181B589E88A03DC497807EE7175CD983585DFF80B92A9E5FDB97FF650CC510C41CEBD1EDA990EEA74D498B0C85B0E2634DAA795325D4C055AAA781B8B123F4CFBBB04A428"})
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
