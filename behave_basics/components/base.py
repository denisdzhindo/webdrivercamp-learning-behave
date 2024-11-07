from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class Base:
    BASE_VAR = "Base Var"

    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        wait = WebDriverWait(self.driver, 10)
        locator = wait.until(expected_conditions.element_to_be_clickable(locator))
        locator.click()


