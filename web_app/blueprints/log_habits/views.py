from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from helpers.s3_helper import upload_file_to_s3
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
from models.round import Round
from models.log_habit import LogHabit


log_habits_blueprint = Blueprint('log_habits',
                            __name__,
                            template_folder='templates')


#Logging habits

@log_habits_blueprint.route('/create' , methods=["POST"])
def create():

    #Getting habit_id from the hidden form
    habit_id = request.form.get('habit-id')
    current_habit = Habit.get_or_none(Habit.id == habit_id)

    game_id = current_habit.game_id
    game = Game.get_or_none(Game.id == game_id)

    user = User.get_or_none(User.id == current_habit.user_id)
    username = user.username

    sender_id = current_habit.user_id
    if sender_id == game.player_1_id:
        receiver_id = game.player_2_id
    else:
        receiver_id = game.player_1_id


    # if current_user == user:



    image_file = request.files[f'image-for-{habit_id}']

    output = upload_file_to_s3(image_file, Config.S3_BUCKET)



                
    latest_round = Round.select(pw.fn.MAX(Round.id)).where(Round.game_id == game_id).scalar()


    new_habit_logged = LogHabit(habit_id = habit_id,
                                sender_id = current_habit.user_id,
                                receiver_id = receiver_id,
                                approved = False,
                                image_path = str(output),
                                game_round_id = latest_round)
    
    new_habit_logged.save()

    flash('Habit submitted. Waiting for your opponent\'s approval. Keep up the good work!')

    return redirect(url_for('games.show', game_id = game_id, username = username ))


@log_habits_blueprint.route('/<username>/<game_id>/show_approve')
def show_approve(username, game_id):
    user = User.get_or_none(User.username == username)
    game = Game.get_or_none(Game.id == game_id)

    habits = Habit.select().where(Habit.game_id == game_id)
    game_habits = []

    for habit in habits:
        game_habits.append(habit.id)

    to_approve = LogHabit.select().where((LogHabit.approved == False) & (LogHabit.receiver_id == user.id) & (LogHabit.habit_id << game_habits))

    to_approve_length = len(to_approve)
    sender_ids = []
    senders = []

    for log in to_approve:
        sender_ids.append(log.sender_id)
    for id in sender_ids:
        sender = User.get_or_none(User.id == id)
        senders.append(sender.username)
    
    

    return render_template('log_habits/approval.html', to_approve = to_approve,
                                                    to_approve_length = to_approve_length,
                                                    username = username,
                                                    game_id = game_id,
                                                    senders = senders)

@log_habits_blueprint.route('/<username>/<game_id>/approve', methods=["POST"])
def approve(username, game_id):
    user = User.get_or_none(User.username == username)
    game = Game.get_or_none(Game.id == game_id)

    habits = Habit.select().where(Habit.game_id == game_id)
    game_habits = []

    for habit in habits:
        game_habits.append(habit.id)

    to_approve = LogHabit.select().where((LogHabit.approved == False) & (LogHabit.receiver_id == user.id) & (LogHabit.habit_id in game_habits))


    loghabit_id = request.form.get('loghabit-ids')


    loghabit = LogHabit.get_or_none(LogHabit.id == loghabit_id)
    LogHabit.update(approved = True).where(LogHabit.id == loghabit_id).execute()

    flash('Habit approved.')

    if len(to_approve) < 1:
        return redirect(url_for('games.show', game_id = game_id, username = username))


    return redirect(url_for('log_habits.show_approve', game_id = game_id, username = username ))

@log_habits_blueprint.route('/<username>/<game_id>/reject', methods=["POST"])
def reject(username, game_id):
    user = User.get_or_none(User.username == username)
    game = Game.get_or_none(Game.id == game_id)

    habits = Habit.select().where(Habit.game_id == game_id)
    game_habits = []

    for habit in habits:
        game_habits.append(habit.id)

    to_approve = LogHabit.select().where((LogHabit.approved == False) & (LogHabit.receiver_id == user.id) & (LogHabit.habit_id in game_habits))


    loghabit_id = request.form.get('loghabit-ids')
    print(loghabit_id)
    loghabit = LogHabit.get_or_none(LogHabit.id == loghabit_id)
    delete_log = LogHabit.delete().where(LogHabit.id == loghabit_id)
    delete_log.execute()

    flash('Habit rejected.')

    if len(to_approve) < 1:
        return redirect(url_for('games.show', game_id = game_id, username = username))

    return redirect(url_for('log_habits.show_approve', game_id = game_id, username = username ))







