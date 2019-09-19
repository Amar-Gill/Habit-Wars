from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config


habits_blueprint = Blueprint('habits',
                            __name__,
                            template_folder='templates')

@habits_blueprint.route('/create/<username>/<game_id>')
def create(username, game_id):
    pass