#TODO add tests

from unittest import TestCase

from flask import url_for, request
from app import app
from models import db, User, Feedback

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise_test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class AuthViewsTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        user1 = User(username="pancakes123", password="donuts123", email="fake@fake.org", first_name="Daniel Day", last_name="Lewis")
        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        
        User.query.delete()
        db.session.commit()

    def test_registration(self):
        with app.app_context(), app.test_request_context():
            response = self.register('hungry242', 'supersecure', 'jason@yahoo.com', 'Jason', 'Score')
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        with app.app_context(), app.test_request_context():
            response = self.login('fake@fake.org', 'donuts123')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/users/pancakes123')
            
    def test_logout(self):
        with app.app_context(), app.test_request_context():
            self.login('fake@fake.org', 'donuts123')
            response = self.logout()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/')
    # helper methods below

    def register(self, username, password, email, first_name, last_name):
        return self.app.post(url_for('register', data=dict(username=username, password=password,email=email,first_name=first_name,last_name=last_name),follow_redirects=True))

    def login(self, username, password):
        return self.app.get(url_for('show_login', data=dict(username=username, password=password)))

    def logout(self):
        return self.app.post(url_for('process_logout'), follow_redirects=True)