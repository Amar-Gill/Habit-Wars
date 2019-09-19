from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from helpers.s3_helper import upload_file_to_s3
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
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


    #Comment back in after login possible
    # if current_user == user:



    image_file = request.files[f'image-for-{habit_id}']

    print(image_file)
    output = upload_file_to_s3(image_file, Config.S3_BUCKET)

    print(output)
    #Add image path after AWS
    #Change hardcoded game round id

                


    new_habit_logged = LogHabit(habit_id = habit_id,
                                sender_id = current_habit.user_id,
                                receiver_id = receiver_id,
                                approved = False,
                                image_path = str(output),
                                game_round_id = 2)
    
    new_habit_logged.save()

    return redirect(url_for('games.show', game_id = game_id, username = username ))








