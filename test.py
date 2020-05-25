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

    # try correct fill of form
    def correct_form_testFail(self, id_username, id_password):
        self.cleanup()
        self.username.send_keys(id_username)
        self.password.send_keys(id_password)
        self.confirm.send_keys(id_password)
        self.submit.click()
        assert self.driver.current_url == self.register_site
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

    def login_testFail(self, id_name, id_password):
        self.cleanup()
        self.username.send_keys(id_name)
        self.password.send_keys(id_password)
        self.submit.click()
        assert self.driver2.current_url == self.login_site
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
        x = "mockuup value"
        print("Logical input test: OK")

    # cleanup fields
    def cleanup(self):
        self.keyword.clear()
        self.location.clear()


# initialize webdriver
driver = webdriver.Edge("C:\\Users\\blueg\\Documents\\Workspace Python\\JobCrawler_\\msedgedriver.exe")
driver.encoding = "UTF-8"

# webdriver config
driver.get("http://127.0.0.1:5000/")

# create mock up user
mock_name = "testUser" + str(random.randint(200, 30000))
mock_pass = "qwerty123"
emoji_name = "😁JO😁"
emoji_pass = "😍JO😍"
pl_name = "ąźćż"
pl_pass = "ńłśóę"
print(mock_name," ", mock_pass)

# conduct tests - register form
print("== Testing Register Form ==")
RegFormTestClass(driver).reg_form_test()
RegFormTestClass(driver).blank_all_test()
RegFormTestClass(driver).blank_pass_test()
RegFormTestClass(driver).blank_username_test()
RegFormTestClass(driver).correct_form_test(mock_name, mock_pass)
#RegFormTestClass(driver).correct_form_test(emoji_name, emoji_pass)
RegFormTestClass(driver).correct_form_testFail(pl_name, pl_pass)

# webdriver config - main page
driver.get("http://127.0.0.1:5000/")

# conduct tests - login form
print("== Testing Login Form ==")
LoginFormTestClass(driver).blank_all()
LoginFormTestClass(driver).blank_username()
LoginFormTestClass(driver).blank_password()
LoginFormTestClass(driver).login_test(pl_name, pl_pass)
driver.find_element_by_link_text("Wyloguj się").click()
#LoginFormTestClass(driver).login_test(emoji_name, emoji_pass)
LoginFormTestClass(driver).login_test(mock_name, mock_pass)

# conduct tests - search form <- must be logged first
print("== Testing Search Form ==")
driver.get("http://127.0.0.1:5000/search")
SearchTestClass(driver).random_input()
driver.get("http://127.0.0.1:5000/search")
SearchTestClass(driver).standardInput()

print("TESTING FINISHED SUCCESSFULLY")

