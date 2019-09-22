from flask import Blueprint, render_template, request, redirect, flash, abort, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import User
from models.log_habit import LogHabit
from models.game import Game
from models.round import Round
from models.habit import Habit
from config import Config
from datetime import datetime, timedelta
import peewee as pw
import random


rounds_blueprint = Blueprint('rounds',
                             __name__,
                             template_folder='templates')


@rounds_blueprint.route('/show/<game_id>/<round_id>', methods=['GET'])
def show(game_id, round_id):


    # get game model object
    game_id = game_id
    game = Game.get_by_id(game_id)

    # empty array for number of dice
    dice_array = []
    num_dice = 0

    # get round id and round instance
    round_id = round_id  # hardcode for dev purposes
    round = Round.get_by_id(round_id)

    # get round number from round index form
    round_num = request.args['round_num']

    # determine if current_user is p1 or p2 and get roll array
    game_player_1_id = game.player_1_id
    if current_user.id == game_player_1_id:
    # if current_player.id == game_player_1_id:
        player_variable = 1
        roll_array = round.player_1_rolls
        player_stats = round.player_1_stats
        player_initiative = round.player_1_initiative
        opponent_initiative = round.player_2_initiative
    else:
        player_variable = 2
        roll_array = round.player_2_rolls
        player_stats = round.player_2_stats
        player_initiative = round.player_2_initiative
        opponent_initiative = round.player_1_initiative

    round_result = round.result

    # querydb get habits with user_id==current user AND game_id==game_id
    # current_user_habit_array = Habit.select().where((Habit.user_id == current_user.id) & (Habit.game_id == game_id))
    current_user_habit_array = Habit.select().where(
        (Habit.user_id == current_user.id) & (Habit.game_id == game_id))

    # for each habit, query log_habits table and get number of rows for that habit for current_round that r approved
    # compare to frequency number of the habit
    for habit in current_user_habit_array:

        # query loghabit table for rows belonging to habit/user which are approved
        # approved_logs = LogHabit.select().where((LogHabit.sender==current_user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved==True) & (LogHabit.game_round_id == round_id))
        approved_logs = LogHabit.select().where((LogHabit.sender == current_user.id) & (
            LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == round_id))

        # get length of list
        # compare length of list to frequency number
        if len(approved_logs) >= habit.frequency:
            # append to dice list
            dice_array += [1]
            num_dice += 1

    return render_template('rounds/show.html',
                            round=round,
                            round_id = round_id,
                            round_num=round_num,
                            num_dice=num_dice,
                            dice_array=dice_array,
                            player_variable=player_variable,
                            game_id=game_id,
                            roll_array=roll_array,
                            player_stats=player_stats,
                            player_initiative=player_initiative,
                            opponent_initiative=opponent_initiative,
                            round_result=round_result)


@rounds_blueprint.route('/<round_id>/game_<game_id>/player_<player>/roll', methods=['POST'])
def roll_dice(game_id, player, round_id):
    roll_value = int(request.form.get('roll_value'))
    roll_index = int(request.form.get('roll_index'))

    # get round instance - do we need game_id????
    round = Round.get_by_id(round_id)

    if player == '1':
        round.player_1_rolls[roll_index] = roll_value
        round.save()
    else:
        round.player_2_rolls[roll_index] = roll_value
        round.save()

    return redirect( url_for('rounds.show', game_id = game_id, round_id=round_id))


@rounds_blueprint.route('/<round_id>/game_<game_id>/player_<player>/submit_stats', methods=['POST'])
def submit_stats(game_id, player, round_id):

    # get round instance - do we need game_id????
    round = Round.get_by_id(round_id)

    stats_array = [
        int(request.form.get('attack-input')),
        int(request.form.get('hitpoints-input')),
        int(request.form.get('luck-input'))
    ]
    print(type(stats_array))
    print(type(stats_array[0]))
    print(stats_array)

    if player == '1':
        round.player_1_stats = stats_array
        round.player_1_initiative = -1
        round.save()
    else:
        round.player_2_stats = stats_array
        round.player_2_initiative = -1
        round.save()

    return redirect( url_for('rounds.show', game_id=game_id, round_id=round_id))


@rounds_blueprint.route('/<round_id>/game=<game_id>/player=<player>/battle', methods=['POST'])
def battle(game_id, player, round_id):

    game = Game.get_by_id(game_id)
    
    # get round instance - do we need game_id????
    round = Round.get_by_id(round_id)

    player_initiative = int(request.form.get('initiative_input'))

    if player == '1':
        round.player_1_initiative = player_initiative
        round.save()
    else:
        round.player_2_initiative = player_initiative
        round.save()

    # algorithm to calculate winner
    # only execute if both players initiatives have been rolled (therefore both > 0)
    if (round.player_1_initiative > 0) and (round.player_2_initiative > 0):

        player_1_initiative = round.player_1_initiative
        player_2_initiative = round.player_2_initiative

        if player_1_initiative == player_2_initiative:
            if random.random() < 0.5:
                first_attack = 1
            else:
                first_attack = 2
        elif player_1_initiative > player_2_initiative:
            first_attack = 1
        else:
            first_attack = 2

        p1_attack = round.player_1_stats[0]
        p1_hp = round.player_1_stats[1]
        p1_luck = round.player_1_stats[2]

        p2_attack = round.player_2_stats[0]
        p2_hp = round.player_2_stats[1]
        p2_luck = round.player_2_stats[2]

        # determine winner of round
        while (p1_hp > 0 and p2_hp > 0):
            # if player 1 goes first
            if first_attack == 1:
                # check if critical hit
                if random.random()*100 < p1_luck:
                    p1_damage = p1_attack*2
                else:
                    p1_damage = p1_attack
                round.player_1_dmg_array.append(p1_damage)
                round.save()

                # check if p2 alive
                p2_hp = p2_hp - p1_damage
                if p2_hp < 0:
                    round.result = User.get_by_id(game.player_1_id)
                    round.save()
                    game.player_1_score +=1
                    game.save()
                    break

                # repeat for p2
                if random.random()*100 < p2_luck:
                    p2_damage = p2_attack*2
                else:
                    p2_damage = p2_attack
                round.player_2_dmg_array.append(p2_damage)
                round.save()

                # check if p1 alive
                p1_hp = p1_hp - p2_damage
                if p1_hp < 0:
                    round.result = User.get_by_id(game.player_2_id)
                    round.save()
                    game.player_2_score += 1
                    game.save()
                    break
            else: # if player 2 attacks first
                if random.random()*100 < p2_luck:
                    p2_damage = p2_attack*2
                else:
                    p2_damage = p2_attack
                round.player_2_dmg_array.append(p2_damage)
                round.save()

                # check if p1 alive
                p1_hp = p1_hp - p2_damage
                if p1_hp < 0:
                    round.result = User.get_by_id(game.player_2_id)
                    round.save()
                    game.player_2_score += 1
                    game.save()
                    break

                if random.random()*100 < p1_luck:
                    p1_damage = p1_attack*2
                else:
                    p1_damage = p1_attack
                round.player_1_dmg_array.append(p1_damage)
                round.save()

                # check if p2 alive
                p2_hp = p2_hp - p1_damage
                if p2_hp < 0:
                    round.result = User.get_by_id(game.player_1_id)
                    round.save()
                    game.player_1_score += 1
                    game.save()

    
    return redirect( url_for('rounds.show', game_id=game_id, round_id=round_id))


@rounds_blueprint.route('/index/<game_id>', methods=["GET"])
def index(game_id):
    rounds = Round.select().where(Round.game_id == game_id)
    game = Game.get_by_id(game_id)
    return render_template('/rounds/index.html', rounds=rounds, game=game)



