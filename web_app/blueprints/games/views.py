from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.game import Game
import peewee as pw
from config import Config


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')

@games_blueprint.route("/new_game")
def new_game_page():
    return render_template('games/new_game_page.html')

@games_blueprint.route('create_new_games')
def create_new_game():
    player_1 = User.get_or_none(User.id == current_user.id)
    player_2_email = request.form.get('p2_email')
    player_2 = User.get_or_none(User.email == player_2_email)
    new_game = Game(player_1 = player_1, player_2 = player_2)
    new_game.save()

    p1_habit_a = Habit(game=new_game, user=player_1, name=request.form.get('habit_1_name'), frequency=request.form.get('habit_1_frequency'))
    p1_habit_b = Habit(game=new_game, user=player_1, name=request.form.get('habit_2_name'), frequency=request.form.get('habit_2_frequency'))
    p1_habit_c = Habit(game=new_game, user=player_1, name=request.form.get('habit_3_name'), frequency=request.form.get('habit_3_frequency'))

    p1_habit_a.save()
    p1_habit_b.save()
    p1_habit_c.save()
    return render_template('games/new_game_page.html')