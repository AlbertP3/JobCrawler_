#!flask/bin/python
import os
import unittest
import app
from app import app, db, User
from flask_login import current_user
from Crawler import  NoFluffJobs

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        self.app = app.test_client()
        db.create_all()
        user1 = User(username="asdasd", password="asdasd")
        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Sprawdzanie czy strony się ładują
    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_registr(self):
        response = self.app.get('register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_offers(self):
        response = self.app.get('offers', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_search(self):
        response = self.app.get('register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('logout', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    # Sprawdzanie zawartości stron

    def test_index_values(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Zarejestruj', response.data)
        self.assertIn(b'Zaloguj', response.data)
        self.assertIn(b'Witamy', response.data)

    def test_register_values(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertIn(b'Confirm Password', response.data)
        self.assertIn(b'username', response.data)
        self.assertIn(b'Password', response.data)

    def test_login_values(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'username', response.data)
        self.assertIn(b'Password', response.data)

    # def test_search_values(self):
    #     response = self.app.get('/search', follow_redirects=True)
    #     self.assertIn(b'keyword', response.data)
    #     self.assertIn(b'miasta', response.data)
    #
    #
    # def test_user_creation_ok(self):
    #     #Najczęstrze hasła 2019 wg. wikipedii + kilka polskich znaków
    #     passwords = ['123456','123456789','qwerty','password','12\34567','12345678','12345','iloveyou','111111','123123','abc123','qwerty123','q2w3e4r','admin','qwertyuiop','654321','555555','lovely','7777777','welcome','888888','princess','dragon','password1' ]
    #     usernames = ['Yasd69','asdw','aFERWGBTG','eabhffr234@asd']
    #     for username in usernames:
    #         for password in passwords:
    #             user = User(username = username, password = password)
    #             db.session.add(user)
    #             db.session.commit()
    #             self.assertEqual(user.username, username)
    #             del user
    #             #self.assertIn(user, db.session)
    #
    # def test_login_logout(client):
    #     """Make sure login and logout works."""
    #
    #     rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])
    #     assert b'You were logged in' in rv.data
    #

if __name__ == '__main__':
    unittest.main()