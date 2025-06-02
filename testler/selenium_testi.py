import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class SeleniumFrontendTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def test_anasayfa_baslik_var_mi(self):
        # Sunucu başlasın diye bekle
        time.sleep(3)

        self.driver.get("http://127.0.0.1:5000")
        time.sleep(1)

        baslik = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertIn("Haberler", baslik.text)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
