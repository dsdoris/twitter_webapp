from flask import Flask
import os
from dotenv import load_dotenv
from twitter_webapp.routes import main_routes, user_routes
from twitter_webapp.models import db, migrate, set_tweetdata


# Twitter delvelop account 승인 시 작업 예정
def create_app():
    load_dotenv()
    app = Flask(__name__)

    # 데이터베이스 초기설정
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI')
    app.config["SQLALCHEMY_TRACK_MODFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # route별 blueprint 등록
    app.register_blueprint(main_routes.main_routes)
    app.register_blueprint(user_routes.user_routes, url_prefix='/<username>')


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)