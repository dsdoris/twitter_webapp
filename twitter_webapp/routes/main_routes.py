from flask import Blueprint, render_template, request
from twitter_webapp.models import db, User, Tweet, compare_user, set_tweetdata

main_routes = Blueprint('main_routes', __name__)

# / : 인덱스 페이지
@main_routes.route('/')
def index():
    # User 데이터 기준으로 Tweet 데이터 세팅
    print("Setting Tweet data...")
    settweetdata = set_tweetdata()
    if settweetdata != []:
        print("Set Tweet data.")

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
        print("@main_route, /update",dict(request.form))
        result = request.form
        user = User.query.filter_by(username=result["username"]).first()

        if result["full_name"] != "":
            user.full_name = result["full_name"]
            if result["location"] != "":
                user.location = result["location"]

            db.session.commit()
    
    return render_template("user_update.html", data=user)


# /compare : 유저간 트윗 분석 페이지
@main_routes.route('/compare')
def compare():
    compare_result=[]
    if request.method == "POST":
        compare_result = compare_user(result["username1"], result["username2"], result["text"])
    return render_template("compare.html", data=compare_result)
