from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time
import json


CONFIG_PATH = "./config.json"
CHROMEDRIVER_PATH = "./chromedriver"
SUGANG_URL = "http://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action"

# DEBUG INFO WARNING ERROR CRITICAL

def loginSugang(browser, snum, id, passwd):
    print(snum, id, passwd)
    ## Login
    browser.get(SUGANG_URL)
    elem = browser.find_element_by_id("user.stu_nbr")
    elem.send_keys(snum)
    elem = browser.find_element_by_id("user.usr_id")
    elem.send_keys(id)
    elem = browser.find_element_by_id("user.passwd")
    elem.send_keys(passwd)
    elem = browser.find_element_by_class_name("login")
    elem.click()

    ## Check if alert is present (which means login failure)
    try:
        WebDriverWait(browser, 0).until(expected_conditions.alert_is_present())
        alert = browser.switch_to.alert
        print("ERROR", "Login Failure:", alert.text)
        alert.accept()
        browser.close()
        exit()
    except TimeoutException:
        print("INFO", "Login Succeed")


if __name__ == "__main__":
    ### Configure chromedriver
    config = json.load(open(CONFIG_PATH, "r"))
    browser = webdriver.Chrome(CHROMEDRIVER_PATH)

    ### Login to sugang
    loginSugang(browser, **config["login"])

    


    