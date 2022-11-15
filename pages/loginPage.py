# coding=utf-8
"""
登录页面
"""
from common.basePage import Action
from common.log import Log
from common.fileReader import IniUtil
from common.commonMethod import CommonMethod
from time import sleep
from common.get_login_token import get_home_page_token


class LoginPage(Action):
    # 定位器，通过元素属性定位元素对象
    __username_loc = ('xpath', "//input[@name='username']")
    __password_loc = ('xpath', "//input[@name='password']")
    __submit_loc = ('xpath', '//*[@id="pane-first"]/form/div/button')
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

    click_login_text_loc = ('xpath', '//*[@id="tab-first"]/span')
    errer_text_loc = ('xpath', '/html/body/div[2]/p')

    def login_homepage(self, username, password):
        """账号密码登录"""
        self.open(self.__login_homepage_url)
        Log().info("打开登录首页: %s" % self.__login_homepage_url)
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
        # self.wait_title_change('九州通', 20)
        # 获取错误密码登录提示消息
        # self.get_text_loc(self.errer_text_loc, timeout=3)
        from pages.homePage import HomePage
        return HomePage(self.driver)

    def login_homepage_by_cookies(self):
        token = get_home_page_token()
        self.open(self.__login_homepage_url)
        Log().info("打开登录首页: %s" % self.__login_homepage_url)
        sleep(1)
        # 给网页注入cookies
        cookies1 = {u'name': u'yjj-token', u'value': token}
        cookies2 = {u'name': u'areaCode', u'value': u'42011100'}
        cookies3 = {u'name': u'companyId', u'value': u'781020001'}
        cookies4 = {u'name': u'companyName',
                    u'value': u'%E6%AD%A6%E6%B1%89%E5%B8%82%E6%96%B0%E6%B4%B2%E5%8C%BA%E5%A5%BD%E8%8D%AF%E5%B8%88%E5%91%A8%E9%93%BA%E5%A4%A7%E8%8D%AF%E6%88%BF'}
        cookies5 = {u'name': u'existBindCustomer', u'value': u'1'}
        cookies6 = {u'name': u'loginName',
                    u'value': u'%E6%AD%A6%E6%B1%89%E5%B8%82%E6%96%B0%E6%B4%B2%E5%8C%BA%E5%A5%BD%E8%8D%AF%E5%B8%88%E5%91%A8%E9%93%BA%E5%A4%A7%E8%8D%AF%E6%88%BF'}
        cookies7 = {u'name': u'nickName', u'value': u'%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7'}
        cookies8 = {u'name': u'userId', u'value': u'4'}
        cookies9 = {u'name': u'userMobile', u'value': u'17798242409'}
        cookies10 = {u'name': u'userName', u'value': u'%E5%91%A8%E9%93%BA%E8%B4%9F%E8%B4%A3%E4%BA%BA'}
        cookies11 = {u'name': u'userBasicId', u'value': u'3'}

        self.driver.add_cookie(cookies1)  # 这里添加cookie，有时cookie可能会有多条，需要添加多次
        self.driver.add_cookie(cookies2)
        self.driver.add_cookie(cookies3)
        self.driver.add_cookie(cookies4)
        self.driver.add_cookie(cookies5)
        self.driver.add_cookie(cookies6)
        self.driver.add_cookie(cookies7)
        self.driver.add_cookie(cookies8)
        self.driver.add_cookie(cookies9)
        self.driver.add_cookie(cookies10)
        self.driver.add_cookie(cookies11)
        sleep(3)
        self.driver.refresh()

    def login_text(self):
        # 获取错误密码登录提示消息
        hint_errer = self.get_text_loc(self.errer_text_loc, timeout=3)
        return hint_errer

    # ============================================忘记密码=============================================

    def click_forget_user_pwd(self):
        pass

    # ============================================用户注册=============================================

    def click_register_user(self):
        pass
