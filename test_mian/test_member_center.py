"""会员中心case"""
# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume
from pages.homePage import HomePage
from pages.prodSearchResultPage import SearchResult
from pages.prodDetailsPage import DetailsPage
from pages.memberCenterPage import MemberCenter
from pages.myCartPage import MyCart
from pages.myOrderPage import MyOrder
from pages.orderDetailsPage import OrderDetails
from pages.orderConfirmationPage import OrderConfirmation
from time import sleep
from common.basePage import Action
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"
search_keyword = "测试"
# 支付商品编码
product_code = "100118860"

# 跑的时候第一个商品不要设置成营销活动


class TestLogin():

    @classmethod
    def setup_class(cls):
        cls.com = CommonMethod()
        cls.driver = cls.com.get_driver()
        cls.loginpage = LoginPage(cls.driver)
        cls.home = HomePage(cls.driver)
        cls.searchpage = SearchResult(cls.driver)
        cls.mycar = MyCart(cls.driver)
        cls.detailsPage = DetailsPage(cls.driver)
        cls.membercenter = MemberCenter(cls.driver)
        cls.myorder = MyOrder(cls.driver)
        cls.orderdetails = OrderDetails(cls.driver)
        cls.orderconfirmation = OrderConfirmation(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # 登录-进入会员中心
    def test_login_loginpag(self):
        # 账号密码登录
        # homepage = self.loginpage.login_homepage(username, password)
        # 通过cookies注入登录
        self.loginpage.login_homepage_by_cookies()
        # 首页引导
        self.home.home_page_guidance()
        # 首页证照过期
        self.home.home_expired_certificate()
        result1 = self.home.get_top_username()  # 获取首页登录店铺名称
        assume(result1 == username, "预期结果为：{1}，实际结果为：{0}".format(result1, username))
        # 跳转到会员中心页面
        result2 = self.home.top_member_center()
        assume(result2 == "会员中心", "预期结果为：会员中心，实际结果为：{0}".format(result2))
        sleep(2)
        # 会员中心如果有引导就操作引导
        self.membercenter.member_center_guidance()
        sleep(3)

    sleep(1)

    # 点击领劵校验
    def test_click_coupon_button(self):
        result = self.membercenter.click_coupon_button()
        assume(result == "领券中心", "预期结果为：领券中心，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)

    sleep(1)

    # 点击查看明细校验
    def test_click_details_view(self):
        result = self.membercenter.click_details_view()
        assume(result == "可用余额", "预期结果为：可用余额，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)

    sleep(1)

    # 点击还款校验
    def test_click_repayment(self):
        result = self.membercenter.click_repayment()
        assume(result == "账期还款", "预期结果为：账期还款，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)

    sleep(1)

    # 订单中心-点击历史采购校验
    def test_click_lscg(self):
        result = self.membercenter.click_lscg()
        assume(result == "历史采购", "预期结果为：历史采购，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 订单中心-点击退货/售后跳转校验
    def test_click_sales_return(self):
        result = self.membercenter.click_sales_return()
        assume(result == "售后申请", "预期结果为：售后申请，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 订单中心-退货/售后-售后申请列表搜索校验
    def test_sales_return_application_list(self):
        result1, result2 = self.membercenter.sales_return_application_list()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))

    sleep(1)

    # 订单中心-退货/售后-申请记录列表搜索校验
    def test_application_record_list(self):
        result1, result2 = self.membercenter.application_record_list()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))

    sleep(1)

    # 订单中心-退货/售后-处理中列表搜索校验
    def test_being_processed_list(self):
        result1, result2 = self.membercenter.being_processed_list()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))

    sleep(1)

    # 订单中心-退货/售后-召回商品列表搜索校验
    def test_recall_of_goods_list(self):
        result1, result2 = self.membercenter.recall_of_goods_list()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))

    '''
    # 我的缺货篮定位不到，暂时注释
    # 关注中心-点击我的缺货篮校验
    def test_click_wdqhl(self):
        result = self.membercenter.click_wdqhl()
        assume(result == "我的缺货篮", "预期结果为：我的缺货篮，实际结果为：{0}".format(result))
        sleep(2)
    '''
    sleep(1)

    # 会员中心-我的优惠券跳转校验
    def test_my_discount_coupon(self):
        result = self.membercenter.my_discount_coupon()
        assume(result == "我的优惠券", "预期结果为：我的优惠券，实际结果为：{0}".format(result))
        sleep(2)
