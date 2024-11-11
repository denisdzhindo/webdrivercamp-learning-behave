from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from behave import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from behave_basics.components.base import Base
from selenium.webdriver.common.action_chains import ActionChains


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
    sleep(1)

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

@step('Select {option} in {section} section')
def select_option(context, option, section):
    option = context.browser.find_elements(By.XPATH, f"//span[text()='{option}']")
    section = context.browser.find_elements(By.XPATH, f"//span[text()='{section}']")
    section_element = section[0]
    context.browser.execute_script("arguments[0].scrollIntoView(true);", section_element)
    option[0].click()
    sleep(2)


@step('Collect all items on the first page into {context_variable}')
def collected_items(context, context_variable):
    context.collected_items = []
    title_list = []
    price_list = []

    # Get initial page height and scroll until all elements are loaded
    last_height = context.browser.execute_script("return document.body.scrollHeight")

    scroll = 0
    while True:
        # Scroll by a fixed amount (in pixels)
        context.browser.execute_script("window.scrollBy(0, 1500);")
        sleep(2)  # Give time for content to load

        # Get the new height and check if it matches the previous height
        new_height = context.browser.execute_script("return document.body.scrollHeight")
        scroll += 1
        # print(f"Scroll {scroll} - New Height: {new_height}, Last Height: {last_height}")

        if new_height == last_height:
            # print("No new content loaded, stopping scroll.")
            break  # Exit if no new content is added
        last_height = new_height  # Update the last height to continue scrolling

    try:
        # Wait for all elements to be present (change to 'presence_of_all_elements_located' if necessary)
        titles = WebDriverWait(context.browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='styles_truncate__Eorq7 sc-4d32bc34-0 lbqtUS' and @title]"))
        )
        # print(f"Found {len(titles)} titles.")


        # Collect the titles
        for title_element in titles:
            title_list.append(title_element.text)

    except TimeoutException:
        print("Timeout waiting for elements to be visible.")

    try:
        # Wait for all elements to be present (change to 'presence_of_all_elements_located' if necessary)
        prices = WebDriverWait(context.browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[@data-test='current-price']/span"))
            )
        #print(f"Found {len(prices)} prices.")
        min_prices = []
        for price in prices:
            price = price.text.replace("$", " ").replace("-", " ")
            price = price.split()
            if len(price) == 2:
                price_1 = float(price[0])
                price_2 = float(price[1])
                min_price = min(price_1, price_2)
            else:
                min_price = float(price[0])
            min_prices.append(min_price)
        #collect min_prices:

        for price_element in min_prices:
            price_list.append(price_element)

    except TimeoutException:
        print("Timeout waiting for elements to be visible.")

    context.collected_items = list(zip(title_list, price_list))


@step('verify all collected results\' price is {condition}')
def collected_result(context, condition):
    mistakes = []
    condition = condition.split(" ")
    operator, value = condition[0], float(condition[1])  # Cast value to float for comparison

    for item in context.collected_items:
        try:
            price = float(item[1])

            # Check for mistakes:
            if operator == "<" and price >= value:  # Mistake if price is >= value when it should be < value
                mistakes.append(item)
            elif operator == ">" and price <= value:  # Mistake if price is <= value when it should be > value
                mistakes.append(item)
            elif operator == "==" and price != value:  # Mistake if price is not equal to value
                mistakes.append(item)
            elif operator == "<=" and price > value:  # Mistake if price is > value when it should be <= value
                mistakes.append(item)
            elif operator == ">=" and price < value:  # Mistake if price is < value when it should be >= value
                mistakes.append(item)

        except ValueError:
            mistakes.append(f"Invalid price format in item: {item}")

    if mistakes:
        print(f"Mistakes:")
        for mistake in mistakes:
            print(mistake)
    else:
        print("All prices meet the condition.")











'''
@step('verify all collected results\' price is {condition}')
def collected_result(context, condition):
    condition = condition.split(" ")
    value, operator = int(condition[1]), condition[0]
    pages = context.browser.find_elements(By.XPATH, "//span[@class='sc-9572954b-0 durrmk']")
    pages = pages[0].text.replace("page", '').split("of")
    current_page = int(pages[0])
    if not current_page:
        raise ValueError('No way to define the current page')
    last_page = int(pages[-1])
    if not current_page:
        raise ValueError('No way to define the last page')

    while current_page < last_page:
        # update the current page:
        pages = context.browser.find_elements(By.XPATH, "//span[@class='sc-9572954b-0 durrmk']")
        pages = pages[0].text.replace("page", '').split("of")

        current_page = int(pages[0])
        if not current_page:
            raise ValueError ('No way to define the current page')

        last_page = int(pages[-1])
        if not current_page:
            raise ValueError ('No way to define the last page')

        #context.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        item_prices = context.browser.find_elements(By.XPATH, "//span[@data-test='current-price']/span")
        print(current_page, len(item_prices))

        next_page_button = context.browser.find_elements(By.XPATH, "//button[@aria-label='next page' and @class='sc-ddc722c0-0 sc-437df23b-0 cJZYiB gONjdr sc-9572954b-2 hhQrrP']")
        if not next_page_button:
            raise ValueError('No way to define the next page')

        sleep(4)
        next_page_button[0].click()
        sleep(2) 
'''






























