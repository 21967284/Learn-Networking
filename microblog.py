from app import app, db
from app.models import User, Question, Answer, Mark

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question, 'Answer': Answer, 'Mark': Mark}