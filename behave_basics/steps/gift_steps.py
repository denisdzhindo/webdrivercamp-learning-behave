from behave import *
from time import sleep
from selenium.webdriver.common.by import By

@step('Navigate to {url}')
def navigate_url(context, url):
    context.browser.get(url)
    sleep(1)

@step('Search for {search_item}')
def search_for_item(context, search_item):
    search_field = context.browser.find_element(By.XPATH,"//input[@class='sc-1c2974c-2 jGwNnC']")
    search_field.send_keys(search_item)
    button_magnifier = context.browser.find_element(By.XPATH, "//button[@class='sc-1c2974c-3 bsiIIZ']")
    button_magnifier.click()
    sleep(5)
