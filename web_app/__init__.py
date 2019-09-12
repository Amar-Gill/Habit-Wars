from app import app
from flask import render_template

from web_app.blueprints.users.views import users_blueprint
from web_app.blueprints.sessions.views import sessions_blueprint
from web_app.blueprints.log_habits.views import log_habits_blueprint
from web_app.blueprints.habits.views import habits_blueprint
from web_app.blueprints.games.views import games_blueprint
from web_app.blueprints.rounds.views import rounds_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(log_habits_blueprint, url_prefix="/log_habit")
app.register_blueprint(habits_blueprint, url_prefix="/habit")
app.register_blueprint(games_blueprint, url_prefix="/game")
app.register_blueprint(rounds_blueprint, url_prefix="/round")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def unauthorized_error(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def resource_not_found_error(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')