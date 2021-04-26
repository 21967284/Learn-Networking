from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    admin = db.Column(db.Integer, index=True)
    password_hash = db.Column(db.String(128))
    questions = db.relationship('Question', secondary='mark')

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), unique=True)
    correct = db.Column(db.Integer)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    users = db.relationship('User', secondary='mark')

    def __repr__(self):
        return 'Question {}'.format(self.question)

class Answer(db.Model):
    __tablename__ = 'answer'
    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(128))
    question_id_fk = db.Column(db.Integer, db.ForeignKey('question.question_id'))

    def __repr__(self):
        return 'Answer {}'.format(self.answer)

class Mark(db.Model):
    __tablename__ = 'mark'
    mark = db.Column(db.Integer)
    question_id_fk = db.Column(db.Integer, db.ForeignKey('question.question_id'), primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return 'Mark {}'.format(self.mark)