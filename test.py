from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Edge("C:\\Users\\blueg\\Documents\\Workspace Python\\JobCrawler_\\msedgedriver.exe")
driver.get("http://127.0.0.1:5000/")
# click register link
register_field = driver.find_element_by_link_text("Zarejestruj się")
register_field.click()
register_site = driver.current_url
#check if site transition OK
assert register_site == "http://127.0.0.1:5000/register", register_site
driver.get(register_site)

# begin testing registration form
username_field = driver.find_elements_by_xpath("/html/body/nav/ul/form/input[2]")
password_field = driver.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
confirm_password_field = driver.find_element_by_xpath("/html/body/nav/ul/form/input[4]")
submit_button = driver.find_element_by_xpath("/html/body/nav/ul/form/input[5]")
#registration form test no.1
# ToDo

# GoTo login form site
driver.get("http://127.0.0.1:5000/")
login_field = driver.find_element_by_link_text("Zaloguj się")
login_field.click()
login_site = driver.current_url
assert login_site == "http://127.0.0.1:5000/login", login_site
driver.get(login_site)
# begin testing login form
username_field1 = driver.find_elements_by_xpath("/html/body/nav/ul/form/input[2]")
password_field1 = driver.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
submit_button1 = driver.find_element_by_xpath("/html/body/nav/ul/form/input[4]")

# login form test no. 1
# Todo

# GoTo search site
driver.get("http://127.0.0.1:5000/search")
keyword_field = driver.find_element_by_xpath("/html/body/nav/ul/form/input[2]")
location_field = driver.find_element_by_xpath("/html/body/nav/ul/form/input[3]")
search_button = driver.find_element_by_xpath("/html/body/nav/ul/form/input[4]")
# begin testing search
# ToDo

# ------
driver.close()



