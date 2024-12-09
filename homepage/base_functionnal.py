from unittest import TestCase

# from selenium import webdriver

from unittest import TestCase

BaseCase = TestCase

_browser = [None]

browser = None


# def setUpModule():

#     _browser[0] = webdriver.Firefox()


# def tearDownModule():

#     _browser[0].quit()


app_name = "FlexUp"

test_content = f"Welcome to {app_name}".lower()

url = "http://localhost:8000/"


class TestPage(TestCase):

    def setUp(self):
        global browser
        browser = _browser[0]

    def test_server_is_up_app_name_in_title(self):
        browser.get(url)
        self.assertIn(app_name, browser.title)

    def test_message_in_welcome_page(self):
        browser.get(url)
        self.assertIn(test_content, browser.page_source.lower())
