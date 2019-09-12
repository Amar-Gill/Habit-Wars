from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config


games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')