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
    #s
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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import string

class RegFormTestClass:

    def __init__(self, driver):
        # go to register form site
        register_field = driver.find_element_by_link_text("Zarejestruj się")
        register_field.click()
        register_site = driver.current_url
        driver.get(register_site)

        self.username = driver.find_element_by_xpath("/html/body/nav/ul/form/input[2]")
        self.password = driver.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
        self.confirm = driver.find_element_by_xpath("/html/body/nav/ul/form/input[4]")
        self.submit = driver.find_element_by_xpath("/html/body/nav/ul/form/input[5]")
        self.register_site = register_site
        self.driver = driver

    # try transition to register page
    def reg_form_test(self):
        assert self.register_site == "http://127.0.0.1:5000/register", self.register_site
        return "Transition to register form page: OK"

    # try submit all blanks
    def blank_all_test(self):
        self.cleanup()
        self.submit.click()
        assert self.driver.current_url == self.register_site
        print("Form check (all blanks): OK")

    # try submit blank password only
    def blank_pass_test(self):
        self.cleanup()
        self.username.send_keys("testUser",random.randint(100, 5000))
        assert self.driver.current_url == self.register_site
        print("Form check (blank password): OK")

    # try submit blank username only
    def blank_username_test(self):
        self.cleanup()
        self.password.send_keys("qwerty123")
        assert self.driver.current_url == self.register_site
        print("Form check (blank username): OK")

    # try correct fill of form
    def correct_form_test(self,id_username, id_password):
        self.cleanup()
        self.username.send_keys(id_username)
        self.password.send_keys(id_password)
        self.confirm.send_keys(id_password)
        self.submit.click()
        assert self.driver.current_url != self.register_site
        print("Form check (final check): OK")

    # cleanup fields
    def cleanup(self):
        self.username.clear()
        self.password.clear()
        self.confirm.clear()


class LoginFormTestClass:

    def __init__(self, driver2):
        login_field = driver2.find_element_by_link_text("Zaloguj się")
        login_field.click()
        login_site = driver2.current_url
        driver2.get(login_site)

        self.username = driver2.find_element_by_xpath("/html/body/nav/ul/form/input[2]")
        self.password = driver2.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
        self.submit = driver2.find_element_by_xpath("/html/body/nav/ul/form/input[4]")
        self.login_site = login_site
        self.driver2 = driver2

    # test submit all blank
    def blank_all(self):
        self.cleanup()
        assert self.driver2.current_url == self.login_site
        print("Form Check (all blank): OK")

    #test submit password only
    def blank_username(self):
        self.cleanup()
        self.password.send_keys("qwerty123")
        self.submit.click()
        assert self.driver2.current_url == self.login_site
        print("Form Check (password only): OK")

    # test submit username only
    def blank_password(self):
        self.cleanup()
        self.username.send_keys("TestUser")
        self.submit.click()
        assert self.driver2.current_url == self.login_site
        print("Form Check (username only): OK")

    # test login
    def login_test(self, id_name, id_password):
        self.cleanup()
        self.username.send_keys(id_name)
        self.password.send_keys(id_password)
        self.submit.click()
        assert self.driver2.current_url != self.login_site
        print("Form Check (login): OK")

    #cleanup fields
    def cleanup(self):
        self.username.clear()
        self.password.clear()


class SearchTestClass:

    def __init__(self, driver3):
        search_site = driver3.current_url
        driver3.get(search_site)
        self.keyword = driver3.find_element_by_xpath("/html/body/nav/ul/form/input[2]")
        self.location = driver3.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
        self.search = driver3.find_element_by_xpath("/html/body/nav/ul/form/input[4]")
        self.search_site = search_site
        self.driver3 = driver3

    # enter random input into fields
    def random_input(self):

        # create random string of lenght i
        def random_string(string_length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(string_length))

        self.cleanup()
        self.location.send_keys(random_string(10))
        self.keyword.send_keys(random_string(12))
        self.search.click()
        link_check = self.driver3.find_element_by_tag_name("h4")
        assert link_check
        print("Random input test: OK")

    # enter logical values
    def standardInput(self):
        self.cleanup()
        self.location.send_keys("Kraków")
        self.keyword.send_keys("Python")
        self.search.click()
        link_check = self.driver3.find_element_by_tag_name("h4")
        assert link_check
        print("Logical input test: OK")

    # cleanup fields
    def cleanup(self):
        self.keyword.clear()
        self.location.clear()


# initialize webdriver
driver = webdriver.Edge("C:\\Users\\blueg\\Documents\\Workspace Python\\JobCrawler_\\msedgedriver.exe")

# webdriver config
driver.get("http://127.0.0.1:5000/")

# create mock up user
mock_name = "testUser" + str(random.randint(200, 30000))
mock_pass = "qwerty123"
print(mock_name," ", mock_pass)

# conduct tests - register form
print("== Testing Register Form ==")
RegFormTestClass(driver).reg_form_test()
RegFormTestClass(driver).blank_all_test()
RegFormTestClass(driver).blank_pass_test()
RegFormTestClass(driver).blank_username_test()
RegFormTestClass(driver).correct_form_test(mock_name, mock_pass)

# webdriver config - main page
driver.get("http://127.0.0.1:5000/")

# conduct tests - login form
print("== Testing Login Form ==")
LoginFormTestClass(driver).blank_all()
LoginFormTestClass(driver).blank_username()
LoginFormTestClass(driver).blank_password()
LoginFormTestClass(driver).login_test(mock_name, mock_pass)

# webdriver config - search page
driver.get("http://127.0.0.1:5000/search")

# conduct tests - search form <- must be logged first
print("== Testing Search Form ==")
SearchTestClass(driver).random_input()
SearchTestClass(driver).standardInput()

print("TESTING FINISHED SUCCESSFULLY")


if __name__ == '__main__':
    unittest.main()