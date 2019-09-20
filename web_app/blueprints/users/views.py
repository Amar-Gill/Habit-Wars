from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config


users_blueprint = Blueprint('users',                        
                            __name__,
                            template_folder='templates')

@users_blueprint.route("/user_profile")
def user_profile_page():
    return render_template('users/user_profile_page.html')

@users_blueprint.route('/register', methods = ["GET"])
def new():
    return render_template('users/register.html')




# @users_blueprint.route("/")