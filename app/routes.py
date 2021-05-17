## define the urls of each webpage ##

import random

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegisterForm, ManageQuestionsForm
from app.helper import nav_items, auto_build_questions, auto_create_login, auto_clear_database
from app.models import User, Answer, Question, Mark


# homepage (set to the root page)
@app.route('/')
def home():
    if not current_user:
        user = None
    else:
        user = current_user
    return render_template('home.html', title="A journey through the tcp/ip model", nav_items=nav_items(user))


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # don't allow logged in users to access this page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    lForm = LoginForm()

    # if the login details are validated - NOTE WE WILL ALSO ADD JAVASCRIPT VALIDATION FOR RESPONSIVE FEEDBACK
    if lForm.validate_on_submit():
        # try setting user to the associated username's row - if that returns None then try email
        user = User.query.filter_by(username=lForm.username.data).first() or User.query.filter_by(
            email=lForm.username.data).first()
        # non-existant user or invalid password
        if user is None or not user.check_password(lForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=lForm.remember_me.data)
        # handle users clicking on pages that require login
        next_page = request.args.get('next')
        # if there is no specified next page, or the 'next' query points to a page outside this domain
        if not next_page or url_parse(next_page).netloc != '':
            # set the default location to the home page
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title="Login", lForm=lForm, nav_items=nav_items(current_user))


# logout button replaces login if the user is authenticated
@app.route('/logout')
def logout():
    logout_user()
    # if the link is clicked, log the user out then reroute them back to home
    return redirect(url_for('home'))


# register page - this function is very similar to the login function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    rForm = RegisterForm()

    if rForm.validate_on_submit():
        user = User(
            first_name=rForm.firstname.data,
            last_name=rForm.lastname.data,
            username=rForm.username.data,
            email=rForm.email.data,
            progress=0)
        user.set_password(rForm.password.data)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()

        # log the user in
        login_user(user, remember=rForm.remember_me.data)
        # we can edit the style of flash messages to help the website interact with users
        flash('Congratulations {}, you are now a registered user!'.format(rForm.firstname.data))
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", rForm=rForm, nav_items=nav_items(current_user))


# register page - this function is very similar to the login function
@app.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    rForm = RegisterForm()

    if rForm.validate_on_submit():
        user = User(
            first_name=rForm.firstname.data,
            last_name=rForm.lastname.data,
            username=rForm.username.data,
            email=rForm.email.data,
            admin=True,
            progress=0)
        user.set_password(rForm.password.data)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()
        # we can edit the style of flash messages to help the website interact with users
        flash('Congratulations {}, you are now an admin user!'.format(rForm.firstname.data))
        return redirect(url_for('login'))

    return render_template('register.html', title="Register admin", rForm=rForm, nav_items=nav_items(current_user))


# all empty pages (yet to be implemented so far)

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', title="Progress", nav_items=nav_items(current_user))


@app.route('/application')
@login_required
def application():
    return render_template('./Content/application.html', title="Application Layer", nav_items=nav_items(current_user))


@app.route('/application-quiz')
@login_required
def application_link():
    return render_template('quiz.html', title="Application Layer Quiz", nav_items=nav_items(current_user))


@app.route('/transport')
@login_required
def transport():
    return render_template('./Content/transport.html', title="Transport Layer", nav_items=nav_items(current_user))


@app.route('/transport-quiz')
@login_required
def transport_quiz():
    return render_template('quiz.html', title="Transport Layer Quiz", nav_items=nav_items(current_user))


@app.route('/network')
@login_required
def network():
    return render_template('./Content/network.html', title="Network Layer", nav_items=nav_items(current_user))


@app.route('/network-quiz')
@login_required
def network_quiz():
    return render_template('quiz.html', title="Network Layer Quiz", nav_items=nav_items(current_user))


@app.route('/link')
@login_required
def link():
    return render_template('./Content/link.html', title="Link Layer", nav_items=nav_items(current_user))


@app.route('/link-quiz')
@login_required
def link_quiz():
    return render_template('quiz.html', title="Link Layer Quiz", nav_items=nav_items(current_user))


@app.route('/retrieve-progress-data')
@login_required
def progress_data():
    user_data = User.query.filter_by(id=current_user.id).first()
    progress = user_data.progress

    progress_by_topic = {
        'Link': False,
        'Network': False,
        'Transport': False,
        'Application': False,
    }

    if progress:
        if progress >= 1:
            progress_by_topic['Link'] = True
        if progress >= 2:
            progress_by_topic['Network'] = True
        if progress >= 3:
            progress_by_topic['Transport'] = True
        if progress >= 4:
            progress_by_topic['Application'] = True

    return progress_by_topic


@app.route('/retrieve-accuracy-data')
@login_required
def accuracy_data():
    accuracy_per_topic = {
        'Application': 0,
        'Transport': 0,
        'Network': 0,
        'Link': 0
    }

    topic_of_interest = ['Link', 'Network', 'Transport', 'Application']

    for topic in topic_of_interest:
        mark_per_question = []

        questions_in_topic = Question.query.filter_by(section=topic).all()

        for question in questions_in_topic:
            mark_for_question = Mark.query.filter_by(question_id_fk=question.question_id,
                                                     user_id_fk=current_user.id).one_or_none() if (
                Mark.query.filter_by(question_id_fk=question.question_id).one_or_none()) else 0

            # query will return Mark object for questions that have been attempted
            # otherwise return 0, which we don't want to include
            if not isinstance(mark_for_question, int):
                mark_per_question.append(mark_for_question.mark)

        # If there is no marks in database, this means the user/student has not attempted this quiz, thus, returning 0
        if len(mark_per_question) == 0:
            accuracy_per_topic[topic] = 0
        else:
            mark_for_topic = round(sum(mark_per_question) / len(mark_per_question) * 100, 1)
            accuracy_per_topic[topic] = mark_for_topic

    return accuracy_per_topic


@app.route('/manage-questions', methods=['GET', 'POST'])
@login_required
def manage_questions():
    # check if current user has admin privileges or not - else flash error message

    if not current_user.admin:
        flash('You need admin privileges to access this page! ' +
              'If you are an admin, please logout and login again using your admin account')
        return redirect(url_for('logout'))

    questions_form = ManageQuestionsForm()

    if questions_form.validate_on_submit():
        answer_options = []

        for answers in questions_form.answer_options.data:
            answer_option = Answer(
                answer=answers
            )
            answer_options.append(answer_option)
            db.session.add(answer_option)

        # Commit correct answer as well
        correct_answer = Answer(
            answer=questions_form.correct_answer.data
        )
        db.session.add(correct_answer)
        answer_options.append(correct_answer)

        question = Question(
            section=questions_form.section.data,
            question=questions_form.question.data,
            correct_answer=questions_form.correct_answer.data,
            answer_options=answer_options
        )
        db.session.add(question)

        db.session.commit()

        flash(
            'Question successfully added! To enter another question, enter the new question details and resubmit the form.')
        return (redirect(url_for('manage_questions')))

    return render_template('manage-questions.html', title="Manage Questions", questions_form=questions_form,
                           nav_items=nav_items(current_user))


@app.route('/retrieve-questions')
@login_required
def retrieve_questions():
    topic = str(request.args.get('topic'))

    # Check if we need to implement auto shuffle questions
    questions_array = []

    question_list = Question.query.filter_by(section=topic).all()

    for question in question_list:
        answer_options = []
        answer_list = question.answer_options.all()

        for answer in answer_list:
            answer_option = {
                'answer': answer.answer,
                'id': answer.answer_id
            }
            answer_options.append(answer_option)

        # shuffle answer options so there is no pattern to where the correct answer appears
        random.shuffle(answer_options)

        questionConfig = {
            'questionContent': question.question,
            'questionId': 'question-id-' + str(question.question_id),
            'answerOptions': answer_options
        }
        questions_array.append(questionConfig)

    return jsonify(data=questions_array)


# Expectes to receive information in HTTP body in the following form:
# [{
#   'question_id': 1,
#   'answer_id': 2
# }, {
#   'question_id': 3,
#   'answer_id':4
# }]
@app.route('/submit-quiz', methods=["POST"])
@login_required
def check_answers():
    results = request.get_json()
    mark_per_question = []

    topic_order = ['Link', 'Network', 'Transport', 'Application']

    if User.update_progress(current_user, (topic_order.index(results['topic']) + 1)):
        for result in results['quizData']:

            question = Question.query.filter_by(question_id=result['question_id']).first()
            correct_answer = question.correct_answer
            submitted_answer = result['answer']

            if submitted_answer == correct_answer:
                mark_per_question.append(1)
                mark = Mark(
                    mark=1,
                    question_id_fk=question.question_id,
                    user_id_fk=current_user.id
                )
                db.session.add(mark)
            else:
                mark_per_question.append(0)
                mark = Mark(
                    mark=0,
                    question_id_fk=question.question_id,
                    user_id_fk=current_user.id
                )
                db.session.add(mark)

        db.session.commit()

        percentage_result = sum(mark_per_question) / len(mark_per_question) * 100
        rounded_percentage_result = round(percentage_result, 1)
        return jsonify(data=rounded_percentage_result)

    else:
        error = {
            "message": "You've done this quiz already!"
        }
        return jsonify(error=error)


# convenience method to demo application capability
# unit testing skipped because its not really part of the project
@app.route('/autopopulate')
def autopopulate():
    auto_create_login()
    auto_build_questions()
    flash('Questions and test accounts successfully created')
    return render_template('home.html', title="A journey through the tcp/ip model", nav_items=nav_items(current_user))


@app.route('/autoclear')
def autoclear():
    auto_clear_database()
    flash('Database successfully cleared')
    return render_template('home.html', title="A journey through the tcp/ip model", nav_items=nav_items(current_user))
