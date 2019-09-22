from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import peewee as pw
from config import Config
from models.user import User
import os

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=["POST"])
def create():
    # Get form field data
    username = request.form.get('username')
    password_to_check = request.form.get('password')

    
    # Get user object and associated pw hash
    u = User.get_or_none(User.username == username)

    
    if u:
        hashed_password = u.hash
        result=check_password_hash(hashed_password, password_to_check)
        if result:
            print(result)
            print('LEEROY')
            print('JENKINS')
            # flash('Success!')
            login_user(u)
            return redirect( url_for('users.show', username=username))
        else:
            flash('Password incorrect')
            return render_template('sessions/new.html')
    else:
        flash('Username incorrect')
        return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=["GET"])
def destroy():
    logout_user()
    return redirect('/')