import json, uuid
from app import db
import bcrypt
from datetime import datetime
from password_validator import PasswordValidator
#from flask_login import UserMixin

"""
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
"""

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    # -------- Connections
    # -------- FK
    # -------- BACKREF
    # events = db.relationship('Event', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    # workouts = db.relationship('Workout', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    # exercises = db.relationship('Exercise', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Username: {self.username}, ID: {self.id}'

    def set_password(self, password):

        schema = PasswordValidator()
        schema \
            .min(8) \
            .max(100) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits() \
            .has().no().spaces() \

        if not schema.validate(password):
            return False

        salt = bcrypt.gensalt(14)
        p_bytes = password.encode()
        pw_hash = bcrypt.hashpw(p_bytes, salt)
        self.password_hash = pw_hash.decode()
        self.salt = salt.decode()
        return True

    def check_password(self, password):
        c_password = bcrypt.hashpw(password.encode(), self.salt.encode()).decode()
        if c_password == self.password_hash:
            return True
        else:
            return False

    def get_self_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser
        }


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    description = db.Column(db.String(256), default='No description')
    short_name = db.Column(db.String(32), default='No name')
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    workouts = db.Column(db.String(), default='')
    sequence = db.Column(db.String(), default='')
    ident = db.Column(db.String(6), nullable=False)
    closed = db.Column(db.Boolean, default=False)
    named = db.Column(db.Integer, default=0)

    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    # -------- BACKREF
    # competitors = db.relationship('Competitor', backref='event', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self):
        self.ident = self.gen_ident()

    def __repr__(self):
        return f'id: {self.id}, ident: {self.ident}, user: {self.user}'

    def gen_ident(self):
        uid = str(uuid.uuid1()).split('-')[3]
        ts = str(datetime.now().timestamp()).encode()
        ts_hash = bcrypt.hashpw(ts, bcrypt.gensalt()).decode()[51:53]
        self.ident = uid + ts_hash
        return str(uid + ts_hash)

    def get_ident(self):
        return str(self.ident)

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.short_name,
            'description': self.description,
            'workouts': self.workouts,
            'sequence': self.sequence,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'closed': self.closed,
            'ident': self.ident,
            'named': self.named
        }


class Workout(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    short_name = db.Column(db.String(32), unique=True, nullable=False, default='No name')
    description = db.Column(db.String(256), default=None)
    exercises = db.Column(db.String(), default='')
    '''

    eg.
    [4,56,23,76,2,42, ... ] -> ID of Exercise

    eg.
    [{'time': 600(time in secs), 'type': 'warmup'(warmup/time/rest), 'max': 120(maximum reps) , 'add': 'KÉSZÜLJ!(plain text)'},{...}]
    eg. pentathlon:
    [
    { 'time': 5, 'type': 'warmup', 'max': 0, 'add': 'Felkészülés'},
    { 'time': 360, 'type': 'time', 'max': 120, 'add': 'Clean'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'time', 'max': 60, 'add': 'Clean&Press'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Jerk'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 108, 'add': 'Half Snatch'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Push Press'}
    ]
    '''
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)

    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'id: {self.id}, name: {self.short_name}, user: {self.user}, exercises: {self.exercises}'

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.short_name,
            'description': self.description,
            'exercises': json.loads(self.exercises),
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        }


class Competitor(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    cname = db.Column(db.String(64))
    association = db.Column(db.String(128))
    weight = db.Column(db.Integer, default=0)
    y_o_b = db.Column(db.Integer, default=1950)
    gender = db.Column(db.Integer, nullable=False, default=1)  # 1 - male, 2 - female
    result = db.Column(db.Integer, default=0)
    category = db.Column(db.String(32), default='')
    finished = db.Column(db.Integer, default=0)

    # -------- Connections
    # -------- FK
    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    workout = db.Column(db.Integer, db.ForeignKey('workout.id'))

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, result: {self.result}'

    def generate_category(self):

        age = datetime.now().year - self.y_o_b

        if self.gender == 2:
            if age <= 18:
                self.category = 'W-U18'
                return True
            elif age >= 50:
                self.category = 'W-Sen50+'
                return True
            else:
                if self.weight < 70:
                    self.category = 'W-70-'
                    return True
                elif self.weight >= 70:
                    self.category = 'W-70+'
                    return True
                else:
                    return False

        elif self.gender == 1:
            if age <= 18:
                self.category = 'M-U18'
                return True
            elif age >= 50:
                self.category = 'M-Sen50+'
                return True
            else:
                if self.weight < 80:
                    self.category = 'M-80-'
                    return True
                elif self.weight >= 80 and self.weight < 95:
                    self.category = 'M-95-'
                    return True
                elif self.weight >= 95:
                    self.category = 'M-95+'
                    return True
                else:
                    return False

        else:
            return False

    def increment_result(self, point):
        try:
            self.result += int(point)
            return True
        except TypeError:
            return False

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.cname,
            'association': self.association,
            'weight': self.weight,
            'y_o_b': self.y_o_b,
            'gender': self.gender,
            'result': self.result,
            'category': self.category,
            'finished': self.finished,
            'event': self.event,
            'workout': self.workout
        }


class Exercise(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, default='Noname exercise')  # Name of exercise, to represent
    short_name = db.Column(db.String(32), default='Noname_short')
    link = db.Column(db.String(), default='')
    type = db.Column(db.String(32), nullable=False, default='rest')  # rest/warmup/workout
    max_rep = db.Column(db.Integer, nullable=False, default=0)  # max countable rep, if -1->unlimited
    duration = db.Column(db.Integer, nullable=False, default=0)  # duration of exercise in seconds
    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    # -------- BACKREF

    def __repr__(self):
        return f'name: {self.name}, type: {self.type}, max: {self.max_rep}, duration: {self.duration}'

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'link': self.link,
            'type': self.type,
            'max_rep': self.max_rep,
            'duration': self.duration,
            'user': self.user
        }