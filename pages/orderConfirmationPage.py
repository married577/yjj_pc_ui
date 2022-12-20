"""确认订单信息页面"""
from selenium.common.exceptions import TimeoutException
from common.log import Log
from pages.topCommonMenu.baseMenus import BaseMenus
from time import sleep


class OrderConfirmation(BaseMenus):

    # 线下结算
    __under_line_settlement_loc = ('xpath', '//label[@id="xxjsbt"]')
    # 在线支付
    __online_settlement_loc = ('xpath', '//*[@id="zxzfbt"]')
    # 提交订单
    __submit_button_loc = ('xpath', '//div/button[text()="提交订单"]')
    # 二维码
    __erweima_img_loc = ('xpath', '//div[@class="u_code_img"][1]')
    # 选择账期支付
    __payment_days_loc = ('xpath', '//div[@class="box payment"]/label[2]')
    # 提交订单
    __submit_order_loc = ('xpath', '//*[text()="提交订单"]')

    # 选择账期支付方式
    def select_payment_days(self):
        try:
            # self.js_focus_element_loc(self.__payment_days_loc)
            # self.click_loc(self.__payment_days_loc)
            element = self.find_element(self.__payment_days_loc)
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print("未配置账期支付，请先配置账期支付")

    # 点击提交订单按钮
    def click_submit_order(self):
        try:
            self.click_loc(self.__submit_order_loc)
        except TimeoutException:
            print("没有定位到提交订单按钮")

    __pay_success_hint = ('xpath', '//div[@class="backTit_content"]/div')
    __pay_way_loc = ('xpath', '//span[contains(text(),"支付方式")]/following-sibling::*')

    # 支付成功和支付方式提取
    def get_pay_way(self):
        try:
            text1 = self.get_text_loc(self.__pay_success_hint)
            text2 = self.get_text_loc(self.__pay_way_loc)
            return text1, text2
        except TimeoutException:
            print("没有定位到支付成功元素，可能是支付失败了")

    # 选中线上支付（不使用余额），并提交订单，返回应付金额
    def submit_order(self):
        # 在线支付
        self.click_loc(self.__online_settlement_loc)
        Log().info(u'点击线上支付')
        # 提交订单
        self.js_focus_element_loc(self.__submit_button_loc)
        self.wait_element_clickable(self.__submit_button_loc, 10)
        self.click_by_mouse(self.__submit_button_loc)
        Log().info(u'点击提交订单')

    __extract_title_loc = ('xpath', '//div[@class="content"]/span[@class="title"]')

    # 提取结算页面title
    def extract_title(self):
        text = self.get_text_loc(self.__extract_title_loc)
        return text

    __order_number_loc = ('xpath', '//span[contains(text(),"订单编号")]/following-sibling::*/i')

    # 提取订单编号
    def get_order_number(self):
        text = self.get_text_loc(self.__order_number_loc)
        return text

    __look_order_loc = ('xpath', '//*[text()="查看订单"]')

    # 点击查看订单-计入我的订单列表
    def click_look_order(self):
        try:
            self.click_loc(self.__look_order_loc)
        except TimeoutException:
            print('没有查找到元素，请检查定位元素是否正确')

    __all_prod_name = ('xpath', '//*[@id="__layout"]/div/div/div[3]/div[2]/div/div/div/ul/li/div[2]/div/div[1]/span[1]/span[1]')

    # 获取页面所有商品名称
    def get_all_prod_name(self):
        text = self.get_text_for_elements(self.__all_prod_name)
        return text

    # 获取结算页面，指定商品的数量
    def get_prod_amount(self, prod_name):
        __prod_amount_loc = ('xpath', '//*[text()="%s"]/../../../div[3]/div/span' % prod_name)
        try:
            text = self.get_text_loc(__prod_amount_loc)
            return text
        except TimeoutException:
            print("结算页面没有要结算商品:%s" % prod_name)


    # 选择线下结算,并提交订单
    def submit_order_offline(self):
        """
        选择线下结算，并提交订单
        :return:
        """
        # 选择线下结算
        self.wait_element_clickable(self.__under_line_settlement_loc, 5)
        self.click_loc(self.__under_line_settlement_loc)
        Log().info(u'点击线下结算')
        # 点击提交订单
        self.js_focus_element_loc(self.__submit_button_loc)# 该方法：聚焦元素，将滚动条滚到显示指定的元素，经常无法点击提交订单按钮，换成下面的-滚动到底部
        # self.js_scroll_end()
        self.wait_element_clickable(self.__submit_button_loc, 10)
        self.move_to_element(self.__submit_button_loc)
        sleep(3)
        self.click_by_mouse(self.__submit_button_loc)
        Log().info(u'点击提交订单')
        # 等待页面跳转到订单完成页面
        self.wait_url_contains('/member/order/successPage.htm', timeout=120)
        Log().info(u'跳转到订单提交完成页面')
        from pages.paymentProcessPages.placeOrder.offlineOrderSubmitSuccessPage import OfflineOrderSuccessPage
        return OfflineOrderSuccessPage(self.driver)

    # 使用余额的radio button -- 有余额的情况
    __remaining_balance_loc = ('xpath', '//*[@id="balanceImg"]')

    def is_balance_selected(self):
        """余额支付是否被选中"""
        try:
            src = self.get_attribute_loc(self.__remaining_balance_loc, 'src')
            result = ('unselected' in src)
            if result:
                return False
            else:
                return True
        except TimeoutException:
            return False

    def select_balance(self):
        """选中余额"""
        if self.is_balance_selected() is False:
            self.js_focus_element_loc(self.__remaining_balance_loc, bottom=False)
            self.click_loc(self.__remaining_balance_loc)
            Log().info("余额充足，当前已勾选余额支付")

    def unselect_balance(self):
        """不选中余额"""
        if self.is_balance_selected():
            self.js_focus_element_loc(self.__remaining_balance_loc, bottom=False)
            self.click_loc(self.__remaining_balance_loc)
            Log().info("去掉使用余额")

    # 选中线上支付（不使用余额），并提交订单，返回应付金额
    def submit_order_online_returnmoney(self):
        # 在线支付
        self.click_loc(self.__online_settlement_loc)
        Log().info(u'点击线上支付')
        self.unselect_balance()
        # 获取应付余额
        returnmoney = float(self.get_yf_price())
        # 提交订单
        self.js_focus_element_loc(self.__submit_button_loc, bottom=False)# 该方法：聚焦元素，将滚动条滚到显示指定的元素，经常无法点击提交订单按钮，换成下面的-滚动到底部
        # self.js_scroll_end()
        self.wait_element_clickable(self.__submit_button_loc, 10)
        sleep(5)
        self.click_by_mouse(self.__submit_button_loc)
        Log().info(u'点击提交订单')
        # 等待页面跳转到选择支付方法页面
        self.wait_title_change('选择支付方法', timeout=180)
        Log().info(u'跳转到选择支付方法页面')
        return returnmoney

    # 选中线上支付（不使用余额），并提交订单
    def submit_order_online_without_balance(self):
        # 在线支付
        self.click_loc(self.__online_settlement_loc)
        Log().info(u'点击线上支付')
        # 不使用余额
        self.unselect_balance()
        # 提交订单
        self.js_focus_element_loc(self.__submit_button_loc, bottom=False) #该方法：聚焦元素，将滚动条滚到显示指定的元素，经常无法点击提交订单按钮，换成下面的-滚动到底部
        # self.js_scroll_end()
        self.wait_element_clickable(self.__submit_button_loc, 30)
        sleep(5)
        self.click_by_mouse(self.__submit_button_loc)
        Log().info(u'点击提交订单')
        # 等待页面跳转到选择支付方法页面
        self.wait_title_change('选择支付方法', timeout=120)
        Log().info(u'跳转到选择支付方法页面')
        from pages.paymentProcessPages.placeOrder.onlinePaymentPage import OnlinePaymentMethod
        return OnlinePaymentMethod(self.driver)

    # 选中线上支付，并选择使用余额(余额充足)，并提交订单
    def submit_order_online_with_balance(self):
        """
        选中线上支付，并选择使用余额，并提交订单
        :return:
        """
        # 在线支付
        self.click_loc(self.__online_settlement_loc)
        Log().info(u'点击线上支付')
        # 选择余额
        self.select_balance()
        # 应付金额
        yf_amount = self.get_yf_price()
        # 点击提交订单
        self.js_focus_element_loc(self.__submit_button_loc, bottom=False)#该方法：聚焦元素，将滚动条滚到显示指定的元素，经常无法点击提交订单按钮，换成下面的-滚动到底部
        # self.js_scroll_end()
        self.wait_element_clickable(self.__submit_button_loc, 10)
        self.click_by_mouse(self.__submit_button_loc)
        Log().info(u'点击提交订单')
        # 如果以应付金额大于0，则跳转到选择支付方式页面，否则应该直接订单提交成功
        if yf_amount == 0:
            # 等待页面跳转到支付成功页面
            self.wait_title_change('订单支付成功', timeout=120)
            Log().info(u'跳转到订单支付成功页面')
            from pages.paymentProcessPages.placeOrder.onlineOrderSubmitSuccessPage import OnlineOrderSuccessPage
            return OnlineOrderSuccessPage(self.driver)
        else:
            # 等待页面跳转到选择支付方法页面
            self.wait_title_change('选择支付方法', timeout=120)
            Log().info(u'跳转到选择支付方法页面')
            from pages.paymentProcessPages.placeOrder.onlinePaymentPage import OnlinePaymentMethod
            return OnlinePaymentMethod(self.driver)

    # ==================================================金额部分===================================== #

    # 商品总金额
    __origional_price_loc = ('xpath', "//div[@class='u_accounts_css']/p[contains(text(), '商品总金额')]/span/i")
    # 立减
    __lj_price_loc = ('xpath', "//div[@class='u_accounts_css']/p[contains(text(), '立减')]/span")
    # 优惠券
    __coupon_price_loc = ('xpath', "//div[@class='u_accounts_css']/p[contains(text(), '优惠券')]/span/i")
    # 应付金额
    __payable_price_loc = ('xpath', "//div[@class='u_accounts_css']/p[contains(text(), '应付金额')]/span/i")
    # 余额支付
    __ye_price_loc = ('xpath', "//div[@class='u_accounts_css']//i[@class='balancePayPrice']")
    # 应付余额
    __total_price_loc = ('xpath', "//div[@class='u_accounts_css']//i[@class='yfPrice']")

    # 获取商品总金额
    def get_origional_price(self):
        self.js_focus_element_loc(self.__erweima_img_loc)
        return float(self.get_text_loc(self.__origional_price_loc, timeout=30))

    # 获取立减金额
    def get_lj_price(self):
        self.js_focus_element_loc(self.__erweima_img_loc)
        return float(self.get_text_loc(self.__lj_price_loc).split('￥')[1])

    # 获取优惠券抵用金额
    def get_coupon_price(self):
        # self.js_scroll_end()
        self.js_focus_element_loc(self.__erweima_img_loc)
        return float(self.get_text_loc(self.__coupon_price_loc))

    # 获取应付余额
    def get_yf_price(self):
        # self.js_scroll_end()
        self.js_focus_element_loc(self.__erweima_img_loc)
        return float(self.get_text_loc(self.__total_price_loc))

    # 获取余额支付
    def get_balance_pay_price(self):
        # self.js_scroll_end()
        self.js_focus_element_loc(self.__erweima_img_loc)
        return float(self.get_text_loc(self.__ye_price_loc))

    # 获取所有需要校验的金额将入列表
    def get_order_config_prices_all_list(self):
        # 获取商品总金额
        amount_sum = self.get_origional_price()
        # 获取立减金额
        amount_lijian = self.get_lj_price()
        # 获取优惠券金额
        amount_coupon = self.get_coupon_price()
        # 获取应付金额
        amount_payable = self.get_yf_price()
        # 返回金额列表
        all_amount_list = [amount_sum, amount_lijian, amount_coupon, amount_payable]
        return all_amount_list

    # 计算应付余额
    def calculate_yf_price(self):
        """
        :return: 商品总金额 - 立减 - 优惠券  - 余额支付
        """
        # 商品总金额
        a = self.get_origional_price()
        # 立减
        b = self.get_lj_price()
        # 优惠券
        c = self.get_coupon_price()
        # 余额支付
        e = self.get_balance_pay_price()
        yf = a - b - c - e
        return yf

    # =========================================元素等待========================================== #

    def wait_element_clickable(self, locator, timeout=10):
        """
        等待元素可点击
        """
        # print("++++", datetime.datetime.now())
        try:
            self.is_clickable(locator, timeout)
        except TimeoutException:
            pass

    def wait_page_load(self, timeout=10):
        """ 等待页面加载"""
        try:
            self.is_visibility(self.__under_line_settlement_loc,timeout)
        except TimeoutException:
            pass

    # 温馨提示：//div[contains(text(),"订单的商品信息发生变化，请返回购物车刷新后重新提交！")]
    __wenxin_message = ('xpath', '//div[contains(text(),"订单的商品信息发生变化，请返回购物车刷新后重新提交！")]')

    def is_toast_exist(self):
        try:
            self.is_visibility(self.__wenxin_message, 40)
            result = True
            msg = ''
        except TimeoutException:
            result = False
            msg = '确认订单页没有提示"订单的商品信息发生变化，请返回购物车刷新后重新提交！"'
        return result, msg
