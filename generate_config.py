import os
import textwrap

def generate_config(dir, filename):
    filepath = os.path.join(dir, filename)
    print(f"Generating config file in {filepath}")
    if os.path.isfile(filepath):
        print("ERROR", "File already exists. Aborting")
        return
    
    f = open(filepath, "w")
    f.write(textwrap.dedent("""\
        {
            "general": {
                "chromedriver_path": "./chromedriver",
                "pool_size": 10,
                "session_renew": 50,
                "delay_sec": 1,
                "sugang_url": "http://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action",
                "lecinfo_url": "http://my.knu.ac.kr/stpo/stpo/cour/lectReqCntEnq/list.action"
            },
            "login": {
                "snum": "2000000000",
                "id": "yes_id",
                "passwd": "yes_passwd"
            },
            "request": {
                "year_term": "20001",
                "lectures": ["COMP101001", "COMP201001", "COMP301001"]
            }
        }
        """))
    f.close()
    print("INFO", "Config file successfully generated")
    return
