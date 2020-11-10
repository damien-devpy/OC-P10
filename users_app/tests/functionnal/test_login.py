from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from users_app.models import User


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        pwd = make_password("random_password")
        new_user = User.objects.create(email="nouvel.user@mail.com",
                                       password=pwd)
        new_user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.CSS_SELECTOR, "#connect").click()
        mail = self.selenium.find_element(By.CSS_SELECTOR, "#id_username")
        mail.send_keys("nouvel.user@mail.com")
        password = self.selenium.find_element(By.CSS_SELECTOR, "#id_password")
        password.send_keys("random_password", Keys.ENTER)
        message = WebDriverWait(self.selenium, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert")))
        assert "Vous êtes maintenant connecté" in message.text
