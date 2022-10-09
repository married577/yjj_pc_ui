"""顶部公共菜单：客户名称，退出，我的订单"""
from common.basePage import Action
from common.log import Log
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class BaseMenus(Action):

    # 客户名称
    __username_loc = ('xpath', '//a[@class="u_user_name"]')
    # 退出
    __log_out_loc = ('xpath', '//a[@class="u_quit"]')
    # 我的订单
    __my_order_loc = ('xpath', '//ul[@class="m_menu_group"]//a[text()="我的订单"]')
    # 返回首页
    __back_to_homepage_loc = ('xpath', '//*[@id="goBackHome"]')
    # 我的购物车
    __my_cart_button_loc = ('xpath', "//div/div[@class='m_cart']/a")

    def log_out(self):
        """
        点击顶部的退出链接
        :return: 登录首页的page对象
        """
        self.click_loc(self.__log_out_loc)
        self.wait_title_change('登录')
        Log().info("退出登录，跳转到登录页面")
        from pages.loginPage import LoginPage
        return LoginPage(self.driver)

    def go_to_my_order_page(self):
        """
        点击顶部的我的订单链接
        :return: 返回我的订单页的page对象
        """
        self.click_loc(self.__my_order_loc)
        # 当前窗口数量
        windows_handles = self.get_windows_num()
        if windows_handles > 1:
            self.close_and_switch_window()
        self.wait_title_change('我的订单')
        Log().info("点击顶部的我的订单，跳转到我的订单页面")
        from pages.myOrderPage import MyOrder
        return MyOrder(self.driver)

    def go_to_member_center_page(self):
        """
        点击顶部的客户名称
        :return: 会员中心首页
        """
        self.click_loc(self.__username_loc)
        self.wait_title_change('会员中心首页')
        Log().info("点击顶部的客户名称，跳转到会员中心页面")
        from pages.memberCenterPage import MemberCenter
        return MemberCenter(self.driver)

    def go_back_to_homepage(self):
        """
        点击顶部的返回首页链接
        :return: 若当前页面存在该链接，则返回首页的page对象，否则返回None
        """
        is_display = EC.visibility_of_element_located(self.__back_to_homepage_loc)
        if is_display:
            self.click_loc(self.__back_to_homepage_loc)
            self.wait_title_change('九州通')
            Log().info("点击顶部的返回首页链接，返回首页")
            from pages.homePage import HomePage
            return HomePage(self.driver)
        else:
            Log().info("当前页面没有返回首页链接")

    def go_to_my_cart_page(self):
        """
        点击顶部右侧的我的购物车按钮
        :return: 若当前页面存在该链接，则返回我的购物车页面的对象，否则返回None
        """
        is_display = EC.visibility_of_element_located(self.__my_cart_button_loc)
        if is_display:
            self.click_loc(self.__my_cart_button_loc)
            self.wait_title_change('我的购物车')
            Log().info('点击顶部的我的购物车按钮，跳转到我的购物车页面')
            from pages.myCartPage import MyCart
            sleep(2)
            self.refresh()
            return MyCart(self.driver)
        else:
            Log().info("当前页面没有我的购物车按钮")

