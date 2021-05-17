from app.models import User, Answer, Question, Mark
from flask import flash

from app import db


# ['label', 'icon', 'link']
def nav_items(current_user):
    relevant_nav_items = []
    home = ['Home', 'house', 'home']
    login = ['Login', 'door-open', 'login']
    logout = ['Logout', 'door-closed', 'logout']
    progress = ['Progress', 'check2-square', 'progress']
    link = ['Link', 'link', 'link']
    network = ['Network', 'hdd-network', 'network']
    transport = ['Transport', 'truck', 'transport']
    application = ['Application', 'window', 'application']
    manage_questions = ['Manage Questions', 'question-square-fill', 'manage_questions']

    # default nav items
    relevant_nav_items.extend((home, login, progress, link))

    if current_user:
        if current_user.is_authenticated:
            # replace login link with logout link if user is authenticated
            relevant_nav_items = [logout if item == login else item for item in relevant_nav_items]

            if current_user.admin:
                # give admin users access to manage questions link and all other menus
                relevant_nav_items.extend((network, transport, application, manage_questions))
            else:
                progress = current_user.progress if current_user.progress else 0

                if progress:
                    if progress >= 1:
                        relevant_nav_items.append(network)
                    if progress >= 2:
                        relevant_nav_items.append(transport)
                    if progress >= 3:
                        relevant_nav_items.append(application)

    return relevant_nav_items


def auto_build_questions():
    questions = [{
        'question': 'What is Hamming Code used for?',
        'section': 'Link',
        'correctAnswer': 'Its used to make sure we are sending over the correct data',
        'answerOptions': [
            'Its a recipe to make ham sandwich',
            'It\'s a special secret code that is used by spies to communicate',
            'It\'s used to make sure the computers are linked together'
        ]
    }, {
        'question': 'How do computers know if they\'ve received information in the correct order?',
        'section': 'Link',
        'correctAnswer': 'Data is grouped into frames and there is additional data in the frames that allows the computer know if its in the correct order or not',
        'answerOptions': [
            'Computers are very smart and knows by itself',
            'The bytes are ordered so the computer can tell if a byte has been sent out of order',
            'There is no way of checking if information has arrived in the correct order or not. So the computers don\'t know'
        ]
    }, {
        'question': 'The Link Layer is the ______ layer in the TCP/IP Model',
        'section': 'Link',
        'correctAnswer': 'Lowest',
        'answerOptions': [
            'Highest',
            'Best',
            'Worst'
        ]
    }, {
        'question': 'Why do networks need to send data in packets?',
        'section': 'Network',
        'correctAnswer': 'To abide by message size limitations and help with routing',
        'answerOptions': [
            'Because networks find it easier to send smaller messages',
            'To provide the lazy networks with more jobs to do!',
            'It\'s a trick question! They don\'t :)'
        ]
    }, {
        'question': 'How do network nodes know where to send their next packet?',
        'section': 'Network',
        'correctAnswer': 'By first exchanging a routing table with neighbour nodes to map out the network',
        'answerOptions': [
            'Using the magical powers of complex maths algorithms',
            'It\'s mostly just "guess and check" - eventually they\'ll get the right answer',
            'They look at a network diagram and follow the easiest path from that'
        ]
    }, {
        'question': 'What is subnet masking?',
        'section': 'Network',
        'correctAnswer': 'A method of labelling IPv4 addresses that avoids wasted addressing bits on small networks',
        'answerOptions': [
            'When one network pretends to be a different one',
            'A way for computers to know who is on their network',
            'It makes sure data gets from point A to point B'
        ]
    }, {
        'question': 'What is a port?',
        'section': 'Transport',
        'correctAnswer': 'a 16-bit positive integer that can be used to uniquely identify which application needs which message',
        'answerOptions': [
            'Wine',
            '...not wine?',
            'It\'s like the USB of networking probably'
        ]
    }, {
        'question': 'How can we ensure a reliable connection is established?',
        'section': 'Transport',
        'correctAnswer': 'Sequence numbers, acknowledgement, and calculating the expected round-trip time of messages',
        'answerOptions': [
            'Make sure all the cables are laid flat with no EMR interference',
            'Resend the same message a few times to reduce the chance of errors or message loss'
        ]
    }, {
        'question': 'Flow control uses _____ to protect a receiver from being overwhelmed by messages',
        'section': 'Transport',
        'correctAnswer': 'a flow control window',
        'answerOptions': [
            'a congestion control window',
            'trial and error',
            'intuition and empathy'
        ]
    }, {
        'question': 'The Application Layer is the ______ layer in the TCP/IP Model',
        'section': 'Application',
        'correctAnswer': 'Highest',
        'answerOptions': [
            'Lowest',
            'Best',
            'Worst'
        ]
    }, {
        'question': 'Which of the below protocols would you use if you want to make sure that your communications are secure?',
        'section': 'Application',
        'correctAnswer': 'SSH',
        'answerOptions': [
            'HTTP',
            'Telnet',
            'SNMP'
        ]
    }, {
        'question': 'What does HTTP stand for?',
        'section': 'Application',
        'correctAnswer': 'HyperText Transfer Protocol',
        'answerOptions': [
            'HostText Tranmission Protocol',
            'Heaps of Text Transferal Process',
            'HyperText Transferance Process'
        ]
    }]

    for question in questions:
        answer_options = []

        for answer in question['answerOptions']:
            answer_option = Answer(answer = answer)
            answer_options.append(answer_option)
            db.session.add(answer_option)


        correct_answer = Answer(answer=question['correctAnswer'])
        answer_options.append(correct_answer)
        db.session.add(correct_answer)


        question_to_commit = Question(
            section = question['section'],
            question = question['question'],
            correct_answer= question['correctAnswer'],
            answer_options=answer_options
        )

        db.session.add(question_to_commit)
        db.session.commit()


def auto_create_login():
    test_user = User(
        first_name="John",
        last_name="Smith",
        username="test",
        email="John@gmail.com",
        progress=0
    )
    test_user.set_password("test")
    db.session.add(test_user)

    test_admin_user = User(
        first_name="Jane",
        last_name="Smith",
        username="admin",
        email="jane@gmail.com",
        admin=True
    )
    test_admin_user.set_password("admin")
    db.session.add(test_admin_user)

    db.session.commit()

def auto_clear_database():
    db.session.query(User).delete()
    db.session.query(Question).delete()
    db.session.query(Answer).delete()
    db.session.query(Mark).delete()
    db.session.commit()
