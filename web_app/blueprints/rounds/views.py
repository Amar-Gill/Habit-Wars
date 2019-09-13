from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.log_habit import LogHabit
import peewee as pw
from config import Config


rounds_blueprint = Blueprint('rounds',
                            __name__,
                            template_folder='templates')

@rounds_blueprint.route('/<game_id>/round')
def show(game_id):

    #get round id
    round_id = 1

    #get current player id


    #querydb get habits with user_id==current user AND game_id==game_id


    #for each habit, query log_habits table and get number of rows for that habit for current_round
    #compare to frequency number of the habit
    num_dice = len(LogHabit.select().where(LogHabit.round_id == round_id))

    return render_template('show.html', num_dice=num_dice)