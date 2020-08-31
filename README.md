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

## Contributing
well...