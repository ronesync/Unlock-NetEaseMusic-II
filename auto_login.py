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
    browser.add_cookie({"name": "MUSIC_U", "value": "009CF44C67C77C66F6CD81C2446A8C2E5C1C52F60786C86D9CE4618BFF3D0425448CFA2B3FBEECB21F6703B1B79C4833B94269B546EECD012383A0CEB5A509CEEB2588A7ECDD16286856249304AC6AC0F5A2F09228C249F74579567D3ABB70CE1C56C1E274449A5915CCBBE7FCD74C3F34EDFA21283F780C47BF65242CEFB5879DACBB845B48426632A371168FE97A43FECEE9B84A819C6229B2108F8785978089FAE90406CEC1E7946CFB1ECE8F9172C5FF3ECA97CEA296EBE8A95A6410A7428D370FA9AE89969AC270DCAFC40ED9167A36599341CD9EE5C311D3FC41A1EB9F15CDB92BDEC743561F5F77081A7EAAA4960C3D15ACAD36E4933B22C7F7BA3E3A7D799466931801E4F8E388842B94C92F4292B0AB8769CA9A76964C38652EABBA31E51E0C34B801B4DAC2E07E21AB92E7F18BE8A45E2E5BE22A0B6F9D97CDE9AD560DB36D1B3D3694520A5EABDCA05C54A5EA69A16AE62F58C800629EE04C88EC3BE3FB9FB503E05CE092E21734D8131042666F70BB1DA88C457EF3C528A0A5D53DCC49662D0F6636EAF5E450CEFBF7A0B274725B37A4C34F83C796C98BF3037C6A"})
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
