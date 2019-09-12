from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User
import config
import os

#Adding comment for test
#this is amars comment
#another comment is here
#more comments

test_variable = True

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'web_app')

login_manager = LoginManager()

app = Flask('Productivity-Wars', root_path=web_dir)
csrf = CSRFProtect(app)
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

