from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.movieAlarm


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# 클라이언트에서 GET 요청한 url에 따라 개봉영화 리스트 조회
# 개봉예정 영화
@app.route('/not_released', methods=['GET'])
def movie_not_released():
    not_released = list(db.movies.find({},{'_id':False}).sort("title",1))
    return jsonify({'result': 'success','not_released': not_released})
# 개봉 영화
@app.route('/released', methods=['GET'])
def movie_released():
    released = list(db.releasedMovies.find({}, {'_id': False}).sort("title", 1))
    return jsonify({'result': 'success','released': released})

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




if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)