
from flask import Flask, redirect, url_for, render_template, sessions
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User
from flask_celery import make_celery
from models.round import Round
from datetime import datetime, timedelta
from dotenv import load_dotenv
import config
import os

load_dotenv()

import config
import os

	
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'web_app')

login_manager = LoginManager()

app = Flask('Productivity-Wars', root_path=web_dir)
csrf = CSRFProtect(app)
celery = make_celery(app)
login_manager.init_app(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)


@celery.task(name='app.async_create_round')
def async_create_round(game_id):

    # get time delta to sunday midnight ( monday 00:00:00 ) in seconds
    present_time = datetime.utcnow()
    sec_per_day = 24*60*60
    delta = (7 - present_time.weekday() )*sec_per_day - present_time.hour*60*60 - present_time.minute*60 - present_time.second

    # automatically end currently active round if it exists
    # can we code logic for loghabit using queries in loghabit functions?

    # add round to db for game
    round = Round(game_id = game_id)
    round.save()

    # start recursive background task to execute on Monday 00:00:00 - which recalls round.create
    # for development purposes set timedelta = 30s
    async_create_round.apply_async((game_id,), countdown = delta )
