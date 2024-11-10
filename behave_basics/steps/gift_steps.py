

from selenium.webdriver.support import expected_conditions as EC
from behave import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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
    sleep(3)

@step('Verify header of the page contains {item}')
def verify_header(context, item):
    xpath_h1 = "//h1"
    xpath_span = "//span[@class='h-text-bs h-display-flex h-flex-align-center h-text-grayDark h-margin-l-x2']"
    h1_elements = context.browser.find_elements(By.XPATH, xpath_h1)
    span_elements = context.browser.find_elements(By.XPATH, xpath_span)

    if span_elements:
        span_text = span_elements[0].text
        if span_text:
            print(f"Search \'{item}\' is present in header \'{span_text}\': {item.lower() in span_text.lower()}")

    if h1_elements:
        h1_text = h1_elements[0].text
        if h1_text:
            print(f"Search \'{item}\' is present in header \'{h1_text}\': {item.lower() in h1_text.lower()}")


    # solution 2
    xpaths = [xpath_h1, xpath_span]

    for xpath in xpaths:
        found_elements = context.browser.find_elements(By.XPATH, xpath)
        if found_elements:
            element_text = found_elements[0].text
            if element_text:
                print(f"Search \'{item}\' is present in header \'{element_text}\': {item.lower() in element_text.lower()}")















