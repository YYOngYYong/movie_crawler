# A.일1회: 내가 저장한 영화가 그날 신규 크롤링된 개봉예정작 목록에 있으면,
# 나의 텔레그램 아이디로 영화명과 D-day를 알려줌
import requests
from pymongo import MongoClient
import telegram
import re

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.
bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

client = MongoClient('localhost', 27017)
db = client.movieAlarm
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# A1.크롤링을 모두 갱신하기 전에 내가 저장한 영화 정보가 어제 크롤링 목록에 D-1이면 보내줌.
def alarm_d_0() :
    # 미개봉작 타이를 저장목록 불러와서 배열
    my_not_released = list(db.mymovie_not_released.find({},{'_id':0}))
    d_0_array = []
    for my_movie in my_not_released:
        d_0_array.append(my_movie['title'])

    # movies에서 타이틀과 디데이를 가져옴
    not_released = list(db.movies.find({'d_day': {'$regex':'\w'}},{'_id':False}).sort('d_day',-1))

    # d_0_array 를 돌면서 not_released의 'title'과 동일하고 개봉까지 남은 날이 D-1이면 새 배열에 저장함
    alarm_msg = ''
    for my_movie in d_0_array:
        for movie in not_released:
            if movie['title'] == my_movie and movie['d_day'] == 'D-11': # 테스트를 위해 임의로 D-11로 설정. 실제 서비스에선 D-1
                alarm_msg = alarm_msg + f"\n - {movie['title']} "
    alarm_msg = f"D-0! 오늘 개봉하는 영화 {alarm_msg}"
    print(alarm_msg)
    # 챗봇으로 오픈일 알려줌
    chat_id = '1204783894'
    bot.sendMessage(chat_id=chat_id, text=alarm_msg)


# A2. 일별 신규 크롤링을 마친 뒤에 D-day 알림 보내줌.
def alarm_d_waiting() :
    # 미개봉작 타이를 저장목록 불러와서 배열
    my_not_released = list(db.mymovie_not_released.find({},{'_id':0}))
    d_array = []
    for my_movie in my_not_released:
        d_array.append(my_movie['title'])

    # movies에서 타이틀과 디데이를 가져옴
    not_released = list(db.movies.find({'d_day': {'$regex':'\w'}},{'_id':False}).sort('d_day',-1))

    # not_released의 'title'과 동일하면 새 배열에 저장함
    alarm_msg = ''
    for movie in not_released:
        for my_movie in d_array:
            if movie['title'] == my_movie:
                alarm_msg = alarm_msg + f"\n - {movie['title']}, {movie['d_day']} "
    alarm_msg = f"개봉을 기다리는 영화 {alarm_msg}"

    print(alarm_msg)
    # 챗봇으로 오픈일 알려줌
    chat_id = '1028099025'
    bot.sendMessage(chat_id=chat_id, text=alarm_msg)

