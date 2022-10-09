# coding=utf-8
"""
登录页面
"""
from common.basePage import Action
from common.log import Log
from common.fileReader import IniUtil
from common.commonMethod import CommonMethod
from time import sleep


class LoginPage(Action):

    # 定位器，通过元素属性定位元素对象
    __username_loc = ('id', "jzt_username")
    __password_loc = ('id', "jzt_password")
    __submit_loc = ('xpath', "//*[@id='login_form_id']/div[4]/button")
    # 登录主页页面
    __login_homepage_url = CommonMethod().get_endpoint('loginpage')

    # 打开登录首页
    def open_login_page(self, base_url=__login_homepage_url, pagetitle='登录'):
        self.open(base_url, pagetitle)

    # 调用send_keys对象，输入用户名
    def input_username(self, username):
        self.send_keys_loc(self.__username_loc, username)

    # 调用send_keys对象，输入密码
    def input_password(self, password):
        self.send_keys_loc(self.__password_loc, password)

    def submit(self):
        # self.click_by_mouse(self.__submit_loc)
        # self.click_loc(self.__submit_loc)
        # 输入密码后，直接在输入密码框按enter键
        self.enter_key(self.__password_loc)

    click_login_text_loc = ('xpath', '//div[@class="userTips"]')

    def login_homepage(self, username, password):
        """登录"""
        self.open(self.__login_homepage_url, u'登录')
        Log().info(u"打开登录首页: %s" % self.__login_homepage_url)
        sleep(1)
        self.js_focus_element_loc(self.click_login_text_loc)
        sleep(1)
        # 点击账号密码登录
        self.click_loc(self.click_login_text_loc)
        Log().info(u"切换到用户名密码登录")
        sleep(1)
        self.input_username(username)
        Log().info(u"在登录首页用户名输入框输入：%s" % username)
        sleep(1)
        self.input_password(password)
        Log().info(u"在登录首页密码输入框输入：%s" % password)
        self.submit()
        Log().info(u"点击登录")
        # 等待页面title变化
        self.wait_title_change('九州通', 20)
        from pages.homePage import HomePage
        return HomePage(self.driver)

    #============================================忘记密码=============================================

    def click_forget_user_pwd(self):
        pass

    # ============================================用户注册=============================================

    def click_register_user(self):
        pass

