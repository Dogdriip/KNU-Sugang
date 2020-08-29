# KNU-Sugang

경북대학교 수강신청 자동화

## 기능
- 수꾸 터진 과목들 빠르게 수강신청
  - 수꾸에 없는 건 안됨
- 수강인원 체크해서 빈자리 나면 들어가기

## 특징
- 멀티스레드(`multiprocessing.Pool`) 이용한 빠른 다중과목 대응
- lxml 이용한 빠른 파싱

## 메모

```
pipenv --python 3.8
pipenv shell
pip install -r .\requirements.txt
python main.py
```

## Sample config.json
```json
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
```