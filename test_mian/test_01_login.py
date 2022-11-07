# coding=utf-8
import pytest
from common.fileReader import IniUtil
from pages.homePage import HomePage
from pages.loginPage import LoginPage
from time import sleep
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume


class TestLogin():
    """测试从登录页面成功校验用户信息是否正确"""

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        # 获取浏览器驱动
        cls.driver = cls.com.get_driver()
        cls.driver.delete_all_cookies()
        cls.loginpage = LoginPage(cls.driver)
        cls.homepage = HomePage(cls.driver)
        # 用户名密码
        cls.username, cls.password = cls.com.get_login_user('main')

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_01_login_loginpage(self):
        """从登录界面登录"""
        self.loginpage.login_homepage(self.username, self.password)
        sleep(2)
        # 比较顶部和右边用户信息是否一致
        text = self.homepage.compare_username()
        assume(text, '判断顶部和右边用户信息是否一致')
        sleep(2)
        # 右侧退出
        self.homepage.log_out()


class TestForgotPwd():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        # 获取浏览器驱动
        cls.driver = cls.com.get_driver()
        cls.driver.delete_all_cookies()
        cls.loginpage = LoginPage(cls.driver)
        cls.homepage = HomePage(cls.driver)
        # 用户名密码
        cls.username, cls.password = cls.com.get_login_user('main')

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_01_forgot_pwd_jump(self):
        pass


class TestUserRegister():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        # 获取浏览器驱动
        cls.driver = cls.com.get_driver()
        cls.driver.delete_all_cookies()
        cls.loginpage = LoginPage(cls.driver)
        cls.homepage = HomePage(cls.driver)
        # 用户名密码
        cls.username, cls.password = cls.com.get_login_user('main')

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_01_user_register(self):
        pass










