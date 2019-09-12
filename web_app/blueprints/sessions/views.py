from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')