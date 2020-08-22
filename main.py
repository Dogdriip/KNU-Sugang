from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from multiprocessing import Pool, freeze_support
import os
import signal
import time
import json


# DEBUG INFO WARNING ERROR CRITICAL


### Load config
try:
    CONFIG = json.load(open("./config.json", "r"))
except:
    print("ERROR", "Cannot open 'config.json'")
    exit()
print("VERBOSE", "Config loaded")


def loginSugang(browser, snum, id, passwd):
    ## Login
    browser.get(CONFIG["general"]["sugang_url"])
    e = browser.find_element_by_id("user.stu_nbr")
    e.send_keys(snum)
    e = browser.find_element_by_id("user.usr_id")
    e.send_keys(id)
    e = browser.find_element_by_id("user.passwd")
    e.send_keys(passwd)
    e = browser.find_element_by_class_name("login")
    e.click()

    ## Check if alert is present (which means login failure)
    try:
        WebDriverWait(browser, 0).until(expected_conditions.alert_is_present())
        alert = browser.switch_to.alert
        print("ERROR", "Login failure:", alert.text)
        alert.accept()
        return False
    except TimeoutException:
        print("INFO", "Login succeed")
        return True


def getLecInfo(lecCode):
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=1000))
    response = session.post(CONFIG["general"]["lecinfo_url"], data={
        "lectReqCntEnq.search_open_yr_trm": CONFIG["year_term"],
        "lectReqCntEnq.search_subj_cde": lecCode[0:7],
        "lectReqCntEnq.search_sub_class_cde": lecCode[7:],
        "searchValue": lecCode
    })
    # soup = BeautifulSoup(response.text, "html.parser")
    soup = BeautifulSoup(response.text, "lxml")
    res = {
        "subj_class_cde": soup.find("td", class_="subj_class_cde").text,
        "subj_nm": soup.find("td", class_="subj_nm").text,
        "unit": int(soup.find("td", class_="unit").text),
        "prof_nm": soup.find("td", class_="prof_nm").text,
        "lect_quota": int(soup.find("td", class_="lect_quota").text),
        "lect_req_cnt": int(soup.find("td", class_="lect_req_cnt").text),
    }
    return res


def initializer():
    # Ignore SIGINT in child workers
    signal.signal(signal.SIGINT, signal.SIG_IGN)


if __name__ == "__main__":
    try:
        ### Configure multiprocess pool, chromedriver
        freeze_support()
        pool = Pool(processes=CONFIG["general"]["pool_size"], initializer=initializer)
        browser = webdriver.Chrome(CONFIG["general"]["chromedriver_path"])

        ### Login to sugang
        if not loginSugang(browser, **CONFIG["login"]):
            raise Exception("LoginFailureException")

        ### Main loop
        while True:
            ## Check remaining session time
            session_renew = CONFIG["general"]["session_renew"]  # remaining sec threshold
            try:
                e = browser.find_element_by_id("timeStatus")
                remain_sec = int(e.text.split("초")[0])
            except:
                remain_sec = 1200  # Initially it does not exist
                pass
            
            if remain_sec < session_renew:
                # Renew
                print("INFO", "Login renewing...")
                e = browser.find_element_by_class_name("stop")
                e.click()
                if not loginSugang(browser, **CONFIG["login"]):
                    raise Exception("LoginFailureException")
                
            print("VERBOSE", f"Remain {remain_sec}sec")
            
            ## Main logic
            regTable = browser.find_element_by_css_selector("#onlineLectReqGrid > div.data > table > tbody")
            packTable = browser.find_element_by_css_selector("#lectPackReqGrid > div.data > table > tbody")
            
            r = pool.map(getLecInfo, CONFIG["request"]["lectures"])
            # print(r)



            """
            r.append({
                "subj_class_cde": "",
                "subj_nm": "Asdf",
                "unit": 3,
                "prof_nm": "sdf",
                "lect_quota": 80,
                "lect_req_cnt": 30,
            })
            """


            for lecInfo in r:
                print("VERBOSE", f"{lecInfo['subj_class_cde']}: r{lecInfo['lect_req_cnt']}, q{lecInfo['lect_quota']}")

                # If available (req_cnt < quota), find lecture in packTable
                if lecInfo["lect_req_cnt"] < lecInfo["lect_quota"]:
                    # Check if it's already registered
                    already = False
                    for tr in regTable.find_elements_by_tag_name("tr"):
                        td = tr.find_elements_by_tag_name("td")
                        if td and td[1].text == lecInfo["subj_class_cde"]:
                            print("WARNING", f"{lecInfo['subj_class_cde']}: Already registered")
                            already = True
                            break
                    if already:
                        continue

                    succeed = False
                    for tr in packTable.find_elements_by_tag_name("tr"):
                        td = tr.find_elements_by_tag_name("td")
                        if td and td[0].text == lecInfo["subj_class_cde"]:
                            try:
                                td[10].click()
                                WebDriverWait(browser, 0).until(expected_conditions.alert_is_present())
                                alert = browser.switch_to.alert
                                print("INFO", f"{lecInfo['subj_class_cde']}: {alert.text}")
                                alert.accept()
                                succeed = True
                            except TimeoutException:
                                print("INFO", "no alert")
                    if not succeed:
                        print("ERROR", "Not found in packTable")
                else:
                    continue
            time.sleep(CONFIG["general"]["delay_sec"])

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print(" ".join(e.args))
    finally:
        print("Terminating")
        pool.terminate()
        pool.join()
        browser.close()
        exit()
