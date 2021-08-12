## This program defines the schema of our relational database using SQLAlchemy ##
## Two versions of the migrations/ folder are included (one labelled by migrations_old/. ##
## This is because only a small change was made to an already existing column, which was not being picked up by flask db migrate. ## 

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# User table (UserMixin is used for Flask-login)
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # since we are likely to want to gather data using more than one field in User, we index username, email, and admin
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    admin = db.Column(db.Boolean, index=True)
    # password stored as a hash for security
    password_hash = db.Column(db.String(128))
    # there is a M:M relationship between User and Question
    questions = db.relationship('Mark', back_populates="user")#, cascade="all, delete-orphan")#secondary='mark', back_populates="users")
    progress = db.Column(db.Integer, default=0)

    # define how entries into this table are represented
    def __repr__(self):
        return 'User {}'.format(self.username)

    # generate a hash code associated with the user's password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # compare the entered password hash to the one stored on the database
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_progress(self, progress):
        if self.progress is None:
            self.progress=0
        if progress >= self.progress:
            self.progress = progress
            return True
        else:
            return False


# store questions in a table
class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True)
    # refers to the content section the question appears in
    section = db.Column(db.String(128))
    # holds the question's text - what the user sees
    question = db.Column(db.String(128), unique=True)
    # which answer is correct
    correct_answer = db.Column(db.String(128))
    # provides a list of answer options to be presented to the user
    answer_options = db.relationship('Answer', backref='question', lazy='dynamic')#, cascade="all, delete-orphan")
    users = db.relationship('Mark', back_populates="question")#secondary='mark', back_populates="questions")


    def __repr__(self):
        return 'Question {}'.format(self.question)


# stores answers (right and wrong) associated with each multi-choice question
class Answer(db.Model):
    __tablename__ = 'answer'
    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(128))
    question_id_fk = db.Column(db.Integer, db.ForeignKey('question.question_id'))

    def __repr__(self):
        return 'Answer {}'.format(self.answer)


# relational table to store user's marks for each question
class Mark(db.Model):
    __tablename__ = 'mark'
    mark = db.Column(db.Integer)
    question_id_fk = db.Column(db.Integer, db.ForeignKey('question.question_id', ondelete=u'CASCADE'), primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id', ondelete=u'CASCADE'), primary_key=True)
    user = db.relationship('User', back_populates="questions")
    question = db.relationship('Question', back_populates="users")

    def __repr__(self):
        return 'Mark {}'.format(self.mark)
