from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import certifi
ca = certifi.where()
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.3dhal.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# DB에서 저장된 단어 찾아서 HTML에 나타내기
@app.route('/')
def home():
    return render_template('/review.html')

# 극장 정보 GET API
@app.route("/main/cinema", methods=["GET"])
def cinema():
    cinema_list = list(db.cinema.find({}, {'_id': False}))
    return jsonify({'cinema':cinema_list})

# review 저장하기 API
@app.route("/review", methods=["POST"])
def review_save():
    store_receive = request.form['store_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    distance_receive = request.form['distance_give']
    waiting_receive = request.form['waiting_give']
    taste_receive = request.form['taste_give']

    review_list = list(db.review.find({},{'_id': False}))
    count = len(review_list) + 1

    doc = {
        'num': count,
        'store':store_receive,
        'star':star_receive,
        'comment':comment_receive,
        'distance':distance_receive,
        'waiting':waiting_receive,
        'taste':taste_receive
    }
    db.review.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


# review 삭제하기 API
@app.route("/review/delete", methods=["POST"])
def review_delete():
    num_receive = request.form['num_give']
    db.review.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})


# reveiw 목록 보여주기 API
@app.route("/review", methods=["GET"])
def review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    print(review_list)
    return jsonify({'reviews': review_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)