from flask import Blueprint, render_template, request, redirect, flash, abort, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.game import Game
from models.user import User
from models.habit import Habit
from models.round import Round
import peewee as pw
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
from models.log_habit import LogHabit


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')


@games_blueprint.route("/new")
@login_required
def new():
    return render_template('games/new.html')


@games_blueprint.route('/create', methods=['POST', 'GET'])
def create():
    
    player_1 = User.get_or_none(User.username == current_user.username)
    p2_name = request.form["p2_name"]

    habit_a_name = request.form.get('habit_1_name')
    habit_a_frequency = request.form.get('habit_1_value')
    habit_b_name = request.form.get('habit_2_name')
    habit_b_frequency = request.form.get('habit_2_value')
    habit_c_name = request.form.get('habit_3_name')
    habit_c_frequency = request.form.get('habit_3_value')
    
    #error handle
    if p2_name == "":
        flash("Please enter a player username!", "danger")
        return redirect(url_for('games.new'))
    elif p2_name == player_1.username:
        flash("You can not invite yourself for a game. Please choose another user.", "danger")
        return redirect(url_for('games.new'))
    else:
        player_2 = User.get_or_none(User.username == p2_name)
        if player_2 == None:
            flash("User doesn't exist. Please enter a valid username!", "danger")
            return redirect(url_for('games.new'))
        else:
            new_game = Game(player_1_id = player_1.id, player_2_id = player_2.id)

    if (not habit_a_name )and (not habit_b_name) and (not habit_c_name):
        flash('Enter at least one habit!', "danger")
        return redirect(url_for('games.new'))

    if habit_a_name:
        if not habit_a_frequency:
            flash('Select how many times per week you wish to complete habit for habit 1', "danger")
            return redirect(url_for('games.new'))
        else:
            habit_a = Habit(game = new_game, user = player_1, 
            name = habit_a_name, 
            frequency= habit_a_frequency)
            new_game.save()
            habit_a.save()

    if habit_b_name:
        if not habit_b_frequency:
            flash('Select how many times per week you wish to complete habit for habit 2', "danger")
            return redirect(url_for('games.'))
        else:
            habit_b = Habit(game = new_game, user = player_1, 
            name = habit_b_name, 
            frequency= habit_b_frequency)
            new_game.save()
            habit_b.save()

    if habit_c_name:
        if not habit_c_frequency:
            flash('Select how many times per week you wish to complete habit for habit 3', "danger")
            return redirect(url_for('games.new'))
        else:
            habit_c = Habit(game = new_game, user = player_1, 
            name = habit_c_name, 
            frequency= habit_c_frequency)
            new_game.save()
            habit_c.save()

    return redirect(url_for('games.show', game_id=new_game.id, username=player_1.username))


@games_blueprint.route('/<username>/<game_id>', methods=["GET", "POST"])
@login_required
def show(username, game_id):

    game = Game.get_or_none(Game.id == game_id)

    #int value for latest round_id for the game
    latest_round = Round.select(pw.fn.MAX(Round.id)).where(Round.game_id == game_id).scalar()
    current_round_object = Round.get_or_none(Round.id == latest_round)

    # get length of all rounds for game to send round number into anchor link to show latest round
    len_round =len(Round.select().where(Round.game_id == game_id))

    # Active player - could be either player 1 or 2
    user = User.get_or_none(User.username == username)    

    #Set up habit info
    user_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == user.id))
    length_habit_list = len(user_habits)

    #progress bars

    progress = []
    user_more_to_go = []

    for habit in user_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == latest_round))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        progress.append(percentage)
        leftover = habit.frequency - logged_habits
        user_more_to_go.append(leftover)

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
    print(opponent_habit_length)

    # check if game has been accepted by player_2 or not
    game_accepted = game.accepted

    #Progress bars

    opponent_progress = []

    for habit in opponent_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == opponent.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == latest_round))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        opponent_progress.append(percentage)
    
    print(opponent_progress)
    rounded_opponent_progress = [round(freq, 0) for freq in opponent_progress]


    habits = Habit.select().where(Habit.game_id == game_id)
    game_habits = []

    for habit in habits:
        game_habits.append(habit.id)
    to_approve = LogHabit.select().where((LogHabit.approved == False) & (LogHabit.receiver_id == user.id) & (LogHabit.habit_id in game_habits))
    to_approve_length = len(to_approve)

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
                            active_user=active_user,
                            to_approve_length = to_approve_length,
                            current_round_object=current_round_object,
                            len_round=len_round)


@games_blueprint.route('/<username>/index')
@login_required
def index(username):
    user = User.get_or_none(User.username == username)

    # Get all active games
    games = Game.select().where((Game.player_1_id == user.id) | (Game.player_2_id == user.id))


    return render_template('games/index.html', games=games, username=username)





    
