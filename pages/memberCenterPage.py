"""会员中心页面"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common.log import Log
from pages.prodSearchResultPage import SearchResult
from time import sleep
from common.commonMethod import CommonMethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.topCommonMenu.baseMenus import BaseMenus
import requests
import time
from common.fileReader import IniUtil


class MemberCenter(BaseMenus):

    '''
    f = IniUtil()
    # 获取当前订单数据来源，返回1代表订单同步1.0，返回2代表订单同步2.0
    order_version = f.get_value_of_option('test_data', 'order_version')
    '''

    # ======================================打开会员中心===========================================
    __member_page_url = CommonMethod().get_endpoint('memberpage')

    # 打开会员中心页面
    def open_center_page(self):
        self.open(self.__member_page_url, '个人中心')

    __member_center_guidance_loc = ('xpath', '//div[@class="guide"]/div/div[4]')

    # 会员中心引导步骤
    def member_center_guidance(self):
        try:
            # 点击第一步
            self.click_loc(self.__member_center_guidance_loc)
            # 点击第二步
            self.click_loc(self.__member_center_guidance_loc)
        except TimeoutException:
            pass

    # ======================================搜索模块===========================================

    # 搜索框
    __search_text_loc = ('xpath', '//*[@id="searchText"]')
    __search_button_loc = ('xpath', "//div[contains(@class, 'u_search_box')]/button")
    # 搜索历史模块
    __search_history_loc = ('xpath', '//*[@id="searchHis"]')
    # 搜索历史模块中的搜索历史列表
    __search_history_list_loc = ('xpath', '//*[@id="searchHis"]/ul/li')
    # 搜索历史列表中，被选中的商品
    __search_history_selected_loc = ('xpath', '//*[@id="searchHis"]/ul/li[contains(@style,"rgb(238, 244, 250)")]/a')

    # 搜索
    def search_goods(self, keywords=''):
        sleep(2)
        self.send_keys_loc(self.__search_text_loc, keywords)
        # self.click_loc(self.__search_button_loc)
        self.enter_key(self.__search_text_loc)
        # 等待页面跳转到搜索结果页面
        self.wait_title_change('商品搜索列表', timeout=30)
        Log().info(u'跳转到商品搜索列表页面')
        from pages.prodSearchResultPage import SearchResult
        return SearchResult(self.driver)

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
        sleep(2)
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

    # 搜索历史列表，点击选中的商品，进入搜索详情页
    def click_selected_prod_in_history(self):
        # 如果有选中的历史记录，就点击该链接
        if self.get_focus_prod_in_search_textbox() is not None:
            self.click_loc(self.__search_history_selected_loc)
            return SearchResult(self.driver)

    # ======================================客户信息===============================================

    # 客户名称
    __customer_name_loc = ('xpath', "//p[contains(@class, 'user_box_tit_change')]")

    def get_customer_name(self):
        """
        # 获取客户名称
        :return:
        """
        try:
            text = self.get_text_loc(self.__customer_name_loc)
        except:
            text = ''
        return text

    # 充值/回款链接
    __recharge_link_loc = ('xpath', "//span[text()='充值/还款']")

    # 点击充值
    def recharge(self):
        # 点击充值
        self.click_loc(self.__recharge_link_loc)
        # 等待窗口title变成
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains('选择支付方法'))
        from pages.paymentProcessPages.receivedPayments.receivedPaymentsPaymentPage import ReceivedPaymentsPayment
        return ReceivedPaymentsPayment(self.driver)

    __coupon_button_loc = ('xpath', '//div[@class="coupon"]/div[@class="mt"]/span[2]')
    __get_coupon_centre = ('xpath', '//*[@id="__layout"]/div/div/div[2]/div/div/div[2]/div')

    # 点击领劵
    def click_coupon_button(self):
        self.click_loc(self.__coupon_button_loc)
        sleep(3)
        text = self.get_text_loc(self.__get_coupon_centre)
        return text

    __details_view_loc = ('xpath', '//div[@class="balance"]/div[@class="mt"]/span[text()="查看明细"]')
    __get_details_loc = ('xpath', '//div[@class="count-title"]')

    # 点击查看明细
    def click_details_view(self):
        self.click_loc(self.__details_view_loc)
        sleep(3)
        text = self.get_text_loc(self.__get_details_loc)
        return text

    __wallet_recharge_loc = ('xpath', '//div[@class="balance"]/div[@class="mt"]/span[text()="充值"]')
    __get_wallet_recharge_text = ('xpath', '//div[@class="content"]/span[@class="title"]')

    # 点击钱包充值
    def click_wallet_recharge(self):
        try:
            self.click_loc(self.__wallet_recharge_loc)
            sleep(3)
            text = self.get_text_loc(self.__get_wallet_recharge_text)
            return text
        except TimeoutException:
            print("没有找到充值按钮")

    __repayment_loc = ('xpath', '//div[@class="arrears"]/div[@class="mt"]/span[2]')
    __get_repayment_loc = ('xpath', '//span[@class="title"]')

    # 点击还款
    def click_repayment(self):
        self.click_loc(self.__repayment_loc)
        sleep(3)
        text = self.get_text_loc(self.__get_repayment_loc)
        return text

    # 左侧我的优惠券链接
    __my_coupon_link_loc = ('xpath', '//*[@id="coupon_id"]')

    # 点击我的优惠券链接，打开我的优惠券页面
    def open_my_coupon_by_link(self):
        # 点击左侧的优惠券链接
        self.click_loc(self.__my_coupon_link_loc)
        # 等待第二个窗口打开
        self.wait_until_windows_open()
        # 切换窗口
        self.switch_window()
        # 等待窗口title变成
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains('我的优惠券'))
        from pages.pagesFromMemberCenter.couponCenterPage import CouponCenter
        return CouponCenter(self.driver)

    # 【立即预存】按钮
    __preStore__loc = ('xpath', '//div[@class="prestore_box"]/div[@class="box4"]//a')

    # 点击立即预存按钮，进入预存专题
    def get_into_preStore(self):
        self.click_loc(self.__preStore__loc)
        self.wait_until_windows_open()
        # 切换窗口
        self.switch_window()
        # 等待窗口title变成
        # WebDriverWait(self.driver, timeout=5).until(EC.title_is('预存赢好礼专题页'))
        from pages.paymentProcessPages.Prestore.prestorePaymentPage import PrestorePaymentPage
        return PrestorePaymentPage(self.driver)

    def is_prestore_end(self):
        """
        判断当前预存活动是否结束
        :return:
        """
        print(self.get_text_loc(self.__preStore__loc))
        end = '立即预存' in self.get_text_loc(self.__preStore__loc)
        if end is True:
            return True
        else:
            Log().info('预存活动已经结束！')
            return False

    # 预存货款金额
    __preStore_price = ('xpath', '//div[@class="pirce"]/span')

    def get_preStore_price(self):
        """
        获取预存货款的金额
        :return: 预存货款的金额
        """
        preStore_price = self.get_text_loc(self.__preStore_price)
        Log().info('预存货款的金额为：%s' % preStore_price)
        return float(preStore_price)

    # ======================================左侧菜单操作===============================================

    # 我的订单
    __wddd_loc = ('xpath', '//*[@id="dd_id"]')

    # 点击我的订单
    def click_wddd(self):
        try:
            self.js_focus_element_loc(self.__wddd_loc)
            self.click_loc(self.__wddd_loc)
            from pages.myOrderPage import MyOrder
            return MyOrder(self.driver)
        except TimeoutException:
            Log().info(u"未找到我的订单菜单！")

    # 历史采购
    __lscg_loc = ('xpath', '//span[text()="历史采购"]')
    __lscg_text_loc = ('xpath', '//div[@class="historyTitle"]/span[@class="title"]')

    # 点击历史采购
    def click_lscg(self):
        try:
            self.js_focus_element_loc(self.__lscg_loc)
            self.click_loc(self.__lscg_loc)
            text = self.get_text_loc(self.__lscg_text_loc)
            return text
        except TimeoutException:
            Log().info(u"未找到历史采购菜单！")

    # 缺货篮
    __wdqhl_loc = ('xpath', '//li[@class="second-li"]/span[text()="我的缺货篮"]')
    __wdqhl_text_loc = ('xpath', '//div[@class="ph-paths"]/span[text()="我的缺货篮"]')

    # 关注中心-点击我的缺货篮
    def click_wdqhl(self):
        try:
            self.js_focus_element_loc(self.__wdqhl_loc)
            self.click_loc(self.__wdqhl_loc)
            text = self.get_text_loc(self.__wdqhl_text_loc)
            return text
        except TimeoutException:
            Log().info(u"未找到我的缺货篮菜单！")

    # 订单中心-点击退货/售后跳转
    __sales_return_loc = ('xpath', '//span[text()="退货/售后"]')
    __sales_return_text_loc = ('xpath', '//div[@class="top"]/span[1]')

    def click_sales_return(self):
        try:
            self.js_focus_element_loc(self.__sales_return_loc)
            self.click_loc(self.__sales_return_loc)
            text = self.get_text_loc(self.__sales_return_text_loc)
            return text
        except TimeoutException:
            Log().info(u"未找到我的关注菜单！")

    # 订单中心-点击退货/售后-售后申请列表搜索
    def sales_return_application_list(self):
        __extract_prodname_loc = ('xpath', '//div[@class="orderList"][1]/div[2]/div/div[1]/ul/li/div/div[1]/div[2]/div[1]')
        __search_box_loc = ('xpath', '//div[@class="top"]/span[5]/div/input')
        # 提取列表第一个商品名称
        prod_name1 = self.get_text_loc(__extract_prodname_loc)
        # 通过商品名称搜索
        self.send_keys_loc(__search_box_loc, text=prod_name1)
        self.enter_key(__search_box_loc)
        sleep(3)
        # 提取列表第一个商品名称
        prod_name2 = self.get_text_loc(__extract_prodname_loc)
        return prod_name1, prod_name2

    # 订单中心-点击退货/售后-申请记录列表搜索
    def application_record_list(self):
        __application_record_loc = ('xpath', '//div[@class="top"]/span[2]')
        __extract_prodname_loc = (
        'xpath', '//div[@class="orderList"][1]/div[2]/div/div[1]/ul/li/div/div[1]/div[2]/div[1]')
        __search_box_loc = ('xpath', '//div[@class="top"]/span[5]/div/input')
        # 点击申请记录列表
        self.click_loc(__application_record_loc)
        sleep(2)
        # 提取列表第一个商品名称
        prod_name1 = self.get_text_loc(__extract_prodname_loc)
        # 通过商品名称搜索
        self.send_keys_loc(__search_box_loc, text=prod_name1)
        self.enter_key(__search_box_loc)
        sleep(3)
        # 提取列表第一个商品名称
        prod_name2 = self.get_text_loc(__extract_prodname_loc)
        return prod_name1, prod_name2

    # 订单中心-点击退货/售后-处理中列表搜索
    def being_processed_list(self):
        __being_processed_loc = ('xpath', '//div[@class="top"]/span[3]')
        __extract_prodname_loc = (
        'xpath', '//div[@class="orderList"][1]/div[2]/div/div[1]/ul/li/div/div[1]/div[2]/div[1]')
        __search_box_loc = ('xpath', '//div[@class="top"]/span[5]/div/input')
        # 点击处理中列表
        self.click_loc(__being_processed_loc)
        sleep(2)
        # 提取列表第一个商品名称
        prod_name1 = self.get_text_loc(__extract_prodname_loc)
        # 通过商品名称搜索
        self.send_keys_loc(__search_box_loc, text=prod_name1)
        self.enter_key(__search_box_loc)
        sleep(3)
        # 提取列表第一个商品名称
        prod_name2 = self.get_text_loc(__extract_prodname_loc)
        return prod_name1, prod_name2

    # 订单中心-点击退货/售后-召回商品列表搜索
    def recall_of_goods_list(self):
        __recall_of_goods_loc = ('xpath', '//div[@class="top"]/span[4]')
        __extract_prodname_loc = (
            'xpath', '//div[@class="orderList"][1]/div[2]/div/div[1]/ul/li/div/div[1]/div[2]/div[1]')
        __search_box_loc = ('xpath', '//div[@class="top"]/span[5]/div/input')
        # 点击召回商品记录列表
        self.click_loc(__recall_of_goods_loc)
        sleep(2)
        # 提取列表第一个商品名称
        prod_name1 = self.get_text_loc(__extract_prodname_loc)
        # 通过商品名称搜索
        self.send_keys_loc(__search_box_loc, text=prod_name1)
        self.enter_key(__search_box_loc)
        sleep(3)
        # 提取列表第一个商品名称
        prod_name2 = self.get_text_loc(__extract_prodname_loc)
        return prod_name1, prod_name2

    __discount_coupon = ('xpath', '//li[@class="second-li"]/span[text()="我的优惠券"]')
    __discount_coupon_text = ('xpath', '//div[@class="coupon-right-top-left"]')

    # 会员中心-我的优惠券跳转
    def my_discount_coupon(self):
        self.click_loc(self.__discount_coupon)
        sleep(3)
        text = self.get_text_loc(self.__discount_coupon_text)
        return text

    __coupon_center_loc = ('xpath', '//div[@class="coupon-right-top-right"]')
    __coupon_center_text_loc = ('xpath', '//div[@class="ph-custom_content"]/div')
    __back_my_discount_coupon = ('xpath', '//div[text()="进入我的优惠券列表"]')

    # 会员中心-我的优惠券列表-领劵中心跳转
    def go_coupon_center(self):
        # 跳转到领劵中心
        self.click_loc(self.__coupon_center_loc)
        sleep(3)
        # 提取领劵中心文本校验
        text1 = self.get_text_loc(self.__coupon_center_text_loc)
        # 返回到我的优惠券列表
        self.click_loc(self.__back_my_discount_coupon)
        # 提取我的优惠券列表文本校验
        text2 = self.get_text_loc(self.__discount_coupon_text)
        return text1, text2

    __enterprise_information_loc = ('xpath', '//li[@class="second-li"]/span[text()="企业信息"]')
    __enterprise_information_text_loc = ('xpath', '//div[@class="invoice-header"]/span[1]')

    # 会员中心-企业信息页面跳转
    def enterprise_information(self):
        # 点击企业信息模块
        self.click_loc(self.__enterprise_information_loc)
        sleep(3)
        # 提取企业信息文本
        text = self.get_text_loc(self.__enterprise_information_text_loc)
        return text

    __shouying_record_loc = ('xpath', '//li[@class="second-li"]/span[text()="首营记录"]')
    __shouying_record_text_loc = ('xpath', '//div[@class="ph-paths"]/span[1]')

    # 会员中心-首营记录跳转
    def shouying_record(self):
        # 点击首营记录
        self.click_loc(self.__shouying_record_loc)
        # 获取首营记录页面文本校验
        text = self.get_text_loc(self.__shouying_record_text_loc)
        return text

    __shouying_record_storename = ('xpath', '//table[@class="el-table__body"]/tbody/tr[1]/td[3]/div')
    __shouying_record_input_box = ('xpath', '//div[@class="query-cont"]/div[1]/input')
    __shouying_record_confirm = ('xpath', '//div[@class="query-cont"]/button[1]')

    # 会员中心-首营记录查询-店铺名称
    def shouying_recored_select_storename(self):
        try:
            store_name1 = self.get_text_loc(self.__shouying_record_storename)
            self.send_keys_loc(self.__shouying_record_input_box, text=store_name1)
            self.click_loc(self.__shouying_record_confirm)
            sleep(3)
            store_name2 = self.get_text_loc(self.__shouying_record_storename)
            return store_name1, store_name2
        except TimeoutException:
            print("没有提取到店铺名称，请检查店铺列表是否有数据")

    __shouying_record_storetype = ('xpath', '//span[@class="el-input__suffix"]/span/i')
    __shouying_record_first_storetype = ('xpath', '//div[@x-placement="bottom-start"]/div[1]/div[1]/ul/li[1]/span')
    __shouying_record_text_storetype = ('xpath', '//table[@class="el-table__body"]/tbody/tr[1]/td[4]/div')
    __shouying_record_reset = ('xpath', '//div[@class="query-cont"]/button[2]')

    # 会员中心-首营记录查询-店铺类型
    def shouying_recored_select_storetype(self):
        try:
            # 点击重置按钮
            self.click_loc(self.__shouying_record_reset)
            sleep(3)
            # 点击店铺类型下拉框
            self.click_loc(self.__shouying_record_storetype)
            # 提取下拉框第一个店铺类型
            storetype1 = self.get_text_loc(self.__shouying_record_first_storetype)
            # 点击第一个店铺类型
            self.click_loc(self.__shouying_record_first_storetype)
            # 点击查询
            self.click_loc(self.__shouying_record_confirm)
            sleep(3)
            # 提取店铺列表第一个店铺类型
            storetype2 = self.get_text_loc(self.__shouying_record_text_storetype)
            return storetype1, storetype2
        except TimeoutException:
            print("没有提取到店铺类型，请检查店铺列表是否有数据")

    __business_management_loc = ('xpath', '//li[@class="second-li"]/span[text()="企业管理"]')
    __business_management_text_loc = ('xpath', '//div[@class="box-title"]/div[1]/span[1]')

    # 会员中心-企业管理页面跳转
    def business_management(self):
        # 点击企业管理
        self.click_loc(self.__business_management_loc)
        sleep(2)
        # 获取企业管理页面文本
        text = self.get_text_loc(self.__business_management_text_loc)
        return text

    __qualification_management_loc = ('xpath', '//li[@class="second-li"]/span[text()="资质管理"]')
    __qualification_management_text_loc = ('xpath', '//div[@class="qualification-title"]/span')

    # 会员中心-资质管理页面跳转
    def qualification_management(self):
        # 点击资质管理
        self.click_loc(self.__qualification_management_loc)
        sleep(2)
        # 获取资质管理页面文本
        text = self.get_text_loc(self.__qualification_management_text_loc)
        return text

    __employee_account_management_loc = ('xpath', '//li[@class="second-li"]/span[text()="员工账号管理"]')
    __employee_account_management_text_loc = ('xpath', '//div[@class="box-title"]/div[1]/span[1]')

    # 会员中心-员工账号管理页面跳转
    def employee_account_management(self):
        # 点击员工账号管理
        self.click_loc(self.__employee_account_management_loc)
        sleep(2)
        # 获取员工账号管理页面文本
        text = self.get_text_loc(self.__employee_account_management_text_loc)
        return text

    __invoice_management_loc = ('xpath', '//li[@class="second-li"]/span[text()="发票管理"]')
    __invoice_management_text_loc = ('xpath', '//div[@class="invoice-header"]/span[1]')

    # 会员中心-发票管理页面跳转
    def invoice_management(self):
        # 点击发票管理
        self.click_loc(self.__invoice_management_loc)
        sleep(2)
        # 获取发票管理页面文本
        text = self.get_text_loc(self.__invoice_management_text_loc)
        return text

    __pay_query_loc = ('xpath', '//li[@class="second-li"]/span[text()="支付查询"]')
    __pay_query_text_loc = ('xpath', '//div[@class="ph-paths"]/span[1]')

    # 个人中心-支付查询页面跳转
    def pay_query(self):
        self.js_focus_element_loc(self.__pay_query_loc)
        # 点击支付查询
        self.click_loc(self.__pay_query_loc)
        sleep(2)
        # 获取支付查询页面文本
        text = self.get_text_loc(self.__pay_query_text_loc)
        return text

    # 个人中心-支付查询页面-支付方式查询
    def pay_query_payment(self):
        try:
            __pay_query_payment_loc = ('xpath', '//div[@class="query-cont"]/div[2]/div[1]/span/span/i')
            __pay_query_payment_text_loc = ('xpath', '//tr[@class="el-table__row"][1]/td[5]/div')
            __pay_query_payment_affirm = ('xpath', '//div[@class="query-cont"]/button')
            # 提取列表第一个支付方式
            text1 = self.get_text_loc(__pay_query_payment_text_loc)
            __pay_query_payment_select_loc = ('xpath', '//div[@class="el-scrollbar"]/div[1]/ul/li/span[text()="{0}"]'.format(text1))
            # 选择支付方式下拉框
            self.click_loc(__pay_query_payment_loc)
            sleep(2)
            # 选择支付方式
            self.click_loc(__pay_query_payment_select_loc)
            sleep(2)
            # 点击查询按钮
            self.click_loc(__pay_query_payment_affirm)
            sleep(3)
            # 提取查询结果
            text2 = self.get_text_loc(__pay_query_payment_text_loc)
            return text1, text2
        except TimeoutException:
            Log().info(u"查看列表是否有数据，没有数据请先添加数据")

    __my_wallet_loc = ('xpath', '//li[@class="second-li"]/span[text()="我的钱包"]')
    __my_wallet_text_loc = ('xpath', '//div[@class="count-title"]')

    # 个人中心-我的钱包页面跳转
    def my_wallet(self):
        self.js_focus_element_loc(self.__my_wallet_loc)
        # 点击我的钱包
        self.click_loc(self.__my_wallet_loc)
        sleep(2)
        # 获取我的钱包页面文本
        text = self.get_text_loc(self.__my_wallet_text_loc)
        return text

    __my_jzb_loc = ('xpath', '//li[@class="second-li"]/span[text()="我的九州币"]')
    __my_jzb_text_loc = ('xpath', '//div[@class="top-box-left"]/div[@class="title"]')

    # 个人中心-我的九州币页面跳转
    def my_jzb(self):
        self.js_focus_element_loc(self.__my_jzb_loc)
        # 点击我的九州币
        self.click_loc(self.__my_jzb_loc)
        sleep(2)
        # 获取我的九州币页面文本
        text = self.get_text_loc(self.__my_jzb_text_loc)
        return text

    __account_security_loc = ('xpath', '//li[@class="second-li"]/span[text()="账户安全"]')
    __account_security_text_loc = ('xpath', '//span[@class="account-title"]')

    # 个人中心-账户安全页面跳转
    def account_security(self):
        self.js_focus_element_loc(self.__account_security_loc)
        # 点击账户安全
        self.click_loc(self.__account_security_loc)
        sleep(2)
        # 获取账户安全页面文本
        text = self.get_text_loc(self.__account_security_text_loc)
        return text

    __my_lottery_loc = ('xpath', '//li[@class="second-li"]/span[text()="抽奖"]')
    __my_lottery_text_loc = ('xpath', '//span[@class="myCoupon-title"]')

    # 个人中心-抽奖页面跳转
    def my_lottery(self):
        self.js_focus_element_loc(self.__my_lottery_loc)
        # 点击抽奖
        self.click_loc(self.__my_lottery_loc)
        sleep(2)
        # 获取抽奖页面文本
        text = self.get_text_loc(self.__my_lottery_text_loc)
        return text

    __complaint_and_advice_loc = ('xpath', '//li[@class="second-li"]/span[text()="投诉建议"]')
    __complaint_and_advice_text_loc = ('xpath', '//div[@id="tab-first"]')

    # 个人中心-投诉建议跳转
    def complaint_and_advice(self):
        self.js_focus_element_loc(self.__complaint_and_advice_loc)
        # 点击投诉建议
        self.click_loc(self.__complaint_and_advice_loc)
        sleep(2)
        # 获取投诉建议页面文本
        text = self.get_text_loc(self.__complaint_and_advice_text_loc)
        return text

    __help_center_loc = ('xpath', '//li[@class="second-li"]/span[text()="帮助中心"]')
    __help_center_text_loc = ('xpath', '//div[@class="ph-content"]/span')

    # 客户服务-帮助中心跳转
    def help_center(self):
        self.js_focus_element_loc(self.__help_center_loc)
        # 点击帮助中心
        self.click_loc(self.__help_center_loc)
        sleep(2)
        # 获取帮助中心页面文本
        text = self.get_text_loc(self.__help_center_text_loc)
        return text

    __merchant_current_account_loc = ('xpath', '//li[@class="second-li"]/span[text()="客商往来账"]')
    __merchant_current_account_text_loc = ('xpath', '//div[@class="ph-paths"]/span[1]')

    # 客户服务-客商往来账跳转
    def merchant_current_account(self):
        self.js_focus_element_loc(self.__merchant_current_account_loc)
        # 点击客商往来账
        self.click_loc(self.__merchant_current_account_loc)
        sleep(2)
        # 获取客商往来账页面文本
        text = self.get_text_loc(self.__merchant_current_account_text_loc)
        return text

    # 我的关注
    __wdgz_loc = ('xpath', '//*[@id="sideBar"]/ul/li[2]/ul/li[1]/span')

    # 点击我的关注
    def click_wdgz(self):
        try:
            self.js_focus_element_loc(self.__wdgz_loc)
            self.click_loc(self.__wdgz_loc)
        except TimeoutException:
            Log().info(u"未找到我的关注菜单！")

    __wdgz_prodname = ('xpath', '//*[@id="pane-first"]/div/ul/li/ul/li/div/div[2]/div[1]')
    __wdgz_storename = ('xpath', '//*[@id="pane-second"]/div/ul/li/div/div[2]')

    # 我的关注列表商品页面，获取所有商品名称
    def get_wdgz_prodname(self):
        try:
            text = self.get_text_for_elements(self.__wdgz_prodname)
            return text
        except TimeoutException:
            Log().info(u"没有商品请先关注！")

    # 我的关注-取消关注商品
    def deselect_gz_prodname(self, prod_name):
        __deselect_gz_loc = ('xpath', '//div[@class="goods-cont"]//div[contains(text(),"%s")]/../../../div/div[4]/button/span[text()="取消关注"]'% prod_name)
        __deselect_confirm_loc = ('xpath', '//div[@class="el-dialog__footer"]/span/button[2]')
        __confirm_hint_loc = ('xpath', '/html/body/div[@role="alert"]/p')
        self.js_focus_element_loc(__deselect_gz_loc)
        # 点击取消按钮
        self.click_loc(__deselect_gz_loc)
        sleep(1)
        # 点击取消确认
        self.click_loc(__deselect_confirm_loc)
        # 提取取消提示信息
        text = self.get_text_loc(__confirm_hint_loc)
        return text

    __store_name_loc = ('xpath', '//*[@id="tab-second"]')

    # 我的关注列表店铺页面，获取所有店铺名称
    def get_wdgz_storename(self):
        # 点击店铺列表
        self.click_loc(self.__store_name_loc)
        sleep(2)
        try:
            text = self.get_text_for_elements(self.__wdgz_storename)
            return text
        except TimeoutException:
            Log().info(u"没有店铺请先关注！")

    # 我的缺货蓝
    __wdqhl_loc = ('xpath', '//*[@id="qhl_id"]')

    # 点击我的缺货蓝
    def click_wdqhl(self):
        try:
            self.js_focus_element_loc(self.__wdqhl_loc)
            self.click_loc(self.__wdqhl_loc)
        except TimeoutException:
            Log().info(u"未找到我的缺货蓝菜单！")

    # 我的优惠券
    __wdyhq_loc = ('xpath', '//*[@id="coupon_id"]')

    # 点击我的优惠券
    def click_wdyhq(self):
        try:
            self.js_focus_element_loc(self.__wdyhq_loc)
            self.click_loc(self.__wdyhq_loc)
        except TimeoutException:
            Log().info(u"未找到我的优惠券菜单！")

    # 首营纪录

    # 账户管理
    __zhgl_loc = ('xpath', '//a[text()="账户管理"]')

    # 点击账户管理
    def click_zhgl(self):
        try:
            self.js_focus_element_loc(self.__zhgl_loc)
            self.click_loc(self.__zhgl_loc)
        except TimeoutException:
            Log().info(u"未找到账户管理菜单！")

    # 资质管理
    __zzgl_loc = ('xpath', '//*[@id="licence"]')

    # 点击资质管理
    def click_zzgl(self):
        try:
            self.js_focus_element_loc(self.__zzgl_loc)
            self.click_loc(self.__zzgl_loc)
        except TimeoutException:
            Log().info(u"未找到资质管理菜单！")

    # 员工账号管理

    # 发票管理

    # 支付查询
    __zxzfcx_loc = ('xpath', '//*[@id="zxzfcx_id"]')

    # 点击在线支付查询
    def click_zxzfcx(self):
        try:
            self.js_focus_element_loc(self.__zxzfcx_loc)
            self.click_loc(self.__zxzfcx_loc)
        except TimeoutException:
            Log().info(u"未找到在线支付查询菜单！")

    # 我的钱包


    # 我的九州币
    __wdjzb_loc = ('xpath', '//*[@id="jzb_id"]')

    # 点击我的九州币
    def click_wdjzb(self):
        try:
            self.js_focus_element_loc(self.__wdjzb_loc)
            self.click_loc(self.__wdjzb_loc)
        except TimeoutException:
            Log().info(u"未找到我的九州币菜单！")

    # 账户安全
    __zhaq_loc = ('xpath', '//*[@id="accountSecurity_id"]')

    # 点击账户安全
    def click_zhaq(self):
        try:
            self.js_focus_element_loc(self.__zhaq_loc)
            self.click_loc(self.__zhaq_loc)
        except TimeoutException:
            Log().info(u"未找到账户安全菜单！")

    # 抽奖

    # 投诉建议
    __tsjy_loc = ('xpath', '//*[@id="ts_id"]')

    # 点击投诉建议
    def click_tsjy(self):
        try:
            self.js_focus_element_loc(self.__tsjy_loc)
            self.click_loc(self.__tsjy_loc)
        except TimeoutException:
            Log().info(u"未找到投诉建议菜单！")

    # 帮助中心
    __bzzx_loc = ('xpath', '//div//p//a[text()="帮助中心"]')

    # 点击帮助中心
    def click_bzzx(self):
        try:
            self.js_focus_element_loc(self.__bzzx_loc)
            self.click_loc(self.__bzzx_loc)
        except TimeoutException:
            Log().info(u"未找到帮助中心菜单！")

    # 客商往来帐元素
    __kswlzcx_loc = ('xpath','//a[@id="kswlz_id"]')

    def click_kswlacx(self):
        """点击客商往来账"""
        try:
            self.js_focus_element_loc(self.__kswlzcx_loc)
            self.click_loc(self.__kswlzcx_loc)
        except:
            Log().info(u'未找到客商往来帐查询')

    __switch_to_button = ('xpath', '//div[@class="userinfo"]/i')
    __get_enterprise_text = ('xpath', '//div[@class="company-ul yjj-scroll"]/div[2]/span')
    __click_switch_to = ('xpath', '//div[@class="company-ul yjj-scroll"]/div[2]/button/span')

    # 切换企业校验
    def switch_to_enterprise(self):
        # 鼠标移动到单位切换处
        self.move_to_element(self.__switch_to_button)
        sleep(3)
        # 提取切换的单位名称
        name = self.get_text_loc(self.__get_enterprise_text)
        # 点击所选单位切换按钮
        self.click_loc(self.__click_switch_to)
        sleep(3)
        return name

    __click_back_switch_to = ('xpath', '//div[@class="company-ul yjj-scroll"]/div[1]/button/span')

    # 切回原来的企业
    def back_enterprise(self):
        # 鼠标移动到单位切换处
        self.move_to_element(self.__switch_to_button)
        sleep(3)
        # 点击所选单位切换按钮
        self.click_loc(self.__click_back_switch_to)
        sleep(3)

    __member_center_search = ('xpath', '//input[@class="el-input__inner"]')

    # 会员中心-搜索页面搜索校验
    def member_center_search(self, prod_name):
        self.js_focus_element_loc(self.__member_center_search)
        # 输入搜索关键字
        self.send_keys_loc(self.__member_center_search, text=prod_name)
        # 回车
        self.enter_key(self.__member_center_search)
        sleep(3)

    # =============================个人中心-我的订单元素集合=======================================================
    # 订单同步1.0-开票单号FDG开头（一组元素6个）
    __listbox_order_number_list = ('xpath', '//*[@class="order_list_box"]//*[@class="fs12 cor999 u_detl_orderNo"]')
    # 订单同步2.0-订单号DM开头（一组元素5个）
    __listbox_order2_number_list = ('xpath', '//span[@class="fs12 cor666"]/a[contains(@href, "orderNewDetail.htm")]')
    # 商品总金额（一组元素6个）
    __listbox_amount_payable_list = ('xpath', '//*[@class="order_list_box"]//*[@class="fs16 cor333 mr20"]')
    # 商品数量（一组元素6个）
    __listbox_product_number_list = ('xpath', '//*[@class="order_list_box"]//*[@class="fs14 cor333"]')
    # 下单时间（一组元素6个）
    __listbox_order_time_list = ('xpath', '//*[@class="order_list_box"]//*[@class="fs12 cor999 mr20"]')

    # 点击详情页入口单个元素，并返回webdriver
    def click_list_product_details_pages(self, local_detail_page):
        self.js_focus_element_ele(local_detail_page)
        self.click_element(local_detail_page)
        # 等待第二个窗口打开
        self.wait_until_windows_open()
        # 切换窗口
        self.switch_window()
        # 等待窗口title变成
        WebDriverWait(self.driver, timeout=10).until(EC.title_is('订单详情页'))
        from pages.orderDetailsPage import OrderDetails
        return OrderDetails(self.driver)

    # 获取会员中心页面我的订单中6个订单的数据（包括订单号list、应付金额list、商品数量list、下单时间list）
    def get_member_center_order_number_list(self):
        """会员中心我的订单模块的6个订单号list"""
        # 获取订单数据来源，返回1代表订单同步1.0，返回2代表订单同步2.0
        member_center_order_number_list = []
        try:
            member_center_order_number_list = self.get_text_for_elements(self.__listbox_order2_number_list)
        except TimeoutException:
            Log().info("最近60天没有下订单，无法订单详情比较")
        return member_center_order_number_list

    def get_member_center_amount_payable_list(self):
        """会员中心我的订单模块的6个订单应付金额list"""
        member_center_amount_payable_list = self.get_text_for_elements(self.__listbox_amount_payable_list)
        # print(member_center_amount_payable_list)
        return member_center_amount_payable_list

    def get_member_center_product_number_list(self):
        """会员中心我的订单模块的6个订单商品数量list"""
        member_center_aproduct_number_list = self.get_text_for_elements(self.__listbox_product_number_list)
        # print(member_center_aproduct_number_list)
        return member_center_aproduct_number_list

    def get_member_center_order_time_list(self):
        """会员中心我的订单模块的6个订单下单时间list"""
        member_center_aorder_time_list = self.get_text_for_elements(self.__listbox_order_time_list)
        # print(member_center_aorder_time_list)
        return member_center_aorder_time_list

    # 再次购买按钮元素
    __buy_again_button = ('xpath', '//*[contains(text(),"再次购买")][1]')

    # 点击再次购买按钮
    def click_buy_again_button(self):
        try:
            self.click_loc(self.__buy_again_button)
        except TimeoutException:
            Log().info("没有找到再次购买按钮，请确保有60天内有订单数据")

    # 查看详情页入口-商品图片（一组元素5个）
    __listbox_product_details_pages_list = ('xpath', '//div[@class="order_list_box"]//table//img')

    # 点击会员中心页面—【我的订单】—【商品图片】按钮，依次获取开票单号、商品总金额、商品数量、下单金额
    def get_order_detail_message_list(self):
        ele_order_details = self.find_elements(self.__listbox_product_details_pages_list)
        # print(ele_order_details)
        # 订单详情页订单号列表集
        order_details_order_number_list = []
        # 订单详情页应付金额列表集
        order_details_amount_payable_list = []
        # 订单详情页商品数量列表集
        order_details_product_number_list = []
        # 订单详情页下单时间列表集
        order_details_order_time_list = []
        for i in ele_order_details:
            order_detail_page = self.click_list_product_details_pages(i)
            time.sleep(3)
            # 获取订单详情页的订单号，并加入列表中
            order_num = order_detail_page.get_order_number()
            order_details_order_number_list.append(order_num)
            # print(order_details_order_number_list)
            # 获取订单详情页的商品实付金额，并加入列表中
            amount_pay = order_detail_page.get_amount_sum()
            order_details_amount_payable_list.append(amount_pay)
            # print(order_details_amount_payable_list)
            # order_detail_page.click_buy_again()
            # 获取订单详情页的商品数量，并加入列表中
            product_num = "共" + str(order_detail_page.get_all_prod_number()) + "种"
            order_details_product_number_list.append(product_num)
            # print(order_details_product_number_list)
            # 获取订单详情页的下单时间，并加入列表中
            order_time = order_detail_page.get_order_time()
            order_details_order_time_list.append(order_time)
            # print(order_details_order_time_list)
            order_detail_page.close()
            # 切换窗口
            self.switch_window()
        return order_details_order_number_list, order_details_amount_payable_list, order_details_product_number_list, order_details_order_time_list

    # ============================================页面等待=======================================================

    def wait_member_refresh(self, timeout=10):
        """
        等待页面某元素过期，即等带页面刷新,此页面用搜索按钮判断
        这里会员中心的搜索按钮若过期，代表页面已经刷新（已经打开别的页面）
        """
        try:
            self.wait_element_staleness(self.__search_button_loc, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    def wait_title_change(self, title, timeout=60):
        """等待新打开直到窗口title出现"""
        try:
            self.is_title_contains(title, timeout)
        except TimeoutException:
            pass














