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
from common.fileReader import IniUtil

if IniUtil().get_value_of_option('test_env', 'env') == 'pre':
    username = "武汉市新洲区好药师周铺大药房"
    password = "123456"
    search_keyword = "测试"
    # 支付商品编码
    product_code = "100118860"
    product_name = "三棱"

if IniUtil().get_value_of_option('test_env', 'env') == 'prod':
    username = "武汉市好药师周铺大药房有限公司"
    password = "123456"
    search_keyword = "测试"
    # 支付商品编码
    product_code = "100118860"
    product_name = "三棱"
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
    """
    # 会员中心领劵按钮功能有变动，目前没有领劵按钮
    # 点击领劵校验
    def test_click_coupon_button(self):
        result = self.membercenter.click_coupon_button()
        assume(result == "领券中心", "预期结果为：领券中心，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)
    
    sleep(1)

    # 点击钱包充值校验
    def test_click_wallet_recharge(self):
        result = self.membercenter.click_wallet_recharge()
        assume(result == "钱包充值", "预期结果为：钱包充值，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)

    sleep(1)
    """

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

    """
    # 我的缺货篮定位不到，暂时注释
    # 关注中心-点击我的缺货篮校验
    def test_click_wdqhl(self):
        result = self.membercenter.click_wdqhl()
        assume(result == "我的缺货篮", "预期结果为：我的缺货篮，实际结果为：{0}".format(result))
        sleep(2)
    """
    sleep(1)

    # 会员中心-我的优惠券跳转校验
    def test_my_discount_coupon(self):
        result = self.membercenter.my_discount_coupon()
        assume(result == "我的优惠券", "预期结果为：我的优惠券，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-我的优惠券-领劵中心跳转校验
    def test_go_coupon_center(self):
        result1, result2 = self.membercenter.go_coupon_center()
        assume(result1 == "领券中心", "预期结果为：领券中心，实际结果为：{0}".format(result1))
        assume(result2 == "我的优惠券", "预期结果为：我的优惠券，实际结果为：{0}".format(result2))
        sleep(3)

    sleep(1)

    # 会员中心-企业信息页面跳转校验
    def test_enterprise_information(self):
        result = self.membercenter.enterprise_information()
        assume(result == "企业信息", "预期结果为：企业信息，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-首营记录页面跳转校验
    def test_shouying_record(self):
        result = self.membercenter.shouying_record()
        assume(result == "首营记录", "预期结果为：首营记录，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-首营记录页面-列表查询店铺名称校验
    def test_shouying_recored_select_storename(self):
        result1, result2 = self.membercenter.shouying_recored_select_storename()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        sleep(2)

    sleep(1)

    # 会员中心-首页记录页面-列表查询店铺类型校验
    def test_shouying_recored_select_storetype(self):
        result1, result2 = self.membercenter.shouying_recored_select_storetype()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        sleep(2)

    sleep(1)

    # 会员中心-企业管理跳转校验
    def test_business_management(self):
        result = self.membercenter.business_management()
        assume(result == "企业管理", "预期结果为：企业管理，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-资质管理跳转校验
    def test_qualification_management(self):
        result = self.membercenter.qualification_management()
        assume(result == "资质管理", "预期结果为：资质管理，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-员工账号管理跳转校验
    def test_employee_account_management(self):
        result = self.membercenter.employee_account_management()
        assume(result == "员工账号管理", "预期结果为：员工账号管理，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-发票管理跳转校验
    def test_invoice_management(self):
        result = self.membercenter.invoice_management()
        assume(result == "发票查询", "预期结果为：发票查询，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-支付查询跳转校验
    def test_pay_query(self):
        result = self.membercenter.pay_query()
        assume(result == "支付查询", "预期结果为：支付查询，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-支付查询-支付方式查询校验
    def test_pay_query_payment(self):
        result1, result2 = self.membercenter.pay_query_payment()
        assume(result1 == result2, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        sleep(2)

    sleep(1)

    # 个人中心-我的钱包页面跳转校验
    def test_my_wallet(self):
        result = self.membercenter.my_wallet()
        assume(result == "可用余额", "预期结果为：可用余额，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-我的九州币页面跳转校验
    def test_my_jzb(self):
        result = self.membercenter.my_jzb()
        assume(result == "我的九州币", "预期结果为：我的九州币，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-账户安全页面跳转校验
    def test_account_security(self):
        result = self.membercenter.account_security()
        assume(result == "账户安全", "预期结果为：账户安全，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-抽奖页面跳转校验
    def test_my_lottery(self):
        result = self.membercenter.my_lottery()
        assume(result == "我的抽奖", "预期结果为：我的抽奖，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 个人中心-投诉建议跳转校验
    def test_complaint_and_advice(self):
        result = self.membercenter.complaint_and_advice()
        assume(result == "提建议", "预期结果为：提建议，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 客户服务-帮助中心跳转校验
    def test_help_center(self):
        result = self.membercenter.help_center()
        assume(result == "帮助中心", "预期结果为：帮助中心，实际结果为：{0}".format(result))
        self.driver.back()
        sleep(2)

    sleep(1)

    # 客户服务-客商往来账跳转校验
    def test_merchant_current_account(self):
        result = self.membercenter.merchant_current_account()
        assume(result == "客商往来账", "预期结果为：客商往来账，实际结果为：{0}".format(result))
        sleep(2)

    sleep(1)

    # 会员中心-搜索校验
    def test_member_center_search(self):
        # 会员中心搜索
        self.membercenter.member_center_search(prod_name=product_name)
        self.searchpage.switch_window()
        # 获取搜索页面搜索结果商品名称
        result = self.searchpage.get_goods_name()
        assume(product_name in result, "预期结果为：{1}，实际结果为：{0}".format(result, product_name))
        # 返回到会员中心页面
        self.searchpage.close_and_switch_window()
        sleep(3)

    # 会员中心-切换企业校验
    @pytest.mark.prod
    def test_switch_to_enterprise(self):
        # 选择切换企业进行切换
        result1 = self.membercenter.switch_to_enterprise()
        # 新企业首页-关闭引导和证照补全和过期
        self.home.home_page_guidance()
        self.home.home_expired_certificate()
        self.home.home_complete_the_certificate()
        sleep(3)
        # 获取切换企业名称
        self.home.switch_window()
        result2 = self.home.get_top_user_name()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        # 还原-切换到原来的企业
        sleep(3)
        self.membercenter.back_enterprise()
        # 原企业首页-关闭引导和证照补全和过期
        self.home.home_page_guidance()
        self.home.home_expired_certificate()
        self.home.home_complete_the_certificate()
        # 跳转到会员中心页面
        result3 = self.home.top_member_center()
        assume(result3 == "会员中心", "预期结果为：会员中心，实际结果为：{0}".format(result3))
        sleep(2)
        # 会员中心如果有引导就操作引导
        self.membercenter.member_center_guidance()
        sleep(3)
