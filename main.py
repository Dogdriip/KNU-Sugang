from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import json


CONFIG_PATH = "./config.json"
CHROMEDRIVER_PATH = "./chromedriver"
SUGANG_URL = "http://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action"


def loginSugang(browser, loginConfig):
    print(loginConfig)
    browser.get(SUGANG_URL)
    



if __name__ == "__main__":
    ### Configure chromedriver
    config = json.load(open(CONFIG_PATH, "r"))
    browser = webdriver.Chrome(CHROMEDRIVER_PATH)

    ### Login to sugang
    loginSugang(browser, config["login"])
    