#-*- coding:utf-8 -*-
# A2. 일별 신규 크롤링을 마친 뒤에 D-day 알림 보내줌.

from pymongo import MongoClient
import telegram

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.
bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.movieAlarm
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# 미개봉작 타이를 저장목록 불러와서 배열
d_array = []
my_not_released = list(db.mymovie_not_released.find({},{'_id':0}))
for my_movie in my_not_released:
    d_array.append(my_movie['title'])
# movies에서 타이틀과 디데이를 가져옴
not_released = list(db.movies.find({'d_day': {'$regex':'\w'}},{'_id':False}).sort('d_day',-1))

# not_released의 'title'과 동일하면 새 배열에 저장함
alarm_list = ''
for my_movie in d_array:
    for movie in not_released:
        if movie['title'] == my_movie:
            alarm_list = alarm_list + f"\n - {movie['title']}, {movie['d_day']} "
alarm_msg = f"개봉을 기다리는 영화 {alarm_list}"

if alarm_list != '':
    # 챗봇으로 오픈일 알려줌
    chat_id = '1204783894'
    bot.sendMessage(chat_id=chat_id, text=alarm_msg)