from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import os
import signal
import time

class WebBrowserController:
    def __init__(self, callback=None):
        nothing_func = lambda driver, wait: None
        self.__callback = callback if callable(callback) else nothing_func

    def initialize(self, timeout=10):
        options = webdriver.ChromeOptions()
        self.__driver = webdriver.Remote(
            command_executor=os.getenv('SELENIUM_URL'),
            options=options,
        )
        self.__wait = WebDriverWait(self.__driver, timeout)

    def execute(self, callback=None, *args, **kwargs):
        if callable(callback):
            callback(self.__driver, self.__wait, *args, **kwargs)
        else:
            self.__callback(self.__driver, self.__wait, *args, **kwargs)

    def finalize(self):
        self.__driver.quit()

class ProcessStatus:
    def __init__(self):
        self.__status = True

    def change_status(self, signum, frame):
        self.__status = False

    def get_status(self):
        return self.__status

if __name__ == '__main__':
    process_status = ProcessStatus()
    # setup signal
    signal.signal(signal.SIGTERM, process_status.change_status)
    signal.signal(signal.SIGINT, process_status.change_status)

    # define the test function
    def test_func(driver, wait):
        # access to google
        driver.get('https://google.com')
        # search "wikipedia"
        driver.find_element(By.NAME, 'q').send_keys('wikipedia' + Keys.RETURN)
        # wait until the search results are displayed
        result = wait.until(presence_of_element_located(
            (By.CSS_SELECTOR, 'h3')
        ))
        text = result.get_attribute('textContent')
        print(text)

    wbc = WebBrowserController(test_func)
    wbc.initialize()

    # execute at once
    wbc.execute()

    # main loop
    while process_status.get_status():
        time.sleep(1)

    wbc.finalize()
