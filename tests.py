import unittest

from selenium import webdriver, common

from app import app, db
from app.models import User
from app.forms import RegisterForm, ValidationError

import time

class UserModelCase(unittest.TestCase):
    def setUp(self):
        # use a fake database for testing
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

        user = User(id=1, username='john', progress=2)

        db.session.add(user)

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

    def test_update_progress(self):
        u = User.query.get('1')
        self.assertEqual(2, u.progress)

        # Should return false if we try to re-gress progress (ie update it to a number less than what's currently in database)
        test_update_1 = u.update_progress(1)
        self.assertFalse(test_update_1)
        self.assertEqual(2, u.progress)

        test_update_2 = u.update_progress(3)
        self.assertTrue(test_update_2)
        self.assertEqual(3, u.progress)


class RegisterFormCase(unittest.TestCase):
    def setUp(self):
        # use a fake database for testing
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
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
    driver = None

    def setUp(self):
        # depending on preferred testing driver, you may select from below
        #self.driver = webdriver.Safari()
        self.driver = webdriver.Firefox()

        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()
            alex = User(id=1, username='alex', email='alex@gmail.com', first_name='Alex', last_name='Wyatt', admin=True)
            angel = User(id=2, username='angel', email='angel@gmail.com', first_name='Angel', last_name='Thanur',
                         admin=True)
            alex.set_password('a')
            angel.set_password('a')
            db.session.add(alex)
            db.session.add(angel)

            db.session.commit()
            self.driver.get('http://localhost:5000/autopopulate')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()
            db.drop_all()
            # self.driver.get('http://localhost:5000/autoclear')


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

    def test_login_should_raise_error_if_user_does_not_exist_in_db(self):
    
         self.driver.get('http://localhost:5000/login')
    
         # login should fail if user is not in database
         username = self.driver.find_element_by_id('username')
         username.send_keys('completely new user')
         password = self.driver.find_element_by_id('password')
         password.send_keys('fake password')
    
         self.driver.implicitly_wait(5)
    
         submit = self.driver.find_element_by_id('submit')
         submit.click()
    
         self.driver.implicitly_wait(15)
    
         alert = self.driver.find_element_by_id('flash-alert')
         error_message = "Invalid username or password"
         alert_innerHTML = alert.get_attribute('innerHTML')
         result = error_message in alert_innerHTML
         self.assertTrue(result)

    def test_login_should_raise_error_if_password_is_incorrect(self):
    
         self.driver.get('http://localhost:5000/login')
    
         username = self.driver.find_element_by_id('username')
         password = self.driver.find_element_by_id('password')
    
         username.send_keys('angel@gmail.com')
         password.send_keys('123')
    
         self.driver.implicitly_wait(5)
    
         submit = self.driver.find_element_by_id('submit')
         submit.click()
    
         self.driver.implicitly_wait(15)
    
         alert = self.driver.find_element_by_id('flash-alert')
         error_message = "Invalid username or password"
         alert_innerHTML = alert.get_attribute('innerHTML')
         result = error_message in alert_innerHTML
         self.assertTrue(result)

    def test_login_should_not_raise_error_if_user_exists_in_db_and_correct_pw_provided(self):
    
         self.driver.get('http://localhost:5000/login')
    
         username = self.driver.find_element_by_id('username')
         password = self.driver.find_element_by_id('password')
    
         username.send_keys('angel')
         password.send_keys('a')
    
         self.driver.implicitly_wait(10)
    
         submit = self.driver.find_element_by_id('submit')
         submit.click()
    
         self.driver.implicitly_wait(15)
    
         try:
             alert = self.driver.find_element_by_id('flash-alert')
             self.fail("Alert should not be shown for successful login")
         except:
             pass




if __name__ == '__main__':
    unittest.main(verbosity=2)
