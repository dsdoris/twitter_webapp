from flask import Blueprint, render_template, jsonify
from twitter_webapp.models import User, Tweet

main_routes = Blueprint('main_routes', __name__)

# / : 인덱스 페이지
@main_routes.route('/')
def index():
    return render_template("index.html")


# /users : 유저들 조회하는 페이지
@main_routes.route('/users')
def users():
    data = User.query.all()
    print(data)
    return render_template("users.html", data=data)


# /update: 유저 업데이트(수정) 페이지
@main_routes.route('/update')
def update():
    
    return render_template("user_update.html")


# /compare : 유저간 트윗 분석 페이지
@main_routes.route('/compare')
def compare():
    
    return render_template("compare.html")


# @main_routes.route('/user.json')
# def json_data():
#     raw_data = get_data()
#     parsed_data = parse_records(raw_data)
    
#     return jsonify(parsed_data)