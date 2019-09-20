from flask import Flask, render_template, sessions
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User
import config
import os


from passlib.hash import sha256_crypt
import config
import os


password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")

print(password)
print(password2)

print(sha256_crypt.verify("password", password))
		
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