# coding=utf-8
"""我的购物车页面"""
from common.log import Log
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from pages.orderConfirmationPage import OrderConfirmation
from common.commonMethod import CommonMethod
from pages.topCommonMenu.baseMenus import BaseMenus
from operator import itemgetter
from decimal import Decimal
from random import randint


class MyCart(BaseMenus):

    # =======================================打开购物车页面=============================
    # 购物车链接
    __cart_page_url = CommonMethod().get_endpoint('cartpage')

    def open_cart_page(self):
        """通过url直接打开购物车页面"""
        # 打开主页
        self.open(self.__cart_page_url, '我的购物车')
        # 等待页面打开
        self.wait_title_change('我的购物车')
        sleep(2)
        self.refresh()

    # =======================================购物车商品信息===============================
    # 所有商品列表 -- 商品编码元素的定位
    __prodno_list_loc = ('xpath', '//input[@id="prodNo"]')
    # 所有失效商品列表（不确定是否包含失效精品组合商品）
    __invalid_list_loc = (
    'xpath', '//div[@class="column column3"]/div/ul/li[@class="f_cb my_cart_li m_abate"]/div[1]/div[1]/a[2]')
    # 购物车数量 -- 购物车(n)
    __total_number_loc = ('xpath', "//span[@class='a-color']")
    # 弹出消息
    __message_loc = ('xpath', '//div[@type="dialog"]/div[@class="layui-layer-content"]')
    # 所有商品名称
    __all_goods_names_loc = ('xpath', '//*[@id="commodity-details"]/div[1]/div/div[2]/div/div/div/ul/li/div/div[1]/div[3]/span[1]')

    # 提取购物车所有商品名称
    def all_goods_names(self):
        text = self.get_text_for_elements(self.__all_goods_names_loc)
        return text

    __yjj_icon_loc = ('xpath', '//div[@class="HeaderMember"]/div/img')

    # 点击药九九图标，返回到首页
    def yjj_icon(self):
        self.click_loc(self.__yjj_icon_loc)

    def count_of_prods(self):
        """
        购物车商品总数（包含有效和失效商品）
        :return: 购物车商品总数
        """
        total_number = int(self.get_text_loc(self.__total_number_loc))
        return total_number

    def display_invalid_prods(self):
        """
        判断失效商品是否显示
        :return: 显示：true，不显示:false
        """
        sleep(2)
        try:
            self.is_visibility(self.__invalid_list_loc, 10)
            result = True
        except TimeoutException:
            result = False
        return result

    def count_of_invalid_prods(self):
        """
        购物车无效商品的总数
        :return: 购物车无效商品的总数
        """
        result = self.display_invalid_prods()
        if result:
            count = len(self.find_elements(self.__invalid_list_loc))
        else:
            count = 0
        return count

    def is_in_cart(self, prodno):
        """
        根据商品编码来判断该商品是否在购物车列表里面
        :param prodno: 商品编码
        :return: 商品在购物车列表里面，返回True,否则返回False
        """
        result = False
        if self.count_of_prods() > 0:
            prop_list = self.get_attribute_for_elements(self.__prodno_list_loc, 'value')
            for prod_no in prop_list:
                if prodno == prod_no:
                    result = True
                    break
        return result

    def is_able_add_to_cart(self):
        """
        判断商品是否可以加购物车
        :return: 能加入购物车，返回true，不能加购物车返回false
        """
        try:
            element = self.find_element_presence(self.__message_loc, 5)
            text = self.get_text_ele(element)
            print(text)
            # 等待消息消失
            self.wait_element_staleness_ele(element)
            if '请谨慎购买' in text:
                return True
            else:
                return False
        except TimeoutException:
            return True

    # =======================================购物车商品操作===============================
    # 全选按钮 -- 商品列表下面
    __select_all = ('xpath', '//*[@id="__layout"]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/span/label/span[1]/span')
    # 清空失效商品--最下面
    __clean_invalid_prods = ('xpath', '//a[@id="clear_abate"]')
    # 点击最下面的清空失效按钮弹框中的'清空失效商品按钮'
    __clean_invalid_confirm = ('xpath', '//a[@onclick="clearInvalidMer();"]')
    # 删除选中商品
    __delete_all_selected_loc = ('xpath', "//a[text()='删除选中商品']")
    # 弹框上的确定按钮
    __confirm_button_window_loc = ('xpath', "//a[text()='确定']")
    # 商品的关注
    __follow_loc = ('xpath', '//a[@class="fragment3 ftchange add_attention_check"]')

    # 购物车全选、取消按钮
    def check_all_prod(self):
        # 点击全选按钮，全部选中
        self.click_loc(self.__select_all)
        sleep(5)
        # 再次点击全选按钮，取消全部选中
        self.click_loc(self.__select_all)
        sleep(4)

    # 勾选指定商品
    def check_appoint_prod(self, prod_name):
        __appoint_prod_loc = ('xpath', '//*[text()="%s"]/../../div[1]/label/span/span' % prod_name)
        self.click_loc(__appoint_prod_loc)
        sleep(2)

    def goods_follow(self):
        """进行商品关注"""
        self.js_focus_element_loc(self.__follow_loc, bottom=False)
        self.click_loc(self.__follow_loc,10)

    # 指定商品添加关注
    def assign_goods_attention(self, prod_name):
        __goods_attention_loc = ('xpath', '//*[text()="%s"]/../../..//*[text()="添加关注"]' % prod_name)
        __goods_attention_hint = ('xpath', '/html/body/div[@role="alert"]/p')
        # 点击添加关注
        self.click_loc(__goods_attention_loc)
        # 获取关注成功提示
        text = self.get_text_loc(__goods_attention_hint)
        return text

    member_center_loc = ('xpath', '//div[@class="right"]/span[text()="会员中心"]')

    # 进入会员中心
    def go_to_membercenter(self):
        # 点击会员中心
        self.click_loc(self.member_center_loc)
        # 切换窗口
        self.switch_window()
        sleep(3)

    def clean_prod_in_cart(self):
        """
        清空购物车的商品，包含有效 和 无效
        :return:
        """
        # 购物车数量
        total_number = int(self.get_text_loc(self.__total_number_loc))
        # 失效商品数量
        invalid_prods = self.count_of_invalid_prods()
        # 如果购物车数量 不等于 失效商品数量，则 清空购物车有效商品
        if total_number != invalid_prods:
            if total_number != 0:
                try:
                    # select 复选框是否被选中
                    result = self.is_selected(self.__select_all, 5)
                except TimeoutException:
                    result = False
                # 如果全选框被选中，直接点击删除选中商品
                if result:
                    self.click_loc(self.__delete_all_selected_loc)
                else:
                    # 选中全选框
                    self.click_element(self.find_element_based_on_element(self.find_element(self.__select_all),
                                                                          ('xpath', './following-sibling::span')))
                    # 点击删除选中商品
                    self.click_loc(self.__delete_all_selected_loc)
                # 点击弹框上的确定按钮
                self.click_loc(self.__confirm_button_window_loc)
        # 如果有失效商品，则 清空购物车失效商品
        elif invalid_prods != 0:
            # 点击 底部的清除失效商品
            self.click_loc(self.__clean_invalid_prods)
            # 点击 弹框上的"清空失效商品"按钮
            self.click_loc(self.__clean_invalid_confirm)

    def select_all_prods_or_not(self, select_all=True):
        """
        选中全部商品，或不选中任意商品
        :param select_all: True表示选中所有商品，False表示不选中任意商品
        :return:
        """
        # 购物车数量
        total_number = int(self.get_text_loc(self.__total_number_loc))
        if total_number != 0:
            try:
                # select 复选框是否被选中
                result = self.is_selected(self.__select_all, 5)
            except TimeoutException:
                result = False
            # 全选复选框元素
            select_all_checkbox_ele = self.find_element_based_on_element(self.find_element(self.__select_all),
                                                                         ('xpath', './following-sibling::span'))
            if result:
                if select_all is False:
                    self.js_focus_element_ele(select_all_checkbox_ele)
                    # 选中全选框1次
                    self.click_element(select_all_checkbox_ele)

            else:
                if select_all:
                    # 选中全选框
                    self.click_element(select_all_checkbox_ele)
                else:
                    self.js_focus_element_ele(select_all_checkbox_ele)
                    # 选中全选框两次
                    self.click_element(select_all_checkbox_ele)
                    self.click_element(select_all_checkbox_ele)

    def select_prod(self, prod_no):
        """
        根据商品编码勾选商品
        :param prod_no:
        :return:
        """
        # 该商品的复选框input元素 -- 可以用来检查是否被勾选
        check_box_input_loc = ('xpath', '//*[@id="prodNo" and @value="%s"]/'
                                        'following-sibling::div[1]//input[@type="checkbox"]' % prod_no)
        check_box_input_ele = self.find_element(check_box_input_loc)
        # 该商品的复选框可勾选的元素 -- 可用来勾选和不勾选
        check_box_ele = self.find_element_based_on_element(check_box_input_ele, ('xpath', './following-sibling::span'))
        # 1. 判断该商品是否被选中
        try:
            # 该商品的复选框是否被选中
            result = self.is_selected(check_box_input_loc, 2)
        except TimeoutException:
            result = False
        if result is False:
            self.js_focus_element_ele(check_box_ele,bottom=False)
            self.click_element(check_box_ele)
        Log().info('勾选商品%s' % prod_no)

    def select_prods(self, *prod_no):
        """
        根据商品编码勾选购物车中的一个或多个商品（只有给定的商品会被选中，其他商品都不被选中）
        :param prod_list:商品编码，例如'KZQ033637X','KZQ033637X1','KZQ0331637X'
        :return:
        """
        # 1. 不勾选全部商品
        self.select_all_prods_or_not(select_all=False)
        # 2. 勾选列表中的商品
        for prod in prod_no:
            self.select_prod(prod)

    # 编辑商品数量
    def modify_prod_num(self, num, prod_no):
        __prod_quantity_loc = ('xpath', '//*[text()="%s"]/../../../div[3]/div/div[1]/div/div/div/input' % prod_no)
        self.js_focus_element_loc(__prod_quantity_loc)
        sleep(2)
        self.send_keys_loc(__prod_quantity_loc, num)
        __prod_unit_loc = ('xpath', '//*[text()="%s"]/../../../div[3]/div/div[3]' % prod_no)
        # self.click_loc(__prod_unit_loc)
        self.enter_key(__prod_quantity_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    def modify_prod_num2(self, num, prod_no):
        __prod_quantity_loc = ('xpath', '//input[@id="merchandiseNumber%s"]' % prod_no)
        self.send_keys_loc2(__prod_quantity_loc, num)
        __prod_unit_loc = ('xpath', '//span[@id="packageunit%s"]' % prod_no)
        self.click_loc(__prod_unit_loc)
        Log().info(u"编辑商品数量，输入： %s" % num)

    # 获取已输入的商品数量
    def get_prod_num(self, prod_no):
        try:
            __prod_quantity_loc = ('xpath', '//input[@id="merchandiseNumber%s"]' % prod_no)
            return Decimal(self.get_attribute_loc(__prod_quantity_loc, 'value'))
        except TimeoutException:
            return 0

    # 增商品
    def plus_prod(self, prod_no):
        __plus_loc = ('xpath', '//a[contains(@onclick,"%s" ) and @class="u_goods_increa"]' % prod_no)
        self.click_loc(__plus_loc)

    # 减商品
    def minus_prod(self, prod_no):
        __minus_loc = ('xpath', '//a[contains(@onclick,"%s" ) and @class="u_goods_reduce"]' % prod_no)
        self.click_loc(__minus_loc)

    # 获取商品价格
    def price_prod(self, prod_no):
        __price_loc = ('xpath', '//*[@id="showPriceText%s"]' % prod_no)
        price = Decimal(self.get_text_content_loc(__price_loc))
        return price

    # 获取商品金额
    def amount_prod(self, prod_no):
        __amount_loc = ('xpath', '//input[@value="%s"]/following-sibling::div[4]/span' % prod_no)
        amount = Decimal(self.get_text_content_loc(__amount_loc))
        return amount

    # 获取商品单位
    def unit_prod(self, prod_no):
        __unit_loc = ('xpath', '//*[@id="packageunit%s"]' % prod_no)
        unit = self.get_text_content_loc(__unit_loc)
        return unit

    # 因起订数量和最小购买单位，导致商品失效的图标是否显示
    def is_expired_icon_display(self, prod_no):
        __icon_loc = ('xpath', "//input[@value='%s' and @id='prodNo']/following-sibling::div[1]"
                               "//i[@class='verifyTan-icon' and text()='!']" % prod_no)
        result = self.is_display(__icon_loc)
        return result

    # 因起订数量和最小购买单位，请重新确认购买数量的消息是否存在
    def is_num_conform_msg_display(self, prod_no):
        __msg_loc = ('xpath', "//span[@id='step%s' and text()='请重新确认购买数量']" % prod_no)
        try:
            result = self.is_display(__msg_loc)
        except TimeoutException:
            result = False
        return result

    # 商品前面的复选框是否显示
    def is_checkbox_icon_display(self, prod_no):
        __icon_loc = ('xpath',
                      "//input[@value='%s' and @id='prodNo']/following-sibling::div[1]//label" % prod_no)
        # result = self.is_display(__icon_loc)
        try:
            self.is_visibility(__icon_loc)
            result = True
        except:
            result = False
        return result

    # 删除指定商品
    def remove_item(self, prod_name):
        __item_loc = ('xpath', '//*[text()="%s"]/../../..//*[text()="删除"]' % prod_name)
        __confirm_remove_loc = ('xpath', '//*[@id="commodity-details"]/div[1]/div[1]/div[4]/div/div/div[3]/span/button[2]/span[contains(text(),"确 定")]')
        __hint_remove_loc = ('xpath', '/html/body/div[@role="alert"]/p')
        # 滑动到元素位置
        self.js_focus_element_loc(__item_loc)
        sleep(2)
        # 点击删除指定商品
        # self.click_loc(__item_loc)
        element = self.find_element(__item_loc)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(2)
        # 点击确认删除
        # self.click_loc(__confirm_remove_loc)
        element = self.find_element(__confirm_remove_loc)
        self.driver.execute_script("arguments[0].click();", element)
        # 提取删除成功提示消息
        text = self.get_text_loc(__hint_remove_loc)
        return text

    # 去逛逛
    __go_to_search_loc = ('xpath', '//a[text()="去逛逛>"]')
    # 去加购
    __go_to_add_loc = ('xpath', '//*[@id="rebaseDiv"]/a[text()="去加购>"]')

    def click_go_to_search(self):
        """
        点击去逛逛
        :return:
        """
        self.click_loc(self.__go_to_search_loc)
        try:
            # 等待搜索结果页面打开
            self.wait_title_change('商品搜索列表')
            from pages.prodSearchResultPage import SearchResult
            return SearchResult(self.driver)
        except:
            return False

    def click_go_to_add(self):
        """
        点击去加购
        :return:
        """
        self.click_loc(self.__go_to_add_loc)


    # =======================================购物车去结算 ===============================
    # 提交订单按钮定位
    __submit_loc = ('xpath', '//div[@class="summary-box"]/button')
    # 商品总金额
    __total_price_loc = ('xpath', '//*[@id="totalPrice"]')
    # 立减金额
    __cut_price_loc = ('xpath', '//*[@id="cutPrice"]')

    def submit_order_button(self):
        """
        点击提交订单按钮，因校验页面未跳转到下一页
        :return:
        """
        self.js_focus_element_loc(self.__submit_loc)
        self.click_loc(self.__submit_loc)
        Log().info(u"点击提交订单")

    __exemption_remind_loc = ('xpath', '//div[@class="el-dialog__body"]/div[text()="提交订单"]')

    # 去结算包邮提醒
    def submit_exemption_remind(self):
        try:
            # 点击包邮提醒，提交订单按钮
            self.click_loc(self.__exemption_remind_loc)
            sleep(3)
        except TimeoutException:
            pass

    def submit_order(self):
        """
        点击提交订单，跳转到确认订单信息页面
        :return:
        """
        self.js_focus_element_loc(self.__submit_loc)
        self.click_loc(self.__submit_loc)
        Log().info(u"点击提交订单")
        # 等待页面跳转到订单确认页面
        self.wait_title_change('确认订单信息', timeout=30)
        Log().info(u'跳转到确认订单信息页面')
        return OrderConfirmation(self.driver)

    def get_order_amount(self):
        """
        获取订单金额，即商品总金额 - 立减金额
        :return: 订单金额
        """
        # 商品总金额
        total_amount = self.get_text_loc(self.__total_price_loc)
        # 立减金额
        cut_amount = self.get_text_loc(self.__cut_price_loc)
        return Decimal(total_amount) - Decimal(cut_amount)

    # ===========================购物车等待============================================

    def wait_prod_in_cart(self, prodno, timeout=10):
        """由于加购物车之后，商品进入购物车有延迟，故需等待商品在购物车页面显示，以及提交订单按钮可见"""
        try:
            WebDriverWait(self.driver, timeout, 0.5).until(ProdIsInList(prodno))
            WebDriverWait(self.driver, timeout, 0.5).until(EC.element_to_be_clickable(self.__submit_loc))
        except(TimeoutException, NoSuchElementException):
            pass


class ProdIsInList(object):
    """根据prodno来判断该商品是否在商品列表里面"""

    def __init__(self, prodno):
        self.prod = prodno

    def __call__(self, driver):
        cart = MyCart(driver)
        if cart.is_in_cart(self.prod):
            return True
        else:
            return False
















