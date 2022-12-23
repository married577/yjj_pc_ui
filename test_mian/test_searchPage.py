"""搜索页面case"""
# coding:utf-8
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from common.AssertWithLog import assume
from pages.homePage import HomePage
from pages.prodSearchResultPage import SearchResult
from pages.myCartPage import MyCart
from time import sleep
from common.basePage import Action
import pytest

username = "武汉市新洲区好药师周铺大药房"
password = "123456"
search_keyword = "三棱"

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
        cls.basepage = Action(cls.driver)

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
        # 证照过期提示
        self.home.home_expired_certificate()
        result1 = self.home.get_top_username()  # 获取首页登录店铺名称
        assume(result1 == username, "预期结果为：{1}，实际结果为：{0}".format(result1, username))
        # 跳转到搜索页面
        self.home.search_jump()
        sleep(2)

    # 所有商品分类跳转校验
    # 清除筛选项校验
    def test_all_goods_classify(self):
        # 选择第一个分类，取分类名称
        result1 = self.home.goods_category_text()
        # 选择分类跳转，获取搜索结果分类名称
        result2 = self.home.goods_category()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        # 清除筛选项
        self.searchpage.clear_search()
        # 清除筛选项校验
        element = '//div[@class="ss-breadcrumbs-selected"]/div/span[1]'
        result3 = self.basepage.isElementExist(element)
        assume(result3 == False, "预期结果为：False，实际结果为：{0}".format(result3))
        # 点击搜索刷新一下页面
        self.searchpage.search_goods()

    sleep(1)

    # 输入框点击搜索跳转和搜索正确校验
    def test_input_box_search(self):
        # 获取商品列表商品名称，作为搜索关键字
        text = self.searchpage.get_goods_name()
        # 输入框输入关键字，点击搜索
        self.searchpage.search_goods(keywords=text)
        # 获取搜索结果，提取商品名称
        result = self.searchpage.get_goods_name()
        assume(text in result, "预期结果为：{1}，实际结果为：{0}".format(result, text))
        # 清除输入框搜索内容,刷新搜索页面(清除不掉输入框内容不知道啥原因，只能换成下面的方法，回到首页再进入搜索页面)
        # self.searchpage.search_goods()
        """关闭当前页面，切换到最后面一个窗口"""
        self.basepage.close_and_switch_window()
        sleep(1)
        # 跳转到搜索页面
        self.home.search_jump()
        sleep(3)

    sleep(1)

    # 搜索页面分类搜索校验
    def test_first_class_search(self):
        # 搜索一级分类第一个分类
        result1, result2 = self.searchpage.first_class_search()
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        # 清除筛选项
        self.searchpage.clear_search()

    sleep(1)

    # 搜索店铺校验
    def test_store_search(self):
        # 搜索第一个店铺校验
        result1, result2 = self.searchpage.store_search()
        # 断言搜索店铺名称与搜索结果第一个店铺名称对比
        assume(result1 == result2, "预期结果为：{1}，实际结果为：{0}".format(result1, result2))
        # 清除筛选项
        self.searchpage.clear_search()
        # 睡2秒等清除加载完成
        sleep(2)

    sleep(1)

    # 搜索厂家校验
    def test_manufacturers_search(self):
        # 搜索第一个厂家校验
        result1, result2 = self.searchpage.manufacturers_search()
        # 断言搜索厂家名称与搜索结果对比
        assume(result2 in result1, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        """关闭当前页面，切换到最后面一个窗口"""
        self.basepage.close_and_switch_window()
        # 清除筛选项
        self.searchpage.clear_search()
        # 睡2秒等清除加载完成
        sleep(2)

    sleep(1)

    # 搜索规格校验
    def test_size_search(self):
        # 搜索第一个规格校验
        result1, result2 = self.searchpage.size_search()
        # 断言搜索规格名称与搜索结果对比
        assume(result2 in result1, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        """关闭当前页面，切换到最后面一个窗口"""
        self.basepage.close_and_switch_window()
        # 清除筛选项
        self.searchpage.clear_search()
        # 更多选项按钮还原
        self.searchpage.more_options()
        # 睡2秒等清除加载完成
        sleep(2)

    sleep(1)

    # 搜索剂型校验
    def test_dosage_form_search(self):
        # 搜索第一个剂型校验
        result1, result2 = self.searchpage.dosage_form_search()
        # 断言搜索剂型名称与搜索结果对比
        assume(result2 == result1, "预期结果为：{0}，实际结果为：{1}".format(result1, result2))
        """关闭当前页面，切换到最后面一个窗口"""
        self.basepage.close_and_switch_window()
        # 清除筛选项
        self.searchpage.clear_search()
        # 更多选项按钮还原
        self.searchpage.more_options()
        # 睡2秒等清除加载完成
        sleep(2)

    sleep(1)

    # 搜索页面点击药九九图标返回到首页校验
    def test_search_page_return(self):
        # 获取首页右侧商户名称
        result = self.searchpage.search_page_return()
        assume(result == username, "预期结果为：{0}，实际结果为：{1}".format(username, result))
        # 返回到搜索页面
        self.driver.back()
        # 等待加载
        sleep(1)

    sleep(1)

    # 列表商品正确加购校验
    def test_first_goods_purchased(self):
        # 获取商品详情页面，商品名称
        goods_name1 = self.searchpage.get_detail_goods_name()
        sleep(1)
        # 获取加购提示
        result1 = self.searchpage.first_goods_purchased()
        assume(result1 == "加购成功！", "预期结果为：加购成功！，实际结果为：{0}".format(result1))
        # 从搜索页面跳转到购物车
        self.searchpage.shopping_cart_skip()
        sleep(1)
        # 获取购物车商品名称
        goods_name2 = self.mycar.all_goods_names()
        assume(goods_name1 in goods_name2, "预期结果为：{0}，实际结果为：{1}".format(goods_name1, goods_name2))
        # 返回到搜索页面
        self.mycar.close_and_switch_window()
        # 等待加载
        sleep(2)

    sleep(1)

    # 点击商品名称，商品图片和点击跳转正确验证
    def test_goods_jump(self):
        # 获取商品列表第一个商品，在商品列表中的商品名称
        result = self.searchpage.get_goods_name()
        # 点击商品名称进入商品详情，获取商品名称
        result1 = self.searchpage.get_detail_goods_name()
        # 点击商品图片进入商品详情，获取商品名称
        result2 = self.searchpage.get_detail_goods_picture()
        # 断言商品详情里面的商品名称跟商品列表的商品名称一致
        assume(result1 in result, "预期结果为：{0}，实际结果为：{1}".format(result, result1))
        assume(result2 in result, "预期结果为：{0}，实际结果为：{1}".format(result, result2))
        sleep(2)

    # 综合条件-价格排序校验
    def test_order_of_price(self):
        # 点击价格排序按钮，调整为价格倒序
        self.searchpage.order_of_price()
        # 获取商品列表前两个商品的商品价格
        result1, result2 = self.searchpage.get_the_price()
        assume(result1 >= result2, "预期结果为：{0}>={1}，实际结果为：{0}>={1}".format(result1, result2))
        # 刷新页面，清空综合条件搜索
        self.searchpage.refresh()
        sleep(2)

    # 综合条件-价格范围校验
    def test_range_of_price(self):
        # 点击价格排序按钮，调整为价格倒序
        self.searchpage.price_rank(down="10", up="20")
        # 获取商品列表前两个商品的商品价格
        result1, result2 = self.searchpage.get_the_price()
        result3 = float(result1)
        result4 = float(result2)
        assume(20.00 >= result3 >= 10.00, "预期结果为：20 >= {0}>= 10，实际结果为：20 >= {0} >= 10".format(result3))
        assume(20.00 >= result4 >= 10.00, "预期结果为：20 >= {0}>= 10，实际结果为：20 >= {0} >= 10".format(result4))
        # 点击搜索按钮，刷新页面清空综合条件
        self.searchpage.refresh()
        sleep(2)

    sleep(1)
    
    # 综合条件-甲类OTC搜索结果校验
    def test_composition_condition_jiaotc(self):
        # 获取甲类OTC筛选类型文本和商品详情里面处方分类类型文本
        result1, result2 = self.searchpage.composition_condition_jiaotc()
        assume(result2 in result1, "预期结果为：{1}属于{0}，实际结果为：{1}属于{0}".format(result1, result2))

    sleep(1)

    # 综合条件-乙类OTC搜索结果校验
    def test_composition_condition_yiotc(self):
        # 获取乙类OTC筛选类型文本和商品详情里面处方分类类型文本
        result1, result2 = self.searchpage.composition_condition_yiotc()
        assume(result2 in result1, "预期结果为：{1}属于{0}，实际结果为：{1}属于{0}".format(result1, result2))

    sleep(1)

    # 综合条件-处方药搜索结果校验
    def test_composition_condition_ethicals(self):
        # 获取处方药筛选类型文本和商品详情里面处方分类类型文本
        result1, result2 = self.searchpage.composition_condition_ethicals()
        assume(result2 in result1, "预期结果为：{1}属于{0}，实际结果为：{1}属于{0}".format(result1, result2))

    sleep(1)

    # 综合条件-器械搜索结果校验
    def test_composition_condition_instrument(self):
        # 获取器械筛选类型文本和商品详情里面器械类型文本
        result1, result2 = self.searchpage.composition_condition_instrument()
        assume(result1 in result2, "预期结果为：{1}属于{0}，实际结果为：{1}属于{0}".format(result2, result1))
