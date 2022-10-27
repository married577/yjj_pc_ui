# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"


class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        cls.driver = cls.com.get_driver()
        cls.loginpage = LoginPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # 正确的账号，正确的密码登录
    def test_01_login_loginpag(self):
        result = self.loginpage.login_homepage(username, password)
        assert result


if __name__ == "__main__":
    pytest.main(["-v", "test_login.py"])
