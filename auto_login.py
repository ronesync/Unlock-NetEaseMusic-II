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
    browser.add_cookie({"name": "MUSIC_U", "value": "006FD88CB0CBD6069136C1676731B45BB4488F90B3B635816CC344A33C0E420BFE97A548E691C57E55D80FBE256FFC235F963321DEF618709CE090AD513FD8609A37797CCCAAAEB52DB9056C42E82C3AD68B84CCB7326FAC7BED06EBE3B889F5FC07E175FC40EBD88FF3091AACBDA9C0B3B0524A50988478E7C95B745F2CE4166ACC37DB1FD9054DB74CA97553882FC09A82A46BF503524EB97A2CA46A866A689267904FB740244FAFB8C3BC2481C230508CF5A0B641EAF626528515FA5EABF2F8007038E2B6C6F39661978AE107A3307F54B18962B31FF909B90DF31ED30B0CD3415E995C6D1D78757062B08DC53E815C9A57563D0441F2B71E4E17A07B6812C3BCFF5A898B4F4532BCE05BC3484274D6CFAFBC5F460A55EA241D57C0964ABE903F9A0834B97120222BF4F1AAA2C33D15BDE8A11B973EADEED67EF84F846C2A9D7D88A9F00AC7AAA749EFB7B856ED4A78B4058AD7B690ED2C6D8BA2AC4BE7D45EC5027C29F3C4DD39E93B533176EA00A6C48144A7E64B55322ACE74753915E8CE6B4504CE1F92983CBD3CE2D78CAF8F0324710A35861D97B6EA1149C53D1AA3E8"})
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
