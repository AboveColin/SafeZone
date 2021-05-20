#!/usr/bin/python
import SafeZone.functions as Function
from SafeZone import user_db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class log:
    def __init__(self, name):
        self.name = name

    def log_prefix_r(self):
        return "[" + bcolors.OKCYAN + " " * int(14 - len(self.name)) + self.name + bcolors.WHITE + "]"

    def log_prefix_addr(self):
        return "[" + bcolors.OKCYAN + " " * int(2 - len(self.name)) + self.name + bcolors.WHITE + "]"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WHITE = '\033[39m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class log_type:
    PING = "[\033[39m" + "P\033[39m]"
    READ = "[\033[92m" + "R\033[39m]"
    INFO = "[\033[95m" + "I\033[39m]"
    ONLINE = "[\033[93m" + "O\033[39m]"


##############
#  Database  #
##############

# The user_loader decorator provides the user with a flask login and gets the ID of that user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Class User
class User(user_db.Model, UserMixin):

    __tablename__ = 'Users'
    id = user_db.Column(user_db.Integer, primary_key=True)
    username = user_db.Column(user_db.String(64), unique=True)
    password_hash = user_db.Column(user_db.String(128))
    admin = user_db.Column(user_db.String(1))

    def __init__(self, username, password, admin=0):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.admin = admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Creates all the databases
user_db.create_all()