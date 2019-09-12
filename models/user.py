from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import peewee as pw
from flask_login import UserMixin, login_manager, current_user
from playhouse.hybrid import hybrid_property
from config import Config

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    hash = pw.CharField()
    profile_image_path = pw.CharField(null=False, default='')