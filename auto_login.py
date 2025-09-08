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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D77BE4E1394C4DD5C5A4105A0DE670CEC8DF0FF7AC0DA72E69EC1D140204D0CE553550B3EC9C9739AAE74E90FC83912FE4325919DA3F02CF1D23AE1D15135D8E4DD0FA58B481248571F258C011F50AE8C91B6D206024E65EBBE7C2A4A98C14DDDC0F41E5CFB4724210174617C2FE77B77B1BA2297064A0FE3F43753634581B6D3979D9ECE60375688F3B305C657E1800E984672336D13C6CA34C7855D801016A8FC04E467426D0A5CCC5A0B3F1FFF33B4E23F1AF5161379D4C38A4F69C654784EF9A418F958112C50ECF3B3D6921A6DBDBF8C2DF01E509294F544FC68DAED37F9C83A8B298BB8748C2BF3DEF45ECDC8DC491D080186BB525D44F662B5F3E308406B53F2A5F7F600632C6D67279C1DE8C16AD4E9BBE972415B70B93FA8FF56BD93966DE1067B1E4F21F26549D9640E4B14F1CA53CAC45BB599EAA03983AE941DB355E71790F660619261D0ACCB44D277571456283AFA8045506A35F16EAB4227F250ADF24D60C971D3F760C6F640F649A7528C28C9D1943C23D97C652D1E6DDB669652EEED4643EA49D2DB4EC1AB22C08EB49B79B33C4467085D1EC359094079A"})
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
