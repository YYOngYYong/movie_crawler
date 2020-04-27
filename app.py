from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import telegram   #텔레그램 모듈을 가져옵니다.
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.movieAlarm

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.

bot = telegram.Bot(token=my_token)   #bot을 선언합니다.

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

for u in updates:   # 내역중 메세지를 출력합니다.
    print(u.message)

# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# 개봉 영화

@app.route('/<movietype>', methods=['GET'])
def movie_released(movietype):
    # movietype에 따라 불러올 collection을 지정함
    dbcollection = db.movies if movietype == 'not_released' else db.releasedMovies
    movies_list = list(dbcollection.find({}, {'_id': False}))
    # movies의 각 제목만 반복문으로 빈 배열에 하나씩 넣음
    titles_array = []
    i = 0
    for movie in movies_list:
        titles_array.append(movie['title'])
        i += 1
    # 중복제거를 위해 set
    titles = list(set(titles_array))
    titles.sort()
    return jsonify({'result': 'success', f'{movietype}': titles})






@app.route('/request_title', methods=['GET'])
def request_title():
    title_receive = request.args.get('title')
    movie_info = list(db.movies.find({'title': title_receive}, {'_id': False}))
    print(movie_info)
    chat_id = '1028099025'
    bot.sendMessage(chat_id=chat_id, text=movie_info[0]['title']+"\n"+movie_info[0]['d_day'])
    return jsonify({'result': 'success','released': movie_info[0]})


@app.route('/not_released_movie', methods=['GET'])
def insert_not_released():
    title_receive = request.args.get('title')

    doc = {

        'title':title_receive
    }

    db.my_not_released.insert_one(doc)
    return jsonify({'result': 'success','message': 'ㅎ헤ㅔ헤'})


@app.route('/released_movie', methods=['GET'])
def insert_released():
    title_receive = request.args.get('title')

    doc = {
        'title': title_receive
    }

    db.my_released.insert_one(doc)
    return jsonify({'result': 'success', 'message': '성공'})




#
#
# @app.route('/api/like', methods=['GET'])
# def counting_list():
#     # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
#     # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
#     # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
#     # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
#     # 참고: '$set' 활용하기!
#     # 5. 성공하면 success 메시지를 반환합니다.
# 	return jsonify({'result': 'success','msg':'like 연결되었습니다!'})

chat_id = '1028099025'




if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)

