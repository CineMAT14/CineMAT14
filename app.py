from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.3dhal.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SECRET_KEY = 'SPARTA'

# DB에서 저장된 단어 찾아서 HTML에 나타내기
@app.route('/')
def home():
    return render_template('/login.html')

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

# 로그인 성공 시, 토큰 전달
@app.route('/')
def give_token():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.cine_users.find_one({"username": payload["id"]})
        return render_template('login.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.cine_users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24) # 로그인 24시간 유지
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8') / python 버전 3 이상부터 decode 적용 불가
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "profile_name": username_receive,
    }
    db.cine_users.insert_one(doc)
    return jsonify({'result': 'success'})

# 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.cine_users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)