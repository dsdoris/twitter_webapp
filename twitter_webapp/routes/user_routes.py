from flask import Blueprint, render_template, request
from twitter_webapp.models import db, User, Tweet, get_userdata, set_tweetdata
from twitter_webapp.services import twitter_api
import tweepy


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=["GET", "POST"])
def index(username):
    return render_template('user_get.html', data=username)

# /{트위터 유저이름}/add : 유저 추가 페이지
@user_routes.route("/add", methods=["GET", "POST"])
def add(username):
    if request.method == "POST":
        print(dict(request.form))
        result = request.form

        db.session.add(User(username = result["username"], #null chk, unique chk
                            full_name = result["full_name"], #null chk
                            followers = result["followers"],
                            location = result["location"]))

        db.session.commit()
    return render_template('user_add.html', username=username)


# /{트위터 유저이름}/delete : 유저 삭제 페이지
@user_routes.route("/delete", methods=["GET", "POST"])
def delete(username):
    data = User.query.filter(User.username == username).all()
    print(data)
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
    #data=set_tweetdata()

    # public_tweets = twitter_api.api.user_timeline("Dorisoh3")
    # for tweet in public_tweets:
    #     print(tweet.text)

    raw_tweets = twitter_api.api.user_timeline(screen_name=username, count=10, include_rts=False, exclude_replies=True, tweet_mode="extended")


    return render_template('user_get.html', data=raw_tweets)