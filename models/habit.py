import peewee as pw
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, current_user
from models.user import User
from models.game import Game
from playhouse.hybrid import hybrid_property
from config import Config

class Habit(BaseModel):
    game = pw.ForeignKeyField(Game, backref='habits', null=False)
    user = pw.ForeignKeyField(User, backref='habits', null=False)
    name = pw.CharField(null=False)
    frequency = pw.IntegerField(null=False)