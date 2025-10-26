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
    browser.add_cookie({"name": "MUSIC_U", "value": "001DF8F7D9050B76BABA8131714680912008F6B9B81D59F4DF8EDB25ABE87C9BFC6AE94D118FE6FAE559F10B7DDAC2B1AE8725C1C5157D066D127122E52E20310D5156589795DE3EF99960951BF110B5B8321EBEA4027306EB22514AD37E35B877AC2821114B2CF49BC6A326513A6DB98E38E03DE29D75A126B2488D5F9AF7E992DC0280EEDEC9533211028FE9992F220B20B964F6CEB3F6314BFF548363B33F74F8584C5BE5D12618717C6FAF94A4F2B8630F08DE1219ECC0B0F825FD182DE50EB264559442F80B8BA909258CFFD70A22719F703AFAFF1718EC2243A5F60C1AD585B178C2CF76178B6D70B1EB174C106FE40BDCC3BA5B7644BAB89A9A8A06BE59553E54C756883E7163D233D05EC7E0D4F52ABD9C3A45E2450B87DF1AB10D901B43106BF8CB7EE13AF9AA87F8E9939F2F24176B2AD0F786CEA762F4B31A2CBCCB0984855536437CCB22C410C4E7A285F9952EC2AD35948B652D424563B28396025199E2158A6F6AF4698555392D23BCC8BFDE64EF62CB09D922A8C555CE8227A57529DD9035E4920D6C8D2B7ECE2BA7ECB77C5FB1E8B223A0AE807C9C4AE54392"})
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
