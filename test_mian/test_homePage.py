"""首页case"""
# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume
from pages.homePage import HomePage
from time import sleep
from common.basePage import Action
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"
search_keyword = "三棱"
product_name = "自动化专用勿动1"


class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        cls.driver = cls.com.get_driver()
        cls.loginpage = LoginPage(cls.driver)
        cls.home = HomePage(cls.driver)
        cls.basepage = Action(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # 登录
    def test_login_loginpag(self):
        # 账号密码登录
        # homepage = self.loginpage.login_homepage(username, password)
        # cookies注入登录
        self.loginpage.login_homepage_by_cookies()
        # 首页引导
        self.home.home_page_guidance()
        result1 = self.home.get_top_username()  # 获取首页登录店铺名称
        assume(result1 == username, "预期结果为：{1}，实际结果为：{0}".format(result1, username))

    # 顶部消息中心跳转校验
    def test_message_center(self):
        result2 = self.home.message_center()
        assume(result2 == '消息中心', "预期结果为：消息中心，实际结果为：%s" % result2)
        '''关闭消息中心'''
        self.home.close_message_center()

    # 顶部购物车跳转校验
    def test_shopping_trolley(self):
        result3 = self.home.shopping_trolley()
        assume(result3 == '购物车', "预期结果为：购物车，实际结果为：%s" % result3)
        '''从购物车退回到首页'''
        sleep(3)
        self.home.close_and_switch_window()

    sleep(2)

    # 首页商品分类跳转校验
    def test_goods_category(self):
        '''获取全部商品分类，第一个分类名称'''
        result4 = self.home.goods_category_text()
        '''获取全部商品分类，跳转第一个分类后，获取分类页面的分类名称'''
        sleep(3)
        result5 = self.home.goods_category()
        assume(result5 == result4, "预期结果为：{0}，实际结果为：{1}".format(result4, result5))
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    # 右侧购物车跳转校验
    def test_right_shopping_trolley(self):
        result6 = self.home.right_shopping_trolley()
        assume(result6 == '购物车', "预期结果为：购物车，实际结果为：%s" % result6)
        '''从购物车退回到首页'''
        sleep(3)
        self.home.close_and_switch_window()

    sleep(1)

    # 右侧反馈建议跳转校验
    def test_right_opinion(self):
        result7 = self.home.right_opinion()
        assume(result7 == '提建议', "预期结果为：提建议，实际结果为：%s" % result7)
        '''从反馈建议页面退回到首页'''
        sleep(3)
        self.home.close_and_switch_window()

    sleep(1)
    """
    # 平台客服弹框定位不到，暂时跳过，再找解决方法
    # 右侧平台客服跳转校验
    def test_right_call_center(self):
        result8 = self.home.right_call_center()
        assume(result8 == '小九在线客服', "预期结果为：小九在线客服，实际结果为：%s" % result8)

    """
    # 顶部领劵中心跳转校验
    def test_right__coupon_center(self):
        result9 = self.home.right__coupon_center()
        assume(result9 == '领券中心', "预期结果为：领劵中心，实际结果为：%s" % result9)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 右侧常购清单跳转校验
    def test_right__often_buy(self):
        result10 = self.home.right__often_buy()
        assume('常购清单' in result10, "预期结果为：常购清单，实际结果为：%s" % result10)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 右侧帮助中心跳转校验
    def test_right__help_center(self):
        result11 = self.home.right__help_center()
        assume(result11 == '帮助中心', "预期结果为：帮助中心，实际结果为：%s" % result11)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 右侧去还款跳转校验
    def test_right__repayment(self):
        result12 = self.home.right__repayment()
        assume(result12 == '账期还款', "预期结果为：账期还款，实际结果为：%s" % result12)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 右侧发票管理跳转校验
    def test_right__invoice_management(self):
        result13 = self.home.right__invoice_management()
        assume(result13 == '发票管理', "预期结果为：发票管理，实际结果为：%s" % result13)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 顶部我的订单跳转校验
    def test_top_my_order(self):
        result14 = self.home.top_my_order()
        assume(result14 == '我的订单', "预期结果为：我的订单，实际结果为：%s" % result14)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 顶部会员中心跳转校验
    def test_top_member_center(self):
        result15 = self.home.top_member_center()
        assume(result15 == '会员中心', "预期结果为：会员中心，实际结果为：%s" % result15)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 顶部会员中心跳转校验
    def test_top_customer_service(self):
        result16 = self.home.top_customer_service()
        assume(result16 == '帮助中心', "预期结果为：帮助中心，实际结果为：%s" % result16)
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()

    sleep(1)

    # 顶部搜索输入框搜索跳转校验
    def test_search_goods(self):
        result17 = self.home.search_goods(keywords=search_keyword)
        assume(search_keyword in result17, "预期结果为：{0}，实际结果为：{1}".format(search_keyword, result17))
        '''关闭当前页面，切换到最后面一个窗口'''
        self.basepage.close_and_switch_window()




