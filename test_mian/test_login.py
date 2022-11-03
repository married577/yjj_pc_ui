# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume
from pages.homePage import HomePage
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"
errer_password = "654321"


class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        cls.driver = cls.com.get_driver()
        cls.loginpage = LoginPage(cls.driver)
        cls.home = HomePage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.fixture()
    def login_out(self):
        self.home.log_out()  # 退出登录

    # 正确的账号，正确的密码登录
    def test_01_login_loginpag(self):
        homepage = self.loginpage.login_homepage(username, password)
        homepage.home_page_guidance()
        result1 = homepage.get_top_username()  # 获取首页登录店铺名称
        assume(result1 == username, "预期结果为：武汉市新洲区好药师周铺大药房，实际结果为：%s" % result1)
        # assert result == "武汉市新洲区好药师周铺大药房"
        homepage.log_out()  # 退出登录

    # 正确的账号，错误的密码登录
    def test_02_login_loginpag(self):
        self.loginpage.login_homepage(username, errer_password)
        result2 = self.loginpage.login_text()
        assume(result2 == "密码输入错误", "预期结果为：密码输入错误 ，实际结果为：%s" % result2)


if __name__ == "__main__":
    pytest.main(["-v", "test_login.py"])
