import os
import time
import json
import random

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    Warning("Selenium not installed. Please install it using 'pip install selenium'")

import tools.web.configs as cfg
from setting import USER_DATA_DIR

driver = None

def init_driver():
    global driver
    if driver is not None:
        return
    
    chrome_options = Options()
    if USER_DATA_DIR:
        chrome_options.add_argument(f"user-data-dir={USER_DATA_DIR}")
        driver = webdriver.Chrome(options=chrome_options)

def close_driver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None

def google_scholar_get(kwd: str):
    init_driver()
    driver.minimize_window()
    
    driver.get(cfg.GOOGLE_SCHOLAR_HM_URL)
    
    try:
        element_present = EC.presence_of_element_located((By.NAME, 'q'))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Page Loading Timeout: {e}")
    
    search_box = driver.find_element(By.NAME, 'q')
    search_box.clear()
    search_box.send_keys(kwd)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)
    
    page_source = driver.page_source
    close_driver()
    return page_source

def google_login():
    if not USER_DATA_DIR:
        raise Exception("No user data found")
    init_driver()
    driver.maximize_window()
    driver.get("https://accounts.google.com/")
    with open("abc.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    wait = WebDriverWait(driver, 10)


    login_flag = False
    account_name = None
    while True:
        if driver.window_handles:
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/header/div[2]/div[3]/div[1]/div[2]/div/a")))
                account_name = element.get_attribute("aria-label")
                account_name = account_name.split("\n")[-1].strip("()")
                login_flag = True
                print(f"Login as {account_name}")
                break
            except Exception as e:
                login_flag = False
            time.sleep(1)
        else:
            break
    
    close_driver()
    return login_flag, account_name


def wos_login():
    init_driver()
    driver.minimize_window()
    driver.get(cfg.WOS_HM_URL)
    time.sleep(5)
    
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "/html/body/app-wos/main/div/div/div[1]/app-header/div[1]/header/div[2]/div[1]/a"))
        WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print(f"Page Loading Timeout: {e}")

    cookies = driver.get_cookies()
    sid = next((cookie['value'] for cookie in cookies if cookie['name'] == 'SID'), None)
    wossid = next((cookie['value'] for cookie in cookies if cookie['name'] == 'WOSSID'), None)
    print(f"SID: {sid}")
    print(f"WOSSID: {wossid}")

    close_driver()
    return sid, wossid