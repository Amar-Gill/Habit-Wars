from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.game import Game
from models.user import User
from models.habit import Habit
import peewee as pw
from config import Config


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')

@games_blueprint.route("/new_game")
def new_game_page():
    return render_template('games/new_game_page.html')

@games_blueprint.route('create_new_games', methods=['POST', 'GET'])
def create_new_game():
    
    player_1 = User.get_or_none(User.username == "user3")
    player_2 = User.get_or_none(User.username == request.form["p2_name"])
    new_game = Game(player_1 = player_1, player_2 = player_2)
    new_game.save()

    habit_a = Habit(game = new_game, user = player_1, 
    name = request.form["habit_1_name"], 
    frequency=request.form["habit_1_value"])

    habit_b = Habit(game = new_game, user = player_1, 
    name = request.form["habit_2_name"], 
    frequency=request.form["habit_2_value"])

    habit_c = Habit(game = new_game, user = player_1, 
    name = request.form["habit_3_name"], 
    frequency=request.form["habit_3_value"])

    habit_a.save()
    habit_b.save()
    habit_c.save()

    return redirect(url_for('games.new_game_page'))