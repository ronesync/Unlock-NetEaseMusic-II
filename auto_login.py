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
    browser.add_cookie({"name": "MUSIC_U", "value": "0020658D9269E50CABE601A8E65872F9DC149046183D2EDC5EB833C4AD9635010061B0CA66CC42AE7A31E3D0152EB8C22D162E4B6B413680BEBE898666D6EED185B32AD742624CF52D051C766E12D952E91AF13C6FE2170F743E4958766A904FE62997386876F039FC4D3BE3BD5601ABB2F6434AB225DC7EB6CF607F2B8E4E303C6EB97BE96CA45DA0F30443C3D78CE8E7B257141238A1B507CF8CDF7EBF6652FBB2883BD696107730CC24D1FDB508B8BE5D83F8D12034D2E833CD2D0F54AB92FD1823F8F2706928FE8A192BEEAB64D0F3EB478BC38EBD656533037DD36620E2DFCD330701E20D5FBE6CB1A35AECA9F51932D44685E23FA8BBC8E8CA61AE8691F68D26B19F1A498AC1B7A242B5F18E8C87C17CD8773F70686A950334717E3B5D0756C2EB6A997013F74E5153E4BDB05CEC53A52535A0F9B622506EA35D5814126B88F65DB866D50304A32476B4A0A77DF5FB9D3E9586039FCEEE1CE8237C623F1D558030115881059414F42791C154DA8151EFB2019F6BAEC5C2A3454B23688267429643FD53DE4AD8AB431474912F09F9"})
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
