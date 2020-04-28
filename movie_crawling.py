#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# from alarm_Dday import alarm_d_0, alarm_d_waiting

# client = MongoClient('localhost', 27017)
# db = client.MWG
# 타겟 URL을 읽어서 HTML를 받아오고,
def not_released_movie_crawler():
    # 크롤링하기 전에 기존 데이터를 모두 삭제
    db.movies.delete_many({})

    comming_movies = requests.get('http://www.cgv.co.kr/movies/pre-movies.aspx')
    soup = BeautifulSoup(comming_movies.text, 'html.parser')

    movie_box = soup.select('#contents > div.wrap-movie-chart > div.sect-movie-chart > ol > li > div.box-contents')
    movie_titles = soup.select('#contents > div.wrap-movie-chart > div.sect-movie-chart > ol > li > div.box-contents ')
    d_day = soup.select('#contents > div.wrap-movie-chart > div.sect-movie-chart > ol > li > div.box-contents')


    # 중복없이 상영 예정작들 크롤링
    pre_movies = []
    d_day = []
    check = 1
    for movies in movie_box:
        title = movies.select_one('a > strong')
        dday = movies.select_one('span.txt-info > strong > em')
        if title is not None:
            pre_movies.append(title.text)
        if dday is not None:
            d_day.append(dday.text)
        if dday is None:
            d_day.append("개봉예정")
    ##tt

    # for i in pre_movies:
    #
    #     if check >= 4:
    #         print(i)
    #     check += 1
    # num = 1
    # for i in d_day:
    #     if num >= 4:
    #         print(i)
    #     num += 1

    id_num = 1

    n = 1
    for i in range(len(pre_movies)):
        if n >= 4:
            doc = {
                '_id': id_num,
                'title': pre_movies[i],
                'd_day': d_day[i]
            }
            db.movies.insert_one(doc)
            id_num += 1
        n += 1

    # 크롤링 끝난 후 알림 발송!
    # larm_d_waiting()
