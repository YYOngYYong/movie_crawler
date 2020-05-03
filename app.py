from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import telegram   #텔레그램 모듈을 가져옵니다.


from released_movie_crawling import get_released_movie

from movie_crawling import not_released_movie_crawler


app = Flask(__name__)

client = MongoClient('mongodb://test:test@54.180.8.158', 27017)
db = client.movieAlarm

my_token = '1065194618:AAGIa44CxcEYsNSPmA2Ouwyqo0Zmba1eLSs'   #토큰을 변수에 저장합니다.

bot = telegram.Bot(token=my_token)   #bot을 선언합니다.


# HTML을 주는 부분
@app.route('/')
def home():
    get_released_movie()
    not_released_movie_crawler()

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

    db.mymovie_not_released.insert_one(doc)
    return jsonify({'result': 'success','message': '성공'})


@app.route('/released_movie', methods=['GET'])
def insert_released():
    title_receive = request.args.get('title')

    doc = {
        'title': title_receive
    }

    db.my_released.insert_one(doc)
    return jsonify({'result': 'success', 'message': '성공'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

