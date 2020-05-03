from pymongo import MongoClient
import telegram

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.
bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

client = MongoClient('mongodb://test:test@54.180.8.158', 27017)
db = client.movieAlarm
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# 미개봉작 타이를 저장목록 불러와서 배열
d_array = []
my_not_released = list(db.mymovie_not_released.find({},{'_id':0}))
for my_movie in my_not_released:
    d_array.append(my_movie['title'])

# movies에서 타이틀과 디데이를 가져옴
not_released = list(db.movies.find({'d_day': {'$regex':'\w'}},{'_id':False}).sort('d_day',-1))

# d_array 를 돌면서 not_released의 'title'과 동일하고 개봉까지 남은 날이 D-1이면 새 배열에 저장함
alarm_list = ''
for my_movie in d_array:
    for movie in not_released:
        if movie['title'] == my_movie and movie['d_day'] == 'D-1':
            alarm_list = alarm_list + f"\n - {movie['title']}"
alarm_msg = f"D-0! 오늘 개봉하는 영화 {alarm_list}"

if alarm_list != '':
    # 챗봇으로 오픈일 알려줌
    chat_id = '1028099025'
    bot.sendMessage(chat_id=chat_id, text=alarm_msg)