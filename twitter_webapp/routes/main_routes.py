from flask import Blueprint, render_template, request
from twitter_webapp.models import db, User, Tweet, compare_user

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
    user=[]
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        user = User.query.filter_by(username=result["username"]).first()

        if result["full_name"] != "":
            user.full_name = result["full_name"]
            user.location = result["location"]  
            db.session.commit()
    
    return render_template("user_update.html", data=user)


# /compare : 유저간 트윗 분석 페이지
@main_routes.route('/compare')
def compare():
    result=[]
    if request.method == "POST":
        result = compare_user(user1, user2, word)
    return render_template("compare.html", data=result)
