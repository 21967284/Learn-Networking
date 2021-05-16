from logging import log
import time, os
import unittest
from wtforms.validators import ValidationError
from app import app, db
from app.models import User, Question, Mark
from app.forms import RegisterForm
from selenium import webdriver, common

class UserModelCase(unittest.TestCase):
    def setUp(self):
        # use a fake database for testing
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()

        user = User(id=1, username='john')
        question1 = Question(question_id=1)
        question2 = Question(question_id=2)
        question3 = Question(question_id=3)
        question4 = Question(question_id=4)
        mark = Mark(mark=1, question_id_fk=1, user_id_fk=1)

        db.session.add(user)
        db.session.add(question1)
        db.session.add(question2)
        db.session.add(question3)
        db.session.add(question4)
        db.session.add(mark)

        db.session.commit()

    def tearDown(self):
        # clear the database, then delete it
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        # create an arbitraty user with password 'test'
        u = User.query.get('1')
        u.set_password('test')
        # make sure check_passsword returns true iff both passwords match
        self.assertFalse(u.check_password('fail'))
        self.assertTrue(u.check_password('test'))

    def test_retrieve_results(self):
        pass

    def test_retrieve_progress(self):
        pass

class RegisterFormCase(unittest.TestCase):
    def setUp(self):
        # use a fake database for testing
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()
        # create an entry into the database to ensure uniqueness tests work
        u = User(username='unique', email='unique@email.com')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        # clear the database, then delete it
        db.session.remove()
        db.drop_all()

    def test_validate_username(self):
        # ensure identical usernames cannot be entered
        same = RegisterForm.username
        same.data = 'unique'
        with self.assertRaises(ValidationError):
            RegisterForm.validate_username(self, same)

        # ensure different usernames will pass the validation
        different = RegisterForm.username
        different.data = 'different'
        try:
            RegisterForm.validate_username(self, different)
        except ValidationError:
            self.fail("validate_username() raised ValidationError unexpectedly!")

    def test_validate_email(self):
        # ensure identical emails cannot be entered
        same = RegisterForm.email
        same.data = 'unique@email.com'
        with self.assertRaises(ValidationError):
            RegisterForm.validate_email(self, same)

        # ensure different emails will pass the validation
        different = RegisterForm.username
        different.data = 'different@email.com'
        try:
            RegisterForm.validate_email(self, different)
        except ValidationError:
            self.fail("validate_email() raised ValidationError unexpectedly!")

class SystemTest(unittest.TestCase):
    driver=None

    def setUp(self):
        self.driver = webdriver.Firefox()

        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
            db.create_all()
            alex = User(id=1,username='alex',email='alex@gmail.com',first_name='Alex',last_name='Wyatt',admin=True)
            angel = User(id=2,username='angel',email='angel@gmail.com',first_name='Angel',last_name='Thanur',admin=True)
            db.session.add(alex)
            db.session.add(angel)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()
            db.drop_all()

    def test_register(self):
        alex = User.query.get(1)
        self.assertEqual(alex.first_name, 'Alex', msg="user exists in db")
        
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(5)

        # enter a new user into the registration form
        first_name = self.driver.find_element_by_id('firstname')
        first_name.send_keys('John')
        last_name = self.driver.find_element_by_id('lastname')
        last_name.send_keys('Doe')
        username_field = self.driver.find_element_by_id('username')
        username_field.send_keys('johndoe')
        email_field = self.driver.find_element_by_id('email')
        email_field.send_keys('johndoe@gmail.com')
        password = self.driver.find_element_by_id('password')
        password.send_keys('password')
        conf_password = self.driver.find_element_by_id('confirmpassword')
        conf_password.send_keys('password')

        time.sleep(1)
        self.driver.implicitly_wait(5)

        # submit the form
        submit = self.driver.find_element_by_id('submit')
        submit.click()

        #check login success
        self.driver.implicitly_wait(5)
        time.sleep(1)
        try:
            logout = self.driver.find_element_by_partial_link_text('Logout')
        except common.exceptions.NoSuchElementException:
            self.fail("could not find Logout button!")

if __name__ == '__main__':
    unittest.main(verbosity=2)