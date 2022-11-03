from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


class Client(object):
    driver: WebDriver

    @classmethod
    def init_web_driver(cls):
        """获取driver"""
        from selenium import webdriver
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0})
        chrome_options.add_argument('start-maximized')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        cls.driver = webdriver.Chrome(options=chrome_options)
        return cls.driver


if __name__ == "__main__":
    Client.init_web_driver()
