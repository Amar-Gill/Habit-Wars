from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, current_user
from models.user import User
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw

class Game(BaseModel):
    player_1 = pw.ForeignKeyField(User, backref='games', null=False)
    player_2 = pw.ForeignKeyField(User, backref='games', null=False)
    player_1_score = pw.IntegerField(default=0, null=False)
    player_2_score = pw.IntegerField(default=0, null=False)
    accepted = pw.BooleanField(default=False)