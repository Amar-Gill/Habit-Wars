from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.game import Game
from models.habit import Habit
from models.user import User
from app import async_create_round
import peewee as pw
from config import Config


habits_blueprint = Blueprint('habits',
                            __name__,
                            template_folder='templates')

#this route is only activated for p2 in a game to accept match and create habits
@habits_blueprint.route('/create/<username>/<game_id>', methods=["POST"])
def create(username, game_id):
    
    # get current game for the page
    game = Game.get_or_none(Game.id == game_id)

    # get the user
    user = User.get_or_none(User.username == username)

    # get response for challenge - Accept or Decline
    challenge_response = request.form.get('challenge-response')

    # save habits if user clicker Accept
    if challenge_response == 'Accept':

        # get form inputs
        habit_1_value = request.form.get('habit-1-value')
        habit_2_value = request.form.get('habit-2-value')
        habit_3_value = request.form.get('habit-3-value')

        habit_1_frequency = request.form.get('habit-1-frequency')
        habit_2_frequency = request.form.get('habit-2-frequency')
        habit_3_frequency = request.form.get('habit-3-frequency')

        # save habit only if field populated
        if habit_1_value:
            if not habit_1_frequency:
                print('error')
            else:
                habit_1 = Habit(game=game,
                                user=user,
                                name=habit_1_value,
                                frequency=habit_1_frequency)
                habit_1.save()
        
        # save habit only if field populated
        if habit_2_value:
            if not habit_2_frequency:
                print('error')
            else:
                habit_2 = Habit(game=game,
                                user=user,
                                name=habit_2_value,
                                frequency=habit_2_frequency)
                habit_2.save()
        
        # save habit only if field populated
        if habit_3_value:
            if not habit_3_frequency:
                print('error')
            else:
                habit_3 = Habit(game=game,
                                user=user,
                                name=habit_3_value,
                                frequency=habit_3_frequency)
                habit_3.save()

        # set game.accepted to True
        game.accepted = True
        game.save()

        # start asynchronus loop for rounds - first call beginning immediately
        async_create_round.delay(game_id)

        return redirect(f'/game/{username}/{game_id}')

    else:
        # destroy game
        game.delete_instance(recursive=True)
        return redirect( url_for('games.index', username=username))