from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config


rounds_blueprint = Blueprint('rounds',
                            __name__,
                            template_folder='templates')