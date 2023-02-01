"""订单结算case"""
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

    # 登录进入搜索页面
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

    sleep(2)

    # 订单结算-账期支付
    def test_order_payment(self):
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
        # 点击提交订单按钮
        self.orderconfirmation.click_submit_order()
        # 进入结算成功页面等待
        sleep(3)
        # 提取支付成功文体
        result2, result3 = self.orderconfirmation.get_pay_way()
        assume("订单支付成功！" in result2, "预期结果为：订单支付成功！，实际结果为：{0}".format(result2))
        assume("账期支付" == result3, "预期结果为：账期支付 ，实际结果为：{0}".format(result3))
        # 返回到商品详情页面
        self.orderconfirmation.close_and_switch_window()
        sleep(2)
        # 返回到搜索列表页面
        self.detailsPage.close_and_switch_window()
        sleep(2)
