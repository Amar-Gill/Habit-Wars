from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import User
from models.log_habit import LogHabit
from models.habit import Habit
import peewee as pw
from config import Config


rounds_blueprint = Blueprint('rounds',
                            __name__,
                            template_folder='templates')

@rounds_blueprint.route('/game=1/show')
# def show(game_id):
def show():

    # hardcode game_id for now
    game_id = 1

    num_dice = []

    #get round id
    round_id = 1 #hardcode for dev purposes

    #get current player id - hardcoded for now
    current_player = User.get_by_id(1)


    #querydb get habits with user_id==current user AND game_id==game_id
    # current_user_habit_array = Habit.select().where((Habit.user_id == current_user.id) & (Habit.game_id == game_id))
    current_user_habit_array = Habit.select().where((Habit.user_id == current_player.id) & (Habit.game_id == game_id))


    #for each habit, query log_habits table and get number of rows for that habit for current_round that r approved
    #compare to frequency number of the habit
    for habit in current_user_habit_array:
        print('littt')

        #query loghabit table for rows belonging to habit/user which are approved
        # approved_logs = LogHabit.select().where((LogHabit.sender==current_user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved==True) & (LogHabit.game_round_id == round_id))
        approved_logs = LogHabit.select().where((LogHabit.sender==current_player.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved==True) & (LogHabit.game_round_id == round_id))

        #get length of list
        #compare length of list to frequency number
        if len(approved_logs) >= habit.frequency:
            #append to dice list
            num_dice += [1]

    return render_template('rounds/show.html', num_dice=num_dice)

@rounds_blueprint.route('/roll')
def roll_dice():
    pass