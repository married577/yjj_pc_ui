# coding=utf-8
"""领券中心页面"""
from common.basePage import Action
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


class CouponCenter(Action):

    # =====================================================================================================
    # =====================================================================================================
    # 领券中心
    # =====================================================================================================
    # =====================================================================================================

    # 领券中心可领取的优惠券数量链接
    __able_take_coupon_number_loc = ('xpath', "//div[@class='u_coup_num']")

    def amount_in_able_take_list(self, coupon_id):
        """
        根据优惠券的id获取优惠券在领券中心的可领取数量
        :param coupon_id: 优惠券的id
        :return: 优惠券的可领取数量
        @Author :
        """
        # 未领取的优惠券列表
        try:
            coupon_list = self.find_elements(self.__able_take_coupon_number_loc, timeout=5)
        except TimeoutException:
            coupon_list = []
        # 若未领取的优惠券列表为空，返回0，否则根据优惠券名称判断，该优惠券是否在列表里面
        if len(coupon_list) == 0:
            return 0
        else:
            # 目标优惠券是否在优惠券列表中
            is_exist = False
            # 可领取的数量
            times = 0
            for ele in coupon_list:
                # 包含优惠券id的优惠券元素定位 -- 相对于优惠券数量的定位
                coupon_id_loc = ('xpath', './preceding-sibling::div[@class="m_coup_bd"]/h5')
                # 优惠券元素
                coupon_ele = self.find_element_based_on_element(ele, coupon_id_loc)
                # 优惠券id
                text = self.get_attribute_ele(coupon_ele, 'onclick').split('(')[1]
                if coupon_id == int(text):
                    is_exist = True
                    # 表示还有多少张已领取，多少张未领取的文本
                    value = self.get_text_content_ele(ele)
                    if len(value) == 0:
                        # 如果未显示可领取的数量，表示只有一张可领取
                        times = 1
                    else:
                        times = int(re.findall("可领([0-9]+)张", value)[0])
            # 如果目标优惠券不在可领取优惠券列表中，返回0
            if is_exist is False:
                    return 0
            else:
                return times

    # 领券中心的未领取的优惠券的立即领取按钮
    __take_button_loc = ('xpath', '//a[text()="立即领取"]')

    # 根据优惠券的id领取优惠券
    def take_coupon(self, coupon_id):
        # 用result来标志是否找到了优惠券且可以领取
        result = False
        # 未领取的优惠券的立即领取按钮
        try:
            take_button_list = self.find_elements(self.__take_button_loc, timeout=5)
        except TimeoutException:
            take_button_list = []
        # 若无立即领取按钮，返回打印；否则，根据优惠券名称，领取优惠券
        if len(take_button_list) == 0:
            print("无优惠券可领取")
        else:
            for button in take_button_list:
                # 优惠券的定位
                coupon_name_loc = ('xpath', './../preceding-sibling::div[1]/h5')
                # 优惠券元素
                coupon_id_ele = self.find_element_based_on_element(button, coupon_name_loc)
                # 优惠券id
                text = self.get_attribute_ele(coupon_id_ele, 'onclick').split('(')[1]
                if coupon_id == int(text):
                    # 找到优惠券，点击立即领取按钮
                    self.js_focus_element_ele(button)
                    self.click_element(button)
                    result = True
                    break
            if result is False:
                print("未找到优惠券：%s" % coupon_id)

    # 领取优惠券后，弹出窗口的关闭和立即使用链接
    __close_window_loc = ('xpath', "//a[text()='关闭']")
    __go_to_use_window_loc = ('xpath', "//a[text()='立即使用']")

    # 点击领取优惠券后，弹出框上点击去使用，或关闭
    def selection_on_window(self, go_to_use=True):
        # 若go_to_use值为true，点击弹出框的去使用按钮，否则点击关闭按钮
        if go_to_use:
            self.click_loc(self.__go_to_use_window_loc)
            # 等待第二个窗口打开
            self.wait_until_windows_open()
            # 切换窗口
            self.switch_window()
            # 等待窗口title变成
            WebDriverWait(self.driver, timeout=5).until(EC.title_contains('商品搜索列表'))
            from pages.prodSearchResultPage import SearchResult
            return SearchResult(self.driver)
        else:
            self.click_loc(self.__close_window_loc)

    # =====================================================================================================
    # =====================================================================================================
    # 我的优惠券和领券中心切换
    # =====================================================================================================
    # =====================================================================================================

    # 我的优惠券
    __my_coupon_link_loc = ('xpath', "//a[text()='我的优惠券']")

    # 切换到我的优惠券页面
    def switch_to_my_coupon(self):
        # 点击我的优惠券链接
        self.click_loc(self.__my_coupon_link_loc)
        # 等待页面title变化
        self.wait_title_change('我的优惠券')

    # 领券中心
    __coupon_center_link_loc = ('xpath', "//a[text()='我的优惠券']")

    # 切换到领券中心页面
    def switch_to_coupon_center(self):
        # 点击领券中心链接
        self.click_loc(self.__coupon_center_link_loc)
        # 等待页面title变化
        self.wait_title_change('领券中心')

    # =====================================================================================================
    # =====================================================================================================
    # 我的优惠券
    # =====================================================================================================
    # =====================================================================================================

    # 可使用的优惠券链接
    __active_coupon_link_loc = ('xpath', "//div[contains(@class, 'active')]//h5[@class='u_coup_type']")

    # 根据优惠券的ID判断优惠券是否在我的优惠券的可使用列表,返回张数
    def is_in_able_use_list(self, coupon_id):
        # 可使用列表
        try:
            coupon_list = self.find_elements(self.__active_coupon_link_loc, timeout=5)
        except TimeoutException:
            coupon_list = []
        # 若可使用优惠券列表为空，返回0，否则根据优惠券id判断，该优惠券是否在列表里面
        if len(coupon_list) == 0:
            return 0
        else:
            coupon_id_list = []
            for ele in coupon_list:
                text = self.get_attribute_ele(ele, 'onclick')
                couponid = int(re.findall("\(([0-9]+)\)", text)[0])
                coupon_id_list.append(couponid)
            if coupon_id in coupon_id_list:
                times = coupon_id_list.count(coupon_id)
                return times
            else:
                return 0

    # 根据优惠券的ID判断一组优惠券是否在我的优惠券的可使用列表
    def is_coupons_in_useable_list(self, *coupon_ids):
        """
        根据优惠券的ID判断一组优惠券是否在我的优惠券的可使用列表
        :param coupon_ids:
        :return:
        """
        result = True
        msg = ''
        # 可使用列表
        try:
            coupon_list = self.find_elements(self.__active_coupon_link_loc, timeout=5)
        except TimeoutException:
            coupon_list = []
        # 若可使用优惠券列表为空，返回0，否则根据优惠券id判断，该优惠券是否在列表里面
        if len(coupon_list) == 0:
            result = False
            msg += "可使用优惠券列表为空"
        else:
            # 获取优惠券列表
            coupon_id_list = []
            for ele in coupon_list:
                text = self.get_attribute_ele(ele, 'onclick')
                couponid = int(re.findall("\(([0-9]+)\)", text)[0])
                coupon_id_list.append(couponid)
            # 判断优惠券
            for coupon_id in coupon_ids:
                if coupon_id not in coupon_id_list:
                    result = False
                    msg += "优惠券：%s不在可使用优惠券列表中；" % coupon_id

        return result, msg




    # 去使用链接
    __go_to_use_my_coupon_loc = ('xpath', "//div[contains(@class, 'z_coup_taked')]//a[text()='去使用']")

    # 根据优惠券的id点击去使用
    def go_to_use(self, coupon_id_expected):
        # 用result来标记是否找到了优惠券
        result = False
        # 所有去使用链接
        try:
            links = self.find_elements(self.__go_to_use_my_coupon_loc)
        except TimeoutException:
            links = []
        # 如果linke为空，则无优惠券可去使用，否则根据优惠券名称来点击去使用
        if len(links) == 0:
            print("无优惠券去使用")
        else:
            for link in links:
                # # 优惠券名称的定位
                # coupon_name_loc = ('xpath', './../preceding-sibling::div[1]/h5')
                # # 优惠券名称元素
                # coupon_name_ele = self.find_element_based_on_element(link, coupon_name_loc)
                # # 优惠券名称
                # coupon_name = self.get_text_ele(coupon_name_ele).split(']')[1]
                # 优惠券id
                text = self.get_attribute_ele(link, 'onclick')
                coupon_id = int(re.findall("\(([0-9]+)\)", text)[0])
                if coupon_id_expected == coupon_id:
                    # 找到优惠券，点击去使用链接
                    self.js_focus_element_ele(link)
                    self.click_element(link)
                    # 等待第二个窗口打开
                    self.wait_until_windows_open()
                    # 切换窗口
                    self.switch_window()
                    # 等待窗口title变成
                    WebDriverWait(self.driver, timeout=5).until(EC.title_contains('商品搜索列表'))
                    from pages.prodSearchResultPage import SearchResult
                    return SearchResult(self.driver)
            if result is False:
                print("未找到优惠券：%s" % coupon_id_expected)





