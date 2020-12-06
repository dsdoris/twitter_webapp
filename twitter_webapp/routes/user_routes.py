from flask import Blueprint, render_template, request
from twitter_webapp.models import db, User, Tweet, get_userdata, set_tweetdata, compare_user, update_userdata
from twitter_webapp.services import twitter_api
import tweepy


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=["GET", "POST"])
def index(username):
    compare_result=[]
    if request.method == "POST":
        result = request.form
        # compare page에서 넘어온 경우
        if username == "compare":
            print("@user_route, /compare", dict(request.form))
            compare_result = compare_user(result["username1"], result["username2"], result["text"])
            print("compare_result:", compare_result)
            return render_template('compare.html', data=compare_result)
        # update page에서 넘어온 경우
        elif username == "update":
            print("@user_route, /update",dict(request.form))
            result = request.form
            user = User.query.filter_by(username=result["username"]).first()
            if "full_name" in result:
                User.query.filter_by(username=result["username"]).update({'full_name': result["full_name"], 'location': result["location"]})
                user = db.session.commit()
            return render_template('user_update.html', data=user)      

    return render_template('user_get.html', data=username)

# /{트위터 유저이름}/add : 유저 추가 페이지
@user_routes.route("/add", methods=["GET", "POST"])
def add(username):
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        user = twitter_api.api.get_user(screen_name=result["username"])

        db.session.add(User(id = user.id,
                            username = result["username"], #null chk, unique chk
                            full_name = user.name, #null chk
                            followers = user.followers_count,
                            location = user.location))

        db.session.commit()
    return render_template('user_add.html', username=username)


# /{트위터 유저이름}/delete : 유저 삭제 페이지
@user_routes.route("/delete", methods=["GET", "POST"])
def delete(username):
    if username != "{username}":
        data = User.query.filter(User.username == username).all()
    else:
        data = username

    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        user  = User.query.filter_by(username=result["username"]).first()

        db.session.delete(user)
        db.session.commit()

        data = User.query.filter(User.username == username).all()
    return render_template('user_delete.html', data=data)


# /{트위터 유저이름}/get : 트윗 조회 페이지
@user_routes.route("/get", methods=["GET", "POST"])
def get(username):
    if username != "{username}":
        data = Tweet.query.filter_by(user_id=User.query.filter_by(username=username).first().id).all()
    else:
        username = ""
        data = ""

    if request.method == "POST":
        print(dict(request.form))
        username = request.form["username"]
        data = Tweet.query.filter_by(user_id=User.query.filter_by(username=username).first().id).all()

    return render_template('user_get.html', data=[username, data])