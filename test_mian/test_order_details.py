"""订单详情case"""
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


@pytest.mark.prod
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

    # 登录-加购-下单-生成订单进入订单列表
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
        # 跳转到搜索页面
        self.home.search_jump()
        sleep(3)
        # 搜索页面通过商品编码搜索
        self.searchpage.search_goods(keywords=product_code)
        sleep(3)
        # 加购数量设置
        __quantity = 1
        # 进入第一个商品商品详情页
        self.detailsPage.go_to_proddetail()
        # 获取商品名称
        result1 = self.detailsPage.get_prodname()
        # 点击加入购物车
        self.detailsPage.click_add_to_cart()
        # 跳转到购物车页面
        self.detailsPage.go_to_my_cart()
        # 清空全选
        self.mycar.check_all_prod()
        # 输入框输入购买数量
        self.mycar.modify_prod_num(num=__quantity, prod_no=result1)
        # 选中指定的商品
        self.mycar.check_appoint_prod(prod_name=result1)
        # 点击去结算
        self.mycar.submit_order_button()
        # 判断是否有包邮提醒
        self.mycar.submit_exemption_remind()
        # 进入订单结算页面
        sleep(3)
        # 选择账期支付
        self.orderconfirmation.select_payment_days()
        sleep(2)
        # 点击提交订单按钮
        self.orderconfirmation.click_submit_order()
        # 进入结算成功页面等待
        sleep(3)
        # 提取订单号
        result2 = self.orderconfirmation.get_order_number()
        # 点击查看订单
        self.orderconfirmation.click_look_order()
        # 进入我的订单页面
        sleep(3)
        # 点击订单编号，进入订单详情
        self.myorder.click_order_number(result2)
        sleep(3)

    sleep(2)

    # 订单详情-点击再次购买校验
    def test_buy_again(self):
        # 提取商品名称
        result1 = self.orderdetails.get_prod_name()
        # 点击再次购买
        self.orderdetails.click_again_bug()
        # 进入购物车页面
        sleep(3)
        # 获取购物车所有商品名称
        result2 = self.mycar.all_goods_names()
        assume(result1 in result2, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        # 返回到商品详情页面
        self.driver.back()

    sleep(1)

    # 订单详情-点击取消订单校验
    def test_cancellation_order(self):
        result = self.orderdetails.click_cancellation_order()
        assume(result == "订单取消成功", "预期结果为：取消成功，实际结果为：{0}".format(result))
