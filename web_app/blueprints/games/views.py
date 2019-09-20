from flask import Blueprint, render_template, request, redirect, flash, abort, url_for, jsonify
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
from app import async_create_round


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')


@games_blueprint.route("/new_game")
def new_game_page():
    return render_template('games/new_game_page.html')


@games_blueprint.route('create_new_games', methods=['POST', 'GET'])
def create_new_game():
    
    player_1 = User.get_or_none(User.username == "test")
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


#Dont forget to change game round id!!!!
@games_blueprint.route('/<username>/<game_id>', methods=["GET", "POST"])
def show(username, game_id):

    game = Game.get_or_none(Game.id == game_id)

    # Active player - could be either player 1 or 2
    user = User.get_or_none(User.username == username)    

    #Set up habit info
    user_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == user.id))
    length_habit_list = len(user_habits)

    #progress bars

    progress = []
    user_more_to_go = []

    for habit in user_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == 2))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        progress.append(percentage)
        leftover = habit.frequency - logged_habits
        user_more_to_go.append(leftover)

    print(user_more_to_go)
    rounded_progress = [round(freq, 0) for freq in progress]


    # Opponent - could be either player 1 or player 2

    # check is active user is player_1 or player_2 for the game
    if user.id == game.player_1_id:
        active_user = 1
        opponent = User.get_or_none(User.id == game.player_2_id)
    else:
        active_user = 2
        opponent = User.get_or_none(User.id == game.player_1_id)


    opponent_username = opponent.username
    opponent_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == opponent.id))
    opponent_habit_length = len(opponent_habits)

    # check if game has been accepted by player_2 or not
    game_accepted = game.accepted

    #Progress bars

    opponent_progress = []

    for habit in opponent_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == opponent.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == 2))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        opponent_progress.append(percentage)
    
    rounded_opponent_progress = [round(freq, 0) for freq in opponent_progress]

    return render_template('games/show.html', 
                            username = user.username, 
                            user_habits = user_habits, 
                            length_habit_list=length_habit_list, 
                            rounded_progress = rounded_progress, 
                            opponent_username = opponent_username,
                            opponent_habits = opponent_habits,
                            opponent_habit_length = opponent_habit_length,
                            rounded_opponent_progress = rounded_opponent_progress,
                            user_more_to_go = user_more_to_go,
                            game_id = game.id,
                            game_accepted = game_accepted,
                            active_user=active_user)


@games_blueprint.route('/<username>/index')
def index(username):
    user = User.get_or_none(User.username == username)

    # Get all active games
    games = Game.select().where((Game.player_1_id == user.id) | (Game.player_2_id == user.id))

    return render_template('games/index.html', games=games, username=username)