from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.game import Game
from models.user import User
from models.habit import Habit
import peewee as pw
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
from models.log_habit import LogHabit


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')

@games_blueprint.route("/new_game")
def new_game_page():
    return render_template('games/new_game_page.html')

@games_blueprint.route('create_new_games', methods=['POST', 'GET'])
def create_new_game():
    
    player_1 = User.get_or_none(User.username == "user3")
    p2_name = request.form["p2_name"]

    habit_a_name = request.form.get('habit_1_name')
    habit_a_frequency = request.form.get('habit_1_value')
    habit_b_name = request.form.get('habit_2_name')
    habit_b_frequency = request.form.get('habit_2_value')
    habit_c_name = request.form.get('habit_3_name')
    habit_c_frequency = request.form.get('habit_3_value')
    
    #error handle
    if p2_name == "":
        flash("Please enter a player username!")
        return redirect(url_for('games.new_game_page'))
    else:
        player_2 = User.get_or_none(User.username == p2_name)
        new_game = Game(player_1 = player_1, player_2 = player_2)

    if (not habit_a_name )and (not habit_b_name) and (not habit_c_name):
        flash('Enter minimum one habit!')
        return redirect(url_for('games.new_game_page'))

    if habit_a_name:
        if not habit_a_frequency:
            flash('Select how many times per week you wish to complete habit for habit 1')
            return redirect(url_for('games.new_game_page'))
        else:
            habit_a = Habit(game = new_game, user = player_1, 
            name = habit_a_name, 
            frequency= habit_a_frequency)
            new_game.save()
            habit_a.save()

    if habit_b_name:
        if not habit_b_frequency:
            flash('Select how many times per week you wish to complete habit for habit 2')
            return redirect(url_for('games.new_game_page'))
        else:
            habit_b = Habit(game = new_game, user = player_1, 
            name = habit_b_name, 
            frequency= habit_b_frequency)
            new_game.save()
            habit_b.save()

    if habit_c_name:
        if not habit_c_frequency:
            flash('Select how many times per week you wish to complete habit for habit 3')
            return redirect(url_for('games.new_game_page'))
        else:
            habit_c = Habit(game = new_game, user = player_1, 
            name = habit_c_name, 
            frequency= habit_c_frequency)
            new_game.save()
            habit_c.save()

    return redirect(url_for('games.new_game_page'))

@games_blueprint.route('/<username>/<game_id>', methods=["GET"])
def show(username, game_id):
    user = User.get_or_none(User.username == username)    
    game = Game.get_or_none(Game.id == game_id)

    #Set up habit info
    user_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == user.id))
    length_habit_list = len(user_habits)


    #To render progress bar

    progress = []

    for habit in user_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == 2))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        progress.append(percentage)
        rounded_progress = [round(freq, 0) for freq in progress]
        print(rounded_progress)


    return render_template('games/show.html', username = user.username, user_habits = user_habits, length_habit_list=length_habit_list, rounded_progress = rounded_progress)

@games_blueprint.route('/<username>/index')
def index(username):
    user = User.get_or_none(User.username == username)

    # Get all active games
    games = Game.select().where((Game.player_1_id == user.id) | (Game.player_2_id == user.id))

    return render_template('games/index.html', games=games, username=username)