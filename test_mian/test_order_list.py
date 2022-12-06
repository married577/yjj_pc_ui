"""订单列表case"""
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

    # 订单列表-订单列表查询、订单详情校验
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
        # 提取订单号
        result2 = self.orderconfirmation.get_order_number()
        # 点击查看订单
        self.orderconfirmation.click_look_order()
        # 进入我的订单页面
        sleep(3)
        # 输入订单号搜索
        self.myorder.custom_order_search(result2)
        sleep(2)
        # 获取搜索结果第一个订单单号
        result3 = self.myorder.get_first_order_number()
        assume(result2 in result3, "预期结果为：{1}，实际结果为：{0}".format(result2, result3))
        # 点击订单图片，进入订单详情
        self.myorder.click_order_picture(result2)
        sleep(2)
        # 获取订单详情里面的订单号
        result4 = self.orderdetails.get_order_number1()
        # 断言订单号是否正确
        assume(result2 in result4, "预期结果为：{1}，实际结果为：{0}".format(result2, result4))
        '''
        # 客服页面句柄定位不到暂时注释
        # 校验联系客服跳转
        text = self.orderdetails.click_contact_merchant()
        assume(text == "小九在线客服", "预期结果为：小九在线客服，实际结果为：{0}".format(text))
        self.detailsPage.close_and_switch_window()
        '''
        # 关闭当前页面，返回到订单列表页
        self.detailsPage.close_and_switch_window()
        sleep(3)
        # 点击订单编号，进入订单详情
        self.myorder.click_order_number(result2)
        sleep(2)
        # 获取订单详情里面的订单号
        result5 = self.orderdetails.get_order_number1()
        # 断言订单号是否正确
        assume(result2 in result5, "预期结果为：{1}，实际结果为：{0}".format(result2, result5))
        # 关闭当前页面，返回到订单列表页
        self.detailsPage.close_and_switch_window()
        sleep(3)
        # 点击店铺名称，跳转到店铺首页校验
        result6 = self.myorder.click_store_name()
        print(6)
        # 断言店铺名称是否正确
        assume(result6 == "湖北九州通", "预期结果为：湖北九州通，实际结果为：{0}".format(result6))
        # 关闭当前页面，返回到订单列表页
        self.detailsPage.close_and_switch_window()
        sleep(3)
        '''
        # 跳转到客服页面获取不到句柄，切不到最新页面，暂时注释
        # 点击店和我联系，跳转到客服首页
        result7 = self.myorder.click_relation_and_me(result2)
        # 断言客服名称是否正确
        assume(result7 == "小九在线客服", "预期结果为：小九在线客服，实际结果为：{0}".format(result7))
        # 关闭当前页面，返回到订单列表页
        self.detailsPage.close_and_switch_window()
        sleep(3)
        '''
        # 取消订单校验
        self.myorder.cancellation_of_order(result2)
        sleep(5)
        # 输入订单号搜索，刷新订单状态
        self.myorder.custom_order_search(result2)
        sleep(2)
        # 获取取消的订单，订单状态
        result8 = self.myorder.order_state(result2)
        assume("已取消" in result8, "预期结果为：已取消，实际结果为：{0}".format(result8))
        sleep(2)
        # 删除订单校验
        result9 = self.myorder.delete_order(result2)
        assume(result9 == "操作成功", "预期结果为：操作成功，实际结果为：{0}".format(result9))
