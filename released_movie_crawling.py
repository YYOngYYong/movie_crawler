import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

date_crawl_og = datetime.now()
date_crawl = date_crawl_og.strftime("%Y%m%d")

# while 돌리기. i = 1일째부터 14일후의 날까지.
# i = 1
# while i < 14:
data = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date=20200421&screencodes=&screenratingcode=02&regioncode=07', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, 영들을 불러오기
movies = soup.select('.showtimes-wrap > .sect-showtimes > ul > li')

id = 1
# movies (li들) 의 반복문을 돌리기
for movie in movies:
    # movie 안에 a 가 있으면,
    a_tag = movie.select_one('.col-times > div.info-movie > a > strong')
    print(a_tag.text.strip())
    # 영화 제목/시간표/잔여석 가져오기
    if a_tag is not None:
        title = a_tag.text.strip()
        timetable_original = movie.select('.col-times > .type-hall > div.info-timetable > ul > li > a > em')
        left_seats = movie.select('.col-times > .type-hall > div.info-timetable > ul > li > a > span')

        timetables = []
        for timetable in timetable_original:
            timetables.append(timetable.text)
        seats = []
        for seat in left_seats:
            seats.append(seat.text)

        doc = {
            '_id': id,
            'title': title,
            'date': str(date_crawl),
            'timetable': timetables,
            'left_seats': seats
        }
        #db.movies.insert_one(doc)
        print(doc)
        id += 1

    date_crawl_og = date_crawl_og + timedelta(1)
