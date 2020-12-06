from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
from embedding_as_service_client import EmbeddingClient
from twitter_webapp.services import twitter_api
from sklearn.linear_model import LogisticRegression

db = SQLAlchemy()
migrate = Migrate()

en = EmbeddingClient(host='54.180.124.154', port=8989)


# User Table
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    full_name = db.Column(db.String, nullable=False)
    followers = db.Column(db.BigInteger, default=0)
    location = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"


# Tweet Table
class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String, nullable=False)
    user = db.relationship('User',backref=db.backref('tweets', lazy=True))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    embedding = db.Column(db.PickleType)

    def __repr__(self):
        return f"<Tweet {self.id}>"


# User 데이터 가져오기(전체)
def get_userdata():
    return User.query.all()


# User 데이터 수정
def update_userdata(username, fullname, location):
    user = User.query.filter_by(username=username).update({'full_name': fullname, 'location': location})
    db.session.commit()
    print("update_commit")
    return User.query.filter_by(username=username).first()


# Tweet 데이터 세팅
def set_tweetdata():
    # Tweet테이블 초기화(기존자료 삭제)
    Tweet.query.delete()

    # User 데이터 가져오기
    user = get_userdata()

    # User테이블 데이터 기준으로 트윗데이터 저장
    print("update data at Tweet table...")
    for user in user:
        raw_tweet = twitter_api.api.user_timeline(user_id = user.id, count=50, include_rts=False, exclude_replies=True, tweet_mode="extended")
        en_tweet = embedding_tweet(raw_tweet)
        for tweet in raw_tweet:
            db.session.add(Tweet(id=tweet.id, text=tweet.full_text, user_id=user.id, embedding=en_tweet))
    
    db.session.commit()
    
    return Tweet.query.all()


# tweet 데이터 벡터화
def embedding_tweet(data):
    en_list = []
    for tweet in data:
        en_list.append(tweet.full_text)

    return en.encode(texts=en_list)

# 학습데이터 라벨링
def append_to_with_label(to_arr, from_arr, label_arr, label):
    for item in from_arr:
        to_arr.append(item)
        label_arr.append(label)


# 트윗데이터 분석
def compare_user(user1, user2, word):
    # 이용자의 트윗 불러오기
    userid1 = User.query.filter_by(username=user1).first().id
    userid2 = User.query.filter_by(username=user2).first().id

    raw_tweet1 = twitter_api.api.user_timeline(user_id = userid1, count=50, include_rts=False, exclude_replies=True, tweet_mode="extended")
    raw_tweet2 = twitter_api.api.user_timeline(user_id = userid2, count=50, include_rts=False, exclude_replies=True, tweet_mode="extended")
    
    # 텍스트를 벡터로 변경
    em_X_1 = embedding_tweet(raw_tweet1)    # em_X_1 = db.session.query(Tweet.embedding).filter_by(user_id=userid1).all()
    em_X_2 = embedding_tweet(raw_tweet2)    # em_X_2 = db.session.query(Tweet.embedding).filter_by(user_id=userid2).all()
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

    return f"'{PREDICTION_TEXT}'(이)라는 단어를 말할 확률이 높은 이용자는 {pred_result} 입니다."


# def save_model(model):
#     with open(MODEL_PATH, "wb") as file:
#         pickle.dump(model, file)


# def load_model():
#     with open(MODEL_FILEPATH, "rb") as file:
#         loaded_model = pickle.load(file)
#     return loaded_mode 