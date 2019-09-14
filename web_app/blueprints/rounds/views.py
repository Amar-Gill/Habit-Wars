from flask import Blueprint, render_template, request, redirect, flash, abort, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import User
from models.log_habit import LogHabit
from models.game import Game
from models.round import Round
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

    #get game model object
    game = Game.get_by_id(game_id)

    #empty array for number of dice
    dice_array = []
    num_dice = 0

    #get round id and round instance
    round_id = 1 #hardcode for dev purposes
    round = Round.get_by_id(round_id)

    #get current player id - hardcoded for now
    current_player = User.get_by_id(1)

    #determine if current_user is p1 or p2 and get roll array
    game_player_1_id = game.player_1_id
    # if current_user.id == game_player_1_id:
    if current_player.id == game_player_1_id:
        player_variable = 1
        roll_array = round.player_1_rolls
    else:
        player_variable = 2
        roll_array = round.player_2_rolls


    #querydb get habits with user_id==current user AND game_id==game_id
    # current_user_habit_array = Habit.select().where((Habit.user_id == current_user.id) & (Habit.game_id == game_id))
    current_user_habit_array = Habit.select().where((Habit.user_id == current_player.id) & (Habit.game_id == game_id))


    #for each habit, query log_habits table and get number of rows for that habit for current_round that r approved
    #compare to frequency number of the habit
    for habit in current_user_habit_array:

        #query loghabit table for rows belonging to habit/user which are approved
        # approved_logs = LogHabit.select().where((LogHabit.sender==current_user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved==True) & (LogHabit.game_round_id == round_id))
        approved_logs = LogHabit.select().where((LogHabit.sender==current_player.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved==True) & (LogHabit.game_round_id == round_id))

        #get length of list
        #compare length of list to frequency number
        if len(approved_logs) >= habit.frequency:
            #append to dice list
            dice_array += [1]
            num_dice += 1

    return render_template('rounds/show.html', num_dice=num_dice, dice_array=dice_array, player_variable=player_variable, game_id=game_id, roll_array=roll_array)

@rounds_blueprint.route('/game=<game_id>/player=<player>/roll', methods=['POST'])
def roll_dice(game_id, player):
    roll_value = int(request.form.get('roll_value'))
    roll_index = int(request.form.get('roll_index'))

    # get round instance - do we need game_id????
    round = Round.get_by_id(1)

    if player == '1':
        round.player_1_rolls[roll_index] = roll_value
        round.save()
    else:
        round.player_2_rolls[roll_index] = roll_value
        round.save()

    return redirect('round/game=1/show')