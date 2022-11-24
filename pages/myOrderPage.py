"""我的订单页面"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException
from common.log import Log
from pages.topCommonMenu.baseMenus import BaseMenus
from common.updateDataFromDB import OperationInDB
from common.fileReader import IniUtil
from time import sleep


class MyOrder(BaseMenus):

    f = IniUtil()
    # 订单号列表-订单同步2.0
    __order2_list_loc = ('xpath', '//div[@class="m_b_status_t"]/p[2]/a')
    # 立即支付按钮-订单同步2.0
    __order2_pay_now_button= ('xpath', '//p[@class="orderDetail_c_b orderStatusDesc"]')
    # 订单编码部分路径（以订单号为基准）
    # __ = ('xpath', '//*[@id="orderForm"]/div/div/ul[2]/li/div/p[2]/span/ancestor::li[1]/ul/li/a')
    __order_code_path = '//*[@id="orderForm"]/div/div/ul[2]/li/div/p[2]/span[contains(text(),"'
    __other_path = '")]/ancestor::li[1]/ul/li/a'
    # 我的订单页面第一条记录的订单状态
    __first_order_status = ('xpath', '//ul[@class="m_b_status_c"]/li[1]//li[@class="col-md-2 orderStatusDesc"]')
    # 第一个订单查看链接
    __first_order_button = ('xpath', '//li[@class="li-cont"][1]//div[text()="查看详情"]')

    # 点击第一个订单进入订单详情页，并返回driver
    def go_to_frist_order_detail(self):
        # 点击第一个订单进入订单详情页
        self.js_focus_element_loc(self.__first_order_button, bottom=False)
        self.click_loc(self.__first_order_button)
        self.switch_window()
        sleep(2)
        # 等待页面跳转
        # self.wait_title_change("订单详情页")
        # 返回订单详情页page
        # from pages.orderDetailsPage import OrderDetails
        # return OrderDetails(self.driver)

    # 获取订单列表
    def get_order_list(self):
        order_list = []
        order_list = self.find_elements(self.__order2_list_loc)
        return order_list

    def is_pay_now_button_display(self):
        """
        订单同步2.0：判断立即支付按钮是否存在
        :return:
        """
        try:
            result = self.is_visibility(self.__order2_pay_now_button)
            print(result)
            result = True
        except TimeoutException:
            result = False
        return result

    # 根据订单号判断订单是否在订单列表里面-
    def is_in_order_list(self, order_num):
        order_info_list = self.get_order_list()
        order_list = {}
        status = ''
        order_nums = ''
        # 立即支付按钮的定位
        pay_now_button = ('xpath', '//a[contains(@onclick,"payOrder(' + order_num + ')") and @class="btn btn-p orderPayBtn"]')
        # print(pay_now_button)
        try:
            # 如果立即支付按钮 存在，则判断支付不成功
            self.is_display(pay_now_button)
            Log().info("订单: %s 支付不成功" % order_num)
        except:
            Log().info("订单: %s 支付成功" % order_num)
            order_nums = self.get_text_loc(self.__order2_list_loc)
        if order_num in order_nums:
            return True, status
        else:
            return False, None

    def open_order_details(self, order_num):
        """
        打开订单详情页
        :param order_num: 订单编号
        :return:
        """
        if self.is_in_order_list(order_num)[0]:
            self.click_loc(self.__order2_list_loc)
        else:
            Log().info(u'订单编号: %s 不在订单列表里面.' % order_num)

    def get_first_order_status(self):
        """
        获取第一条订单的状态
        :return:
        """
        first_status = self.get_text_loc(self.__first_order_status)
        Log().info("第一条订单的状态为：%s" % first_status)
        return first_status

    # 第一条订单的单据编号
    __first_order_billid = ('xpath', '//ul[@class="m_b_status_c"]/li[1]//a[@class="font-td-ch addCartAgainOrderCode"]')
    def get_first_billid(self):
        """
        获取第一条订单的单据编号,类似：FDGXSG08581690
        :return:
        """
        first_status = self.get_first_order_status()
        if first_status == '正在拣货':
            billid = self.get_text_loc(self.__first_order_billid)
            print(billid)
            return billid
        else:
            Log().info("订单状态还不是正在拣货")

    # 第一条订单的DM编号
    __first_order_DM = ('xpath', '//ul[@class="m_b_status_c"]/li[1]//span[contains(text(),"DM")]')
    def get_first_DM(self):
        """
        获取第一条订单的DM编号，类似：DM_20190221_000003
        :return:
        """
        first_status = self.get_first_order_status()
        if first_status == '正在拣货':
            DM_code = self.get_text_loc(self.__first_order_DM)
            print(DM_code)
            return DM_code
        else:
            Log().info("订单状态还不是正在拣货")

    # ====================================================== 订单列表操作 =======================================

    # 选择订单时间
    __my_oreder_time_type_loc = ('xpath','//span[@class="u_dropdown_hover"]')
    # 选择近半年类型
    __my_order_half_year_loc = ('xpath','//a[text()="近半年内订单"]')

    def click_my_order_type(self):
        """选择半年内的订单"""
        try:
            self.move_to_element(self.__my_oreder_time_type_loc)
            self.js_focus_element_loc(self.__my_order_half_year_loc)
            self.click_loc(self.__my_order_half_year_loc)
        except:
            Log().info('选择订单时间类型错误')

    # 我的订单页面搜索元素
    __my_order_searcg_loc = ('xpath','//input[@id="searchQuery"]')

    def custom_order_search(self,code):
        """进行订单搜索"""
        try:
            self.js_focus_element_loc(self.__my_order_searcg_loc)
            self.send_keys_loc(self.__my_order_searcg_loc,code)
            self.enter_key(self.__my_order_searcg_loc)
        except:
            Log().info('我的订单页面进行订单搜索错误')

    # 获取第一个订单再次购买元素
    __order_prod_agaiin_add_loc = ("xpath",'//ul[@class="m_b_status_c"]/li[1]//a[text()="再次购买"]')

    def click_again_add_prod(self):
        """第一个订单点击再次购买"""
        try:
            self.js_focus_element_loc(self.__order_prod_agaiin_add_loc)
            self.click_loc(self.__order_prod_agaiin_add_loc)
        except:
            Log().info('点击此次购买错误')

    __my_car_loc = ("xpath",'//div[@class="ph-icon_menus"]/div/div[2]/div/img[1]')

    # 点击购物车图标
    def click_my_car(self):
        self.click_loc(self.__my_car_loc)
        sleep(2)

