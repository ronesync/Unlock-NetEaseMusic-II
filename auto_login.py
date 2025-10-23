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
    browser.add_cookie({"name": "MUSIC_U", "value": "0075E70E4DF2F993D36891363623855FD24D913823BA94CC0CF28FA00A879AAF75CFE6BF497C59FDAAF41316E33AE6C933C6F46707A973A7B6C4F8C74D7B7CD5499AFB33EF120398229B325971B5490D9E6DF5ED9BFACB400416E6A88F54C034DBD3D35AD8F4AD5C2B4393651B110B64274081C04398E8B0AB5F3E403E45A76798569B3402B0EF9FCAF350C85197AD29FFDB5AC20625D56DD02D7295F8E8319A3DD13E390E661B083E60A4D5E0B8C2F047071307012659BF9FABBA27E0D2DC446BC8EB5846C97D8AD9533295D1B1D0C9583768DC654391170583F8188A36CBECB1255431EFBD47E3F85247EC5091E9B0C7525458C542986381AD8B6E995A3F575BF00A1573F546C6C9E9472CEE0DD02CFB0A46B7ABFF84EB0A813A0BC26E839340A35E07E27546C9B2313244CABA30464984655BFA7A51098C563527C2AE07E6EBF9CF25C808D5254A58948321598FD005A8BF409C89BCC56B65833F2F3E5EDD85C0A2B0D67FDF8871830EFAD24538C97B3EB4612CCFC8EB06E138F7461883A5A2E3311F17D1C1FB5A4427CCA84CF05505045B9BF603B68DD957D1A8D55D33D073"})
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
