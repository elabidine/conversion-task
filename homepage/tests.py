from django.test import TestCase
from django.http import HttpRequest

from homepage.views import home_page


from .base_data import app_name


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        tab_label = app_name
        self.assertIn(f"<title>{tab_label}</title>", html)
