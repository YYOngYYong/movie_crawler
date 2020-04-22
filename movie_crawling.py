import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
# db = client.MWG
# 타겟 URL을 읽어서 HTML를 받아오고,

client = MongoClient('localhost', 27017)
db = client.movieAlarm
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 크롤링하기 전에 기존 데이터를 모두 삭제
db.movies.delete_many({})

comming_movies = requests.get('http://www.cgv.co.kr/movies/pre-movies.aspx')
#formresult > div > div > div.vignetteListeCollection145 > a > img
soup = BeautifulSoup(comming_movies.text, 'html.parser')

#formresult > div > div:
# img_urls = soup.select('#formresult > div > div > div.vignetteListeCollection145')
# #formresult > div > div > div.mosaiqueCttCollection145 > a > div.txt2 > span
# titles = soup.select('#formresult > div > div > div.mosaiqueCttCollection145 > a > div.txt2')  #css 셀렉터 생각하면 된다. 이 위치의 모든 tr 태그들을 for문 돌릴 수있음
# artists = soup.select('#formresult > div > div > div.mosaiqueCttCollection145 > a > div.txt1')
#formresult > div > div > div.mosaiqueCttCollection145 > a > div.txt1 > span
#############################
# movies (tr들) 의 반복문을 돌리기
#formresult > div > div

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









# for artist in artists:
#     a_artist = artist.select_one('span')
#     if a_tag is not None:
#         # a의 text를 찍어본다
#         print(a_artist.text)
##contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(1) > div.box-contents > a > strong
#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(4) > li:nth-child(1) > div.box-contents > a > strong



#movie_more_container > li:nth-child(34) > div.box-contents > a > strong