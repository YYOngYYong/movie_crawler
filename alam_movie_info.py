from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import telegram   #텔레그램 모듈을 가져옵니다.
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.movieAlarm

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.

bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.


##디비에 내가 알림받기 선택한 영화 타이틀들을 조회하여 개봉된 영화와 대조.

def movie_info():
    di = list(db.my_released.find())
    all_movie = list(db.releasedMovies.find({},{'_id':0}))
    movie_piked = ''
    for i in di:
        movie_piked = i['title']
    # 텔레그램에 뿌려줄 문자열 생성
    result = ''
    for i in all_movie:
        ##만약 타이틀이 내가 알림받기한 타이틀과 같다면
        if movie_piked == i['title']:
            print('제목',i['title'])
            print('날짜',i['date'])
            ## 문자열에 제목, 타임테이블, 좌석들 문자열에 추가해준다
            result += f"제목 : {i['title']} \n 날짜 : {i['date']} \n"
            index = 0
            for j in i['timetables']:
                print('시간',j,':',i['seats'][index],'석')
                result += f" {j} : {i['seats'][index]}석 \n"
                index +=1
            print('--------------------------------------------')
            result += f"--------------------------------------- \n"
    return result

movie_info()


chat_id = '1028099025'
bot.sendMessage(chat_id=chat_id, text=movie_info())

# for i in all_movie:
#     if movie_piked == i['title']:
#         print("(날짜)"+i['date'] +"\n",i['timetables'],i['seats'])
#         print('-----------------------------------------------')
