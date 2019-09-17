from models.base_model import BaseModel
from playhouse.postgres_ext import ArrayField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, current_user
from models.user import User
from models.game import Game
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw

class Round(BaseModel):
    game = pw.ForeignKeyField(Game, backref='rounds', null=False)
    player_1_rolls = ArrayField(pw.IntegerField, null=True)
    player_2_rolls = ArrayField(pw.IntegerField, null=True)
    player_1_initiative = pw.IntegerField(default = 0)
    player_2_inititative = pw.IntegerField(default = 0)
    player_1_stats = ArrayField(pw.IntegerField, default=[10,150,5]) #make array
    player_2_stats = ArrayField(pw.IntegerField, default=[10,150,5]) #make array
    player_1_dmg_array = ArrayField(pw.IntegerField, default=[]) #make array
    player_2_dmg_array = ArrayField(pw.IntegerField, default=[]) #make array
    result = pw.ForeignKeyField(User, backref='rounds', null=True)