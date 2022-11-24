# coding=utf-8
"""首页"""
from common.basePage import Action
from common.log import Log
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from time import sleep
from pages.prodSearchResultPage import SearchResult
from pages.loginPage import LoginPage
from common.commonMethod import CommonMethod
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.topCommonMenu.baseMenus import BaseMenus
import random
from common.fileReader import IniUtil

f = IniUtil()


class HomePage(BaseMenus):
    # ==============================================打开主页===========================================
    # 首页地址
    __home_page_url = CommonMethod().get_host()

    # 打开主页
    def open_homepage(self, url=__home_page_url):
        self.open(url, u'九州通')
        Log().info(u"打开首页: %s" % self.__home_page_url)

    # ===================================顶部登录和退出======================================

    '''右侧登录模块的元素'''
    __right_username_loc = ('xpath', '//*[@id="login_form_id"]/div[1]/span/input')
    __right_password_loc = ('xpath', '//*[@id="login_form_id"]/div[2]/span/input')
    __right_submit_loc = ('xpath', '//*[@id="login_form_id"]/div[4]/button')

    '''登录之后顶部用户名'''
    __top_u_username_loc = ('xpath', '//*[@class="userinfo"]/span')

    com = CommonMethod()

    '''退出按钮'''
    __log_out_loc = ('xpath', '//*[@class="outLogin"]/span')

    # 通过首页右边的登录模块登录
    def login_from_side(self, username, password):
        self.open(self.__home_page_url, title='九州通')
        Log().info(u"打开首页: %s" % self.__home_page_url)
        self.send_keys_loc(self.__right_username_loc, username)
        Log().info(u"在首页右侧用户名输入框输入：%s" % username)
        self.send_keys_loc(self.__right_password_loc, password)
        Log().info(u"在首页右侧密码输入框输入：%s" % password)
        self.enter_key(self.__right_password_loc)
        Log().info(u"点击登录")

    __guidance_step = ('xpath', '//*[@id="__layout"]//div[@class="text"]')

    # 首页引导操作
    def home_page_guidance(self):
        try:
            '''点击第一步'''
            self.click_loc(self.__guidance_step)
            '''点击第二步'''
            self.click_loc(self.__guidance_step)
            '''点击第三步'''
            self.click_loc(self.__guidance_step)
        except:
            pass

    __expired_certificate_loc = ('xpath', '//div[@class="el-dialog__footer"]/span/button[1]/span')

    # 首页证照过期
    def home_expired_certificate(self):
        try:
            self.click_loc(self.__expired_certificate_loc)
        except:
            pass

    __right_name_loc = ('xpath', '//div[@class="textAlignCenter"]/span')

    # 获取右侧用户名
    def get_right_name(self):
        text = self.get_text_loc(self.__right_name_loc)
        return text

    # 消息中心跳转
    __message_center_data1 = ('xpath',
                              '//*[@id="__layout"]/div/div/div[2]//div[@class="ph-icon_menus"]/div/div[1]/div/div[1]//div[@class="ph-menu"]/span[1]')
    __message_center_data2 = (
        'xpath', '//*[@id="__layout"]//div[@class="el-dialog__body"]//div[@class="ml-left"]/div/div')
    __message_center_data3 = (
        'xpath', '//*[@id="__layout"]/div/div/div[2]/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/button/i')

    def message_center(self):
        '''点击消息中心'''
        self.click_loc(self.__message_center_data1)
        text = self.get_text_loc(self.__message_center_data2)
        return text

    def close_message_center(self):
        '''关闭消息中心'''
        self.click_loc(self.__message_center_data3)

    # 顶部购物车跳转
    __shopping_data1 = ('xpath',
                        '//*[@id="__layout"]//div[@class="yjj_page_header"]//div[@class="ph-menus-item"][2]//div[@class="ph-menu"]/span[1]')
    __shopping_data2 = ('xpath', '//span[@class="title"]')

    def shopping_trolley(self):
        '''点击购物车'''
        self.click_loc(self.__shopping_data1)
        text = self.get_text_loc(self.__shopping_data2)
        return text

    # 右侧购物车跳转
    __right_shopping_data1 = ('xpath',
                              '//div[@class="shopping-card"]/div/i[@class="icon-cart"]')
    __right_shopping_data2 = ('xpath', '//span[@class="title"]')

    def right_shopping_trolley(self):
        '''点击购物车'''
        self.click_loc(self.__right_shopping_data1)
        text = self.get_text_loc(self.__right_shopping_data2)
        return text

    # 右侧反馈建议跳转
    __right_opinion_data1 = ('xpath',
                             '//div[@class="suggest"]/div/i[@class="icon-edit"]')
    __right_opinion_data2 = ('xpath', '//div[@id="tab-first"]')

    def right_opinion(self):
        '''点击反馈建议'''
        self.click_loc(self.__right_opinion_data1)
        text = self.get_text_loc(self.__right_opinion_data2)
        return text

    # 右侧平台客服跳转
    __right_call_center1 = ('xpath',
                            '//div[@class="suggest"]/div/i[@class="icon-service"]')
    __right_call_center2 = ('xpath', '//div[@class="status-bar"]/span[2]')
    __right_call_center3 = ('xpath', '//div[@id="em-kefu-webim-chat"]//i[@title="关闭"]')
    __frame_data = ('xpath', '//*[@id="cross-origin-iframe"]')

    def right_call_center(self):
        '''点击平台客服'''
        self.click_loc(self.__right_call_center1)
        sleep(2)
        # self.js_focus_element_loc(self.__frame_data)
        self.switch_frame(self.__frame_data)
        '''提取客服对话框断言字段'''
        text = self.get_text_loc(self.__right_call_center2)
        '''关闭客服对话框'''
        self.click_loc(self.__right_call_center3)
        return text

    # 右侧领劵中心跳转
    __right_coupon_center1 = ('xpath',
                              '//div[@class="fastEntrance"][1]/div[1]')
    __right_coupon_center2 = ('xpath', '//div[@class="ph-custom_content"]/div')

    def right__coupon_center(self):
        '''点击右侧领劵中心按钮'''
        self.click_loc(self.__right_coupon_center1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__right_coupon_center2)
        return text

    # 右侧常购清单跳转
    __right_often_buy1 = ('xpath',
                          '//div[@class="fastEntrance"][1]/div[2]')
    __right_often_buy2 = ('xpath', '//div[@class="ss-breadcrumbs"]/span')

    def right__often_buy(self):
        '''点击右侧常购清单按钮'''
        self.click_loc(self.__right_often_buy1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__right_often_buy2)
        return text

    # 右侧帮忙中心跳转
    __right_help_center1 = ('xpath',
                            '//div[@class="fastEntrance"][2]/div[1]')
    __right_help_center2 = ('xpath', '//div[@class="ph-content"]/span')

    def right__help_center(self):
        '''点击右侧帮忙中心按钮'''
        self.click_loc(self.__right_help_center1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__right_help_center2)
        return text

    # 右侧去还款跳转
    __right_repayment1 = ('xpath',
                          '//div[@class="fastEntrance"][2]/div[2]')
    __right_repayment2 = ('xpath', '//span[@class="title"]')

    def right__repayment(self):
        '''点击右侧去还款按钮'''
        self.click_loc(self.__right_repayment1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__right_repayment2)
        return text

    # 右侧发票管理跳转
    __right_invoice_management1 = ('xpath',
                                   '//div[@class="fastEntrance"][2]/div[3]')
    __right_invoice_management2 = ('xpath', '//div[@class="invoice-header"]/span')

    def right__invoice_management(self):
        '''点击右侧发票管理按钮'''
        self.click_loc(self.__right_invoice_management1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__right_invoice_management2)
        return text

    # 顶部我的订单跳转
    __top_my_order1 = ('xpath',
                       '//div[@class="content"]/div[@class="right"]/span[2]')
    __top_my_order2 = ('xpath', '//div[@class="ph-paths"]/span[1]')

    def top_my_order(self):
        '''点击顶部我的订单按钮'''
        self.click_loc(self.__top_my_order1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__top_my_order2)
        return text

    # 顶部会员中心跳转
    __top_member_center1 = ('xpath',
                            '//div[@class="content"]/div[@class="right"]/span[3]')
    __top_member_center2 = ('xpath', '//div[@class="ph-paths"]/span')

    def top_member_center(self):
        '''点击顶部会员中心按钮'''
        self.click_loc(self.__top_member_center1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__top_member_center2)
        return text

    # 顶部客户服务跳转
    __top_customer_service1 = ('xpath',
                               '//div[@class="content"]/div[@class="right"]/span[4]')
    __top_customer_service2 = ('xpath', '//ul/li[@class="el-dropdown-menu__item"]')
    __top_customer_service3 = ('xpath', '//div[@class="ph-content"]/span')

    def top_customer_service(self):
        '''移动到顶部客户服务下面'''
        self.move_to_element(self.__top_customer_service1)
        sleep(1)
        '''点击帮助中心按钮'''
        self.click_loc(self.__top_customer_service2)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        text = self.get_text_loc(self.__top_customer_service3)
        return text

    # 退出登录
    def log_out(self):
        # 移动到用户账号下
        self.move_to_element(self.__top_u_username_loc)
        sleep(1)
        self.click_by_mouse(self.__log_out_loc)
        # self.click_loc(self.__log_out_loc)
        Log().info(u"退出登录")

    # 右侧退出
    __right_login_out_loc = ('xpath', '//div[@class="l_logout"]/a/span[text()="退出"]')

    def right_login_out_method(self):
        """右侧退出登陆方法"""
        self.js_focus_element_loc(self.__right_login_out_loc)
        self.click_loc(self.__right_login_out_loc)

    # 顶部用户名称
    __top_user_name_loc = ('xpath', '//*[@class="userinfo"]/span')

    def move_to_username(self):
        # 鼠标悬浮在顶部用户名
        self.move_to_element(self.__top_u_username_loc)

    __top_text_username_loc = ('xpath', '//h3[@onclick="memberHomeTop(this)"]')

    def check_top_username(self):
        """
        鼠标悬浮用户名后，下拉框显示的用户名
        :return:
        """
        name = self.get_text_loc(self.__top_text_username_loc)
        return name

    def click_top_username(self):
        """
        鼠标悬浮用户名后，下拉框显示用户名，点击用户名跳转个人中心
        :return:
        """
        # 鼠标悬浮在顶部用户名
        self.move_to_username()
        self.click_loc(self.__top_text_username_loc)
        self.wait_title_change('会员中心首页')
        Log().info("鼠标悬浮用户名后，下拉框显示用户名，点击用户名跳转个人中心")
        return

    # 左上角鼠标悬浮用户名后，下拉框显示的"个人中心"
    __top_membercenter_loc = ('xpath', '//div[@class="list"]/a[@class="goMember"]')

    def check_top_membercenter(self):
        """
        鼠标悬浮用户名后，下拉框显示个人中心
        :return:
        """
        name = self.get_text_loc(self.__top_membercenter_loc)
        return name

    def click_top_membercenter(self):
        """
        鼠标悬浮用户名后，下拉框显示的用户名，点击跳转个人中心
         :return:
        """
        # 鼠标悬浮在顶部用户名
        self.move_to_username()
        self.click_loc(self.__top_membercenter_loc)
        self.wait_title_change('会员中心首页')
        Log().info("鼠标悬浮用户名后，下拉框显示的个人中心，点击跳转个人中心")
        return

    # ====================================首页输入框搜索=====================================================
    # 搜索框
    __search_text_loc = ('xpath', '//div[@class="yjj_page_header"]//div[@class="ph-si-el_input el-input"]/input')
    # 搜索按钮
    __search_button_loc = (
    'xpath', '//div[@class="yjj_page_header"]//button[@class="el-button ph-si-btn el-button--default"]')
    # 搜索结果页面文本获取
    __search_result_loc = ('xpath', '//div[@class="ss-breadcrumbs"]/span[2]')
    # 搜索历史模块
    __search_history_loc = ('xpath', '//*[@id="searchHis"]')
    # 搜索历史模块中的搜索历史列表
    __search_history_list_loc = ('xpath', '//*[@id="searchHis"]/ul/li')
    # 搜索历史列表中，被选中的商品
    __search_history_selected_loc = ('xpath', '//*[@id="searchHis"]/ul/li[contains(@style,"rgb(238, 244, 250)")]/a')

    # 搜索框不输入，点击搜索按钮跳转到搜索页面
    def search_jump(self):
        self.click_loc(self.__search_button_loc)
        sleep(1)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()

    # 搜索框输入，搜索
    def search_goods(self, keywords=''):
        sleep(2)
        self.move_to_element(self.__search_text_loc)
        self.send_keys_loc(self.__search_text_loc, keywords)
        self.click_loc(self.__search_button_loc)
        # self.enter_key(self.__search_text_loc)
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        sleep(1)
        self.switch_window()
        # 获取商品列表页面，搜索名称
        result = self.get_text_loc(self.__search_result_loc)
        return result
        # self.move_to_element(self.__search_button_loc)
        # self.click_loc(self.__search_button_loc)
        # print("点击搜索按钮")
        # 等待页面跳转到搜索结果页面
        # self.wait_title_change('商品搜索列表', timeout=30)
        # Log().info(u'跳转到商品搜索列表页面')
        # from pages.prodSearchResultPage import SearchResult
        # return SearchResult(self.driver)

    # 判断是否有搜索历史列表
    def is_search_history_exist(self):
        # 如果搜索列表存在，就代表有历史搜索记录，否则就代表无历史搜索记录
        is_exist = self.is_located(self.__search_history_list_loc, is_all=True)
        if is_exist:
            return True
        else:
            return False

    # 获取搜索历史的div的显示属性
    def get_attribute_of_search_history(self):
        # 获取搜索历史的div的显示属性,也就是style的属性,style = display: none;时，搜索历史处于不显示的状态，style = display: block;时处于显示状态
        attr = self.get_attribute_loc(self.__search_history_loc, 'style')
        return attr

    # 获取鼠标点击搜索文本框之后，搜索历史的div的显示属性
    def get_search_history_after_click(self):
        #  鼠标点击搜索框
        self.click_loc(self.__search_text_loc)
        # 等待1秒
        sleep(1)
        # 先判断搜索历史记录列表是否存在
        is_exist = self.is_search_history_exist()
        if is_exist:
            # 如果存在，获取搜索历史的div的属性
            attr = self.get_attribute_of_search_history()
            return attr
        else:
            # 如果不存在，返回None
            return None

    # 搜索框内，键盘的上下键操作，选择搜索历史 -- 向下键
    def key_down_in_search_textbox(self, n=1):
        #  向下
        for i in list(range(n)):
            self.down_key(self.__search_text_loc)
            i = i + 1
            if i == n:
                break

    # 搜索框内，键盘的上下键操作，选择搜索历史 -- 向上键
    def key_up_in_search_textbox(self):
        # 向上
        self.up_key(self.__search_text_loc)

    # 获取点击搜索框之后，下拉框弹出的搜索列表中被选中的商品的名称,被选中的商品，<li>的style包含background: rgb(238, 244, 250);
    def get_focus_prod_in_search_textbox(self):
        try:
            # 找到被选中的商品，就返回商品的名称
            prod_name = self.get_text_loc(self.__search_history_selected_loc)
            return prod_name
        except TimeoutException:
            #  未找到被选中的商品，就返回None
            return None

    # 点击选中的商品，进入搜索详情页
    def click_selected_prod_in_history(self):
        # 如果有选中的历史记录，就点击该链接
        if self.get_focus_prod_in_search_textbox() is not None:
            self.click_loc(self.__search_history_selected_loc)
            return SearchResult(self.driver)

    # ===============================登陆成功后右侧客户信息===========================================

    # 获取登录之后，首页顶部的用户名信息
    def get_top_username(self):
        return self.get_text_loc(self.__top_user_name_loc)

    #
    # # 获取登陆之后，首页右边的用户名信息
    # def get_right_username(self):
    #     return self.get_text_loc(__self.right_u_username_loc)

    '''登录之后右侧用户名'''
    __right_u_username_loc = ('xpath', '//a[@class="u_mmb_name"]')

    # 比较顶部和右边用户信息是否一致
    def compare_username(self):
        top_username = self.get_text_loc(self.__top_u_username_loc)
        right_username = self.get_text_loc(self.__right_u_username_loc)
        result = True if top_username == right_username else False
        return result

    # 点击登陆之后右侧用户名
    def click_username_on_right(self):
        self.click_loc(self.__right_u_username_loc)

    # ==========================================左侧所有商品分类======================================

    # 左侧商品分类栏
    __prod_category_loc1 = ('xpath', '//div[@class="acc-title"]')
    __prod_category_loc2 = ('xpath', '//div[@id="level1"]/div[1]/div[1]/span')
    __prod_category_loc3 = ('xpath', '//div[@class="ss-breadcrumbs-selected"]/div/span[1]')

    # 全部商品分类，选择第一个分类提取文本
    def goods_category_text(self):
        # 移动到所有商品分类下面
        self.move_to_element(self.__prod_category_loc1)
        try:
            # 获取第一个分类名称
            result = self.get_text_loc(self.__prod_category_loc2)
            return result
        except TimeoutException:
            print("无商品分类，请先配置分类！")

    # 全部商品分类，选择第一个分类跳转
    def goods_category(self):
        # 移动到所有商品分类下面
        self.move_to_element(self.__prod_category_loc1)
        sleep(1)
        try:
            self.js_focus_element_loc(self.__prod_category_loc2)
            # 点击第一个分类
            self.click_loc(self.__prod_category_loc2)
        except TimeoutException:
            Log().info("无商品分类，请先配置分类！")
        """切换window，针对打开多个窗时,切换窗口，默认切换到最新的一个窗口"""
        self.switch_window()
        # 获取商品列表页面，分类名称
        result = self.get_text_loc(self.__prod_category_loc3)
        return result

    '''
    # 获取所有的分类
    def get_categories(self):
        categories = []
        try:
            categories = self.find_elements(self.__prod_category_loc)
        except TimeoutException:
            print(u"无商品分类，请先配置分类！")
        return categories

    # 获取商品分类数量
    def count_of_categories(self):
        return len(self.get_categories())

    # 点击任意一商品分类,同时返回该链接指向的部分链接
    def click_category(self):
        count = self.count_of_categories()
        if count > 0:
            x = random.randint(0, count - 1)
            ele = self.get_categories()[x]
            # 获取该分类指向的链接（除去base url以外）
            part_url = self.get_attribute_ele(ele, 'onclick').split("'")[1]
            # 点击该分类
            self.click_element(ele)
            Log().info("点击商品分类：%s" % part_url.split("=")[1])
            return part_url
    '''

    # ==========================================导航栏信息======================================

    def click_navigation_text(self):
        """
        点击指定的导航栏
        :return:
        """
        navigation_text_loc = ('xpath', '//ul[@id="nav_barIdforInte"]/li[1]/a')
        self.js_focus_element_loc(navigation_text_loc)
        self.click_loc(navigation_text_loc)

    # ===============================右侧快捷入口信息===========================================

    # 首页右侧的优惠券图标 //*[@id='tool_entey']//span[text()='领券中心']
    __yhj_loc = ('xpath', "//*[@id='tool_entey']//span[text()='领券中心']")

    # 侧边栏个人中心优惠券后面的数字
    __yhj_number_loc = ('xpath', '//div[@id="custInfo"]//a[@class="m_my_coupon_num"]')

    # 侧边栏个人中心按钮"去领券"
    __yhj_get_loc = ('xpath', "//div[@class='m_my_coupon']//a[@class='m_my_gotoGet']")

    def click_myyhj(self):
        """
        # 点击首页右侧侧边栏个人中心icon-按钮"去领券"-进入领券中心页面
        :return:
        """
        # 点击我的优惠券后面的去领券
        self.click_loc(self.__yhj_get_loc)
        # 等待第二个窗口打开
        self.wait_until_windows_open()
        # 切换窗口
        self.switch_window()
        # 等待窗口title变成
        WebDriverWait(self.driver, timeout=10).until(EC.title_is('领券中心'))
        from pages.pagesFromMemberCenter.couponCenterPage import CouponCenter
        return CouponCenter(self.driver)

    # ===============================右侧快捷楼梯信息=======================================================

    # 点击侧边栏咨询客服icon到达“客服系统”页面。
    click_im_icon_loc = ('xpath', '//a[@class="u_s_icon icon_service"]')

    def click_im_icon(self):
        self.js_focus_element_loc(self.click_im_icon_loc)
        self.click_loc(self.click_im_icon_loc)
        Log().info(u"点击侧边栏客服系统icon")

    # ===============================================首页楼层信息=============================================
    # 首页楼层元素
    __fristpage_floor = ('xpath', '//*[contains(@class,"m_sec_hd")]')

    # 检查首页楼层元素是否存在
    def check_homepage_floor(self):
        try:
            result = self.is_display_all(self.__fristpage_floor)
            if result is not None:
                result = True
        except TimeoutException:
            result = False
        return result

    click_first_adv_loc = ('xpath', '//div[@class="m_focus_advert"]/a[1]/img')

    def click_first_adv_image(self):
        self.js_focus_element_loc(self.click_first_adv_loc)
        self.click_loc(self.click_first_adv_loc)
        Log().info(u"点击广告专区第一个图片")

    click_first_activity_loc = ('xpath', '//div[@class="u_activity_entry"]/a[1]')

    def click_first_activity_image(self):
        self.js_focus_element_loc(self.click_first_activity_loc)
        self.click_loc(self.click_first_activity_loc)
        Log().info(u"点击活动第一个图片")

    # ===============================================首页楼层商品信息=============================================

    # 商品图片
    __prod_pic_list_loc1 = ('xpath', '//a[@class="m_goods_img"]')
    __prod_pic_list_loc2 = ('xpath',
                            '//div[contains(@class, "u_template ")]/div[@class="templateCon"]//span[contains(@class, "name")]/following-sibling::a[1]')
    # 商品名称
    __prod_name_list_loc1 = ('xpath', '//a[@class="u_goods_name"]')
    __prod_name_list_loc2 = ('xpath', '//div[contains(@class, "u_template")]//span[contains(@class, "name ")]/a')
    # 非会员价格
    __unhuiyuan_price_loc = ('xpath', '//i[@class="u_uservipimg"]/../../../div[@class="u_info_nomember"]')
    # 首页皇冠图表logo
    __shouyehuangguan_logo = ('xpath', '//img[@id="indexVipPngDiv"]')

    # 获取会员登录情况下的会员商品的非会员价格集合
    def get_unhuiyuan_prices(self):
        """
        获取会员登录情况下的会员商品价格结合list
        :return:
        """
        info = []
        price_list = self.find_elements(self.__unhuiyuan_price_loc)
        # print("price_list为%s" % price_list)
        if len(price_list) > 0:
            for ele in price_list:
                # print("当前ele为：%s" % ele)
                unhuiyuan_price = float(self.get_text_content_ele(ele).split('¥')[1])
                info.append(unhuiyuan_price)
        return info

    # 获取首页所有商品
    def get_prod_list(self):
        prod_list = []
        try:
            prod_list = self.find_elements(self.__prod_name_list_loc2)
        except TimeoutException:
            print("No prod in list.")
        return prod_list

    # 获取首页会员商品数量
    def huiyuan_count_of_prods(self):
        return len(self.find_elements(self.__unhuiyuan_price_loc))

    # 获取首页商品数量
    def count_of_prods(self):
        return len(self.get_prod_list())

    # 获取首页所有商品的name和prodno
    def get_prods_info(self):
        info = []
        if self.count_of_prods() > 0:
            for ele in self.get_prod_list():
                prodno = self.get_attribute_ele(ele, 'href').split('/')[-1]
                # print("1-%s" % prodno)
                prodname1 = self.get_attribute_ele(ele, 'text')
                # print("首页获取的原始商品名称为：%s" % prodname1)
                # prodname = self.get_attribute_ele(ele, 'text').split(' ')[0]
                prodname = self.get_attribute_ele(ele, 'text')
                info.append((prodno, prodname))
        return info

    # 任意点击首页中的一个商品的图片， 并返回该商品的prodno和prodname
    def click_picture(self):
        count = self.count_of_prods()
        if count > 0:
            # 获取所有商品图片
            pictures = self.find_elements(self.__prod_pic_list_loc2)
            # x = random.randint(0, count - 1)
            # x = len(pictures)
            # print(x)
            # 拿到商品列表中的一个随机商品
            ele = pictures[0]
            self.js_focus_element_ele(ele)
            self.visibility_of(ele, 10)
            sleep(1)
            # 获取该商品的prodno和prodname
            info = self.get_prods_info()[0]
            print(info)
            # 点击该商品的图片
            self.click_element(ele)
            return info
        else:
            return ()

    # 任意点击首页中的一个商品的名称， 并返回该商品的prodno和prodname
    def click_title(self):
        count = self.count_of_prods()
        print(count)
        if count > 0:
            # 获取所有商品名称
            name = self.find_elements(self.__prod_name_list_loc2)
            # x = random.randint(0, count-1)
            # print("=====",x,"======")
            # 拿到商品列表中的一个随机商品
            ele = name[0]
            self.js_focus_element_ele(ele)
            self.visibility_of(ele, 10)
            sleep(1)
            # 获取该商品的prodno和prodname
            info = self.get_prods_info()[0]
            print(info)
            # 点击该商品的名称
            self.send_keys_element(ele)
            return info
        else:
            return ()

    # ========================================页面等待===================================="""

    def wait_homepage_refresh(self, timeout=10):
        """
        等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断
        这里首页的搜索按钮若过期，代表页面已经刷新（已经打开别的页面）
        """
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    def wait_title_change(self, title, timeout=5):
        """等待新打开直到窗口title出现"""
        try:
            self.is_title_contains(title, timeout)
        except TimeoutException:
            pass
