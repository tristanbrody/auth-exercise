from unittest import TestCase

from flask import url_for, request, json
from app import app, LOGIN_ROOT
from models import db, User, Feedback
from forms import LoginForm

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class AuthViewsTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        db.session.commit()
        self.app = app.test_client()
        with app.app_context(), app.test_request_context():
            test_data = {'username': 'hungry242', 'password': 'supersecure', 'email': 'jason@yahoo.com', 'first_name': 'Jason', 'last_name': 'Score'}
            self.register(test_data)

    def tearDown(self):
        db.session.rollback()
    
    def test_registration(self):
        with app.app_context(), app.test_request_context():
            test_data = {'username': 'hungry242', 'password': 'supersecure', 'email': 'jason@yahoo.com', 'first_name': 'Jason', 'last_name': 'Score'}
            response = self.register(test_data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/users/hungry242')

    def test_login(self):
        with app.app_context(), app.test_request_context():
            test_data = {
                'username': 'hungry242', 'password': 'supersecure'
            }
            response = self.login(test_data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/users/hungry242')
            
    def test_logout(self):
        with app.app_context(), app.test_request_context():
            test_data = {
                'username': 'pancakes123', 'password': 'donuts123'
            }
            self.login(test_data)
            response = self.logout()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/')
    # helper methods below

    def register(self, data):
        return self.app.post('/register', data=data)

    def login(self, data):
        return self.app.post(LOGIN_ROOT, data=data)

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)