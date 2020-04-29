import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import re

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)


client = MongoClient('mongodb://test:test@54.180.8.158', 27017)
db = client.movieAlarm


def get_released_movie():
    # 크롤링하기 전에 기존 데이터를 모두 삭제
    db.releasedMovies.delete_many({})

    # URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    date_now = datetime.now()
    date_str = date_now.strftime("%Y%m%d")

    # while 돌리기. i = 1일째부터 14일후의 날까지.
    i = 1
    id = 1

    while i < 14:
        data = requests.get(
            f'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date={date_str}&screencodes=&screenratingcode=02&regioncode=07',
            headers=headers)

        # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
        soup = BeautifulSoup(data.text, 'html.parser')

        # select를 이용해서, 영들을 불러오기
        movies = soup.select('.showtimes-wrap > .sect-showtimes > ul > li')

        # movies (li들) 의 반복문을 돌리기
        for movie in movies:
            # movie 안에 a 가 있으면,
            a_tag = movie.select_one('.col-times > div.info-movie > a > strong')
            # 영화 제목/시간표/잔여석 가져오기
            if a_tag is not None:
                title = a_tag.text.strip()
                timetable_og = movie.select('.col-times > .type-hall > div.info-timetable > ul > li > a > em')
                seats_og = movie.select('.col-times > .type-hall > div.info-timetable > ul > li > a > span')

                timetables = []
                for timetable in timetable_og:
                    timetables.append(timetable.text)
                if timetables == []:
                    timetables.append('마감')

                seats = []
                for seat in seats_og:
                    seat = seat.text
                    seat = int(re.findall("\d+", seat)[0])
                    seats.append(seat)
                if seats == []:
                    seats.append('마감')

                doc = {
                    '_id': id,
                    'title': title,
                    'date': str(date_str),
                    'timetables': timetables,
                    'seats': seats
                }
                db.releasedMovies.insert_one(doc)
                id += 1
                print(doc)

        # datetime으로 선언된 변수는 덮어쓰기가 안됨. 새로운 변수에 추가된 값을 넣고 원본 변수는 값을 다 지운다음에 새로운 변수값을 넣어줘야함
        date_add_day = date_now + timedelta(1)
        date_now = ''
        date_now = date_add_day
        date_str = date_now.strftime("%Y%m%d")
        i += 1



