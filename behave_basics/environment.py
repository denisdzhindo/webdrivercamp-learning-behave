from selenium import webdriver

def before_scenario(context, scenario):
    # Set up the browser (make sure you have the appropriate WebDriver installed)
    context.browser = webdriver.Chrome()  # You can replace Chrome() with Firefox(), etc.
    context.browser.maximize_window()  # Optional: to make the window full-screen

def after_scenario(context, scenario):
    # After each scenario, close the browser
    context.browser.quit()

