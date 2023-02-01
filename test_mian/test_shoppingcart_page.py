"""购物车页面case"""
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
# 售罄商品编码
product_code = "100154268"

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

    # 售罄商品加购校验
    def test_sell_out_prod(self):
        # 搜索售罄商品
        self.searchpage.search_goods(keywords=product_code)
        sleep(3)
        # 售罄商品加购,获取加购提示消息
        result = self.searchpage.first_goods_purchased()
        assume(result == "到货通知登记成功，商品到货后第一时间通知您。", "预期结果为：到货通知登记成功，商品到货后第一时间通知您。，实际结果为：{0}".format(result))
        # 刷新搜索页面
        self.searchpage.refresh()
        sleep(2)

    sleep(1)
    
    # 订单详情再次加购校验
    def test_order_detail_add(self):
        # 从搜索页面进入我的订单页面
        self.myorder.go_to_my_order_page()
        sleep(1)
        # 进入第一个订单，订单详情
        self.myorder.go_to_frist_order_detail()
        sleep(1)
        # 获取订单详情，第一个商品，商品名称
        result = self.orderdetails.get_prod_name()
        # 商品详情，第一个商品再次加购,并提取加购成消息
        result1 = self.orderdetails.click_buy_again()
        assume(result1 == "加入成功", "预期结果为：加入成功，实际结果为：{0}".format(result1))
        # 关闭当前页面，进入我的订单页面
        self.orderdetails.close_and_switch_window()
        sleep(2)
        # 我的订单页面，点击购物车图标
        self.myorder.click_my_car()
        sleep(1)
        # 获取购物车列表，所有商品名称
        result2 = self.mycar.all_goods_names()
        # 关闭当前页面，进入搜索页面
        self.mycar.close_and_switch_window()
        sleep(2)
        assume(result in result2, "预期结果为：{0}，实际结果为：{1}".format(result, result2))

    sleep(1)

    # 点击药九九图返回首页校验
    def test_yjj_back_homepage(self):
        # 进入我的购物车页面
        self.searchpage.shopping_cart_skip()
        sleep(2)
        # 切换到我的购物车页面
        self.mycar.switch_window()
        # 点击药九九图标跳转到主页
        self.mycar.yjj_icon()
        sleep(2)
        # 获取右侧用户名
        result = self.home.get_right_name()
        # 关闭当前窗口，回到搜索页面
        self.home.close_and_switch_window()
        sleep(2)
        assume(result == username, "预期结果为：{1}，实际结果为：{0}".format(result, username))
    
    sleep(1)

    # 购物车删除校验
    def test_remove_item(self):
        # 进入第一个商品商品详情页
        self.detailsPage.go_to_proddetail()
        sleep(3)
        # 获取商品名称
        result1 = self.detailsPage.get_prodname()
        # 点击加入购物车
        self.detailsPage.click_add_to_cart()
        # 跳转到购物车页面
        self.detailsPage.go_to_my_cart()
        # 获取购物车列表商品名称
        result2 = self.mycar.all_goods_names()
        assume(result1 in result2, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        sleep(3)
        # 删除购物车指定商品
        result3 = self.mycar.remove_item(prod_name=result1)
        assume(result3 == "操作成功", "预期结果为：操作成功，实际结果为：{0}".format(result3))
        sleep(3)
        # 再次获取购物车列表商品名称
        result4 = self.mycar.all_goods_names()
        assume(result4 not in result2, "预期结果为：{0}，实际结果为：{1}".format(result4, result2))
        # 关闭当前页返回到商品详情页面
        self.mycar.close_and_switch_window()
        sleep(2)
        # 关闭当前页返回到商品搜索页面
        self.mycar.close_and_switch_window()
        sleep(3)

    sleep(1)
    
    # 购物车点击添加关注以及在我的关注商品页面显示正确和我的关注页面取消校验
    def test_assign_goods_attention(self):
        # 进入第一个商品商品详情页
        self.detailsPage.go_to_proddetail()
        # 获取商品名称
        result1 = self.detailsPage.get_prodname()
        # 点击加入购物车
        self.detailsPage.click_add_to_cart()
        # 跳转到购物车页面
        self.detailsPage.go_to_my_cart()
        # 添加关注商品,提取关注成功提示消息
        result2 = self.mycar.assign_goods_attention(prod_name=result1)
        assume(result2 == "操作成功", "预期结果为：操作成功，实际结果为：{0}".format(result2))
        # 进入会员中心
        self.mycar.go_to_membercenter()
        sleep(1)
        # 会员中心引导
        self.membercenter.member_center_guidance()
        # 点击我的关注
        self.membercenter.click_wdgz()
        sleep(3)
        # 我的关注列表商品页面，获取所有商品名称
        result3 = self.membercenter.get_wdgz_prodname()
        assume(result1 in result3, "预期结果为：{0}，实际结果为：{1}".format(result1, result3))
        # 取消关注商品
        result4 = self.membercenter.deselect_gz_prodname(prod_name=result1)
        assume(result4 == "取消关注成功", "预期结果为：取消关注成功，实际结果为：{0}".format(result4))
        sleep(1)
        # 再次获取关注列表,所有商品名称
        result5 = self.membercenter.get_wdgz_prodname()
        assume(result1 not in result5, "预期结果为：{0}，实际结果为：{1}".format(result1, result5))
        # 关闭当前页返回到购物车页面
        self.membercenter.close_and_switch_window()
        sleep(2)
        # 关闭当前页返回到商品详情页面
        self.mycar.close_and_switch_window()
        sleep(2)
        # 关闭当前页返回到商品列表页面
        self.detailsPage.close_and_switch_window()
        sleep(2)
    
    sleep(1)

    # 购物车,商品数量输入框输入加购商品,以及跳转到结算页面流程校验
    def test_modification_amount(self):
        # 加购数量设置
        __quantity = 100
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
        # 校验页面跳转是否正确
        result2 = self.orderconfirmation.extract_title()
        assume(result2 == "订单结算", "预期结果为：订单结算，实际结果为：{0}".format(result2))
        # 获取结算页面所有商品名称
        result4 = self.orderconfirmation.get_all_prod_name()
        assume(result1 in result4, "预期结果为：{0}，实际结果为：{1}".format(result1, result4))
        # 提取商品购买数量
        result3 = self.orderconfirmation.get_prod_amount(prod_name=result1)
        result5 = str(__quantity)
        assume(result5 in result3, "预期结果为：{1}，实际结果为：{0}".format(result3, result5))
        # 关闭当前页返回到购物车
        self.orderconfirmation.close_and_switch_window()
        sleep(2)
        # 关闭当前页返回到商品列表页面
        self.detailsPage.close_and_switch_window()
        sleep(2)
