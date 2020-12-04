from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
from embedding_as_service_client import EmbeddingClient
from twitter_webapp.services import twitter_api
from sklearn.linear_model import LogisticRegression

db = SQLAlchemy()
migrate = Migrate()

#en = EmbeddingClient(host='54.180.124.154', port=8989)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    full_name = db.Column(db.String, nullable=False)
    followers = db.Column(db.BigInteger, default=0)
    location = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String, nullable=False)
    user = db.relationship('User',backref=db.backref('tweets', lazy=True))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    embedding = db.Column(db.PickleType)

    def __repr__(self):
        return f"<Tweet {self.id}>"

def get_userdata():
    return User.query.all()


def set_tweetdata(username):
    userid = User.query.filter_by(username=username).first().id
    user = User.query.get(userid) or User(id=userid)

    raw_tweet = twitter_api.api.user_timeline(user_id = userid, count=50, include_rts=False, exclude_replies=True, tweet_mode="extended")

    for tweet in raw_tweet:
        db.session.add(Tweet(id=tweet.id, text=tweet.full_text, user_id=userid)) #embedding 트윗 추가필요
    
    db.session.commit()
    
    return raw_tweet


def save_model(model):
    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)


def load_model():
    with open(MODEL_FILEPATH, "rb") as file:
        loaded_model = pickle.load(file)
    return loaded_mode 


def embedding_tweet(data):
    en_list = []
    for tweet in data:
        en_list.append(en.encode(texts=tweet.fulltext))

    return en_list

def append_to_with_label(to_arr, from_arr, label_arr, label):
    for item in from_arr:
        to_arr.append(item)
        label_arr.append(label)



def compare_user(user1, user2, word):
    en = EmbeddingClient(host='54.180.124.154', port=8989)
    print('Connected with server')
    print('-'*40)

    # 이용자의 트윗 불러오기
    raw_tweet1 = twitter_api.api.user_timeline(user_id = user1, tweet_mode="extended")
    raw_tweet2 = twitter_api.api.user_timeline(user_id = user2, tweet_mode="extended")

    # 텍스트를 벡터로 변경
    em_X_1 = embedding_tweet(raw_tweet1)
    em_X_2 = embedding_tweet(raw_tweet2)
    Y_1 = user1
    Y_2 = user2

    X=[]
    y=[]

    # 벡터 데이터(트윗 텍스트)와 유저 이름(레이블)을 하나의 리스트로 묶어줌
    append_to_with_label(X,em_X_1,y,Y_1)
    append_to_with_label(X,em_X_2,y,Y_2)

    # 모델 학습
    classifier = LogisticRegression()
    classifier.fit(X,y)

    PREDICTION_TEXT = word

    # 예측하고자하는 데이터 벡터화
    em_pred_val = en.encode(texts=[PREDICTION_TEXT])

    # 학습된 모델로 데이터 예측
    pred_result = classifier.predict(em_pred_val)

    print(f"The final prediction value for {PREDICTION_TEXT} is {pred_result}.")









