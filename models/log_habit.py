from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, current_user
from models.user import User
from models.habit import Habit
from models.round import Round
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw

class LogHabit(BaseModel):
    habit = pw.ForeignKeyField(Habit, backref='log_habits', null=False)
    sender = pw.ForeignKeyField(User, backref='log_habits', null=False)
    receiver = pw.ForeignKeyField(User, backref='log_habits', null=False)
    approved = pw.BooleanField(default=False)
    image_path = pw.CharField(default='')
    game_round = pw.ForeignKeyField(Round, backref='log_habits', null=False)