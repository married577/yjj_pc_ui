# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume
from pages.homePage import HomePage
from pages.prodSearchResultPage import SearchResult
from pages.prodDetailsPage import DetailsPage
from pages.memberCenterPage import MemberCenter
from pages.myCartPage import MyCart
from time import sleep
from common.basePage import Action
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"
search_keyword = "测试"

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
        cls.basepage = Action(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # 登录进入第一个商品详情页面
    def test_login_loginpag(self):
        # 账号密码登录
        # homepage = self.loginpage.login_homepage(username, password)
        # 通过cookies注入登录
        self.loginpage.login_homepage_by_cookies()
        self.home.home_page_guidance()
        result1 = self.home.get_top_username()  # 获取首页登录店铺名称
        assume(result1 == username, "预期结果为：{1}，实际结果为：{0}".format(result1, username))
        # 跳转到搜索页面
        self.home.search_jump()
        # 进入商品详情
        self.detailsPage.go_to_proddetail()
        sleep(2)

    # 通过详情url直接打开页面跳转正确校验
    def test_direct_jump_url(self):
        # 获取详情页商品名称
        result1 = self.detailsPage.get_prodname()
        # 获取窗口页面
        url = self.driver.current_url
        # 关闭当前页面，切换到最后面一个窗口
        self.basepage.close_and_switch_window()
        # 通过url直接打开详情
        self.driver.get(url)
        # 获取详情页商品名称
        result2 = self.detailsPage.get_prodname()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        sleep(2)

    sleep(1)

    # 点击商品关注和取消关注显示正确
    def test_gz(self):
        # 获取关注前和关注后的状态对比
        result1, result2, result3 = self.detailsPage.gz()
        if result1 == "关注":
            assume(result2 == "已关注", "预期结果为：已关注，实际结果为：{0}".format(result2))
            assume(result3 == "关注", "预期结果为：关注，实际结果为：{0}".format(result3))
        if result1 == "已关注":
            assume(result2 == "关注", "预期结果为：关注，实际结果为：{0}".format(result2))
            assume(result3 == "已关注", "预期结果为：已关注，实际结果为：{0}".format(result3))
        sleep(2)

    sleep(1)

    # 关注商品-会员中心-我的关注页面显示校验
    def test_click_gz(self):
        # 商品详情，获取商品名称
        result1 = self.detailsPage.get_prodname()
        # 点击关注按钮，关注商品
        self.detailsPage.click_gz()
        # 进入会员中心
        self.detailsPage.get_member_center()
        # 会员中心引导
        self.membercenter.member_center_guidance()
        sleep(1)
        # 进入我的关注商品列表
        self.membercenter.click_wdgz()
        sleep(2)
        # 获取我的关注列表页面，所有商品名称
        result2 = self.membercenter.get_wdgz_prodname()
        assume(result1 in result2, "商品名称为：{0}，关注列表的商品名称为：{1}".format(result1, result2))
        # 关闭当前页面，切换到最后面一个窗口
        self.basepage.close_and_switch_window()
        sleep(2)

    sleep(1)

    # 点击店铺关注和取消关注显示正确
    def test_store_gz(self):
        # 获取关注前和关注后的状态对比
        result1, result2, result3 = self.detailsPage.store_gz()
        if result1 == "关注":
            assume(result2 == "已关注", "预期结果为：已关注，实际结果为：{0}".format(result2))
            assume(result3 == "关注", "预期结果为：关注，实际结果为：{0}".format(result3))
        if result1 == "已关注":
            assume(result2 == "关注", "预期结果为：关注，实际结果为：{0}".format(result2))
            assume(result3 == "已关注", "预期结果为：已关注，实际结果为：{0}".format(result3))
        sleep(2)

    sleep(1)

    # 关注店铺-会员中心-我的关注页面显示校验
    def test_click_store_gz(self):
        # 商品详情，获取店铺名称
        result1 = self.detailsPage.get_store_name()
        # 点击关注按钮，关注店铺
        self.detailsPage.click_store_gz()
        # 进入会员中心
        self.detailsPage.get_member_center()
        # 会员中心引导
        self.membercenter.member_center_guidance()
        sleep(1)
        # 进入我的关注店列表
        self.membercenter.click_wdgz()
        sleep(2)
        # 获取我的关注列表页面，所有店铺名称
        result2 = self.membercenter.get_wdgz_storename()
        if result1 == "湖北九州通":
            assume("九州通医药集团股份有限公司" in result2, "店铺名称为：{0}，关注列表的店铺名称为：{1}".format(result1, result2))
        else:
            assume(result1 in result2, "店铺名称为：{0}，关注列表的店铺名称为：{1}".format(result1, result2))
        # 关闭当前页面，切换到最后面一个窗口
        self.basepage.close_and_switch_window()
        sleep(2)

    sleep(1)

    # 点击店铺跳转正确校验
    def test_store_homepage(self):
        # 获取商品详情店铺名称
        result1 = self.detailsPage.get_store_name()
        # 获取跳转到店铺主页的店铺名称
        result2 = self.detailsPage.store_homepage()
        # 关闭当前页面，切换到最后面一个窗口
        self.basepage.close_and_switch_window()
        sleep(2)
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))