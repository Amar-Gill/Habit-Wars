from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
from models.log_habit import LogHabit




games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')


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
