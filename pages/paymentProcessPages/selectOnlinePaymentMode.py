"""选择在线支付方法 -- 支付宝，微信，个人网银，企业网银"""
from common.basePage import Action
from common.log import Log


class PaymentMode(Action):

    # 支付宝的单选框
    __alipay_loc = ('xpath', "//span[text()='支付宝']/preceding-sibling::*[contains(@class, 'radio')]")
    # 微信的单选框
    __weixin_loc = ('xpath', "//span[text()='微信']/preceding-sibling::*[contains(@class, 'radio')]")
    # 个人网银的单选框
    __personal_pay_loc = ('xpath', "//span[text()='个人网银']/preceding-sibling::*[contains(@class, 'radio')]")
    # 企业网银的单选框
    __enterprise_pay_loc = ('xpath', "//span[text()='企业网银']/preceding-sibling::*[contains(@class, 'radio')]")
    # 微信支付弹层
    __weixin_payment_window_loc = ('xpath', '//*[@id="WXPayLayer"]')
    # 支付宝支付弹层
    __zhifubao_payment_window_loc = ('xpath', '//*[@id="AliPayLayer"]')

    def select_payment_mode(self, entry, payment_mode, loc):
        """
        选择支付方式
        :param entry: 支付页面的入口，即签约特供，预存，回款，订单支付四种
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :param loc: 各个支付页面，选择了支付方法后，下一步操作的方法名称，即点击‘前往支付’，‘去支付’，‘去预存’等按钮
        :return:
        """
        from pages.paymentProcessPages.zhongJingPaymentPage import ZhongJingPayment
        payment = ZhongJingPayment(self.driver)
        entries = {'签约特供': payment.sign_bank_payment,
                   '预存': payment.prestore_bank_payment,
                   '回款': payment.received_payments_bank_payment,
                   '下单': payment.online_order_payment}
        # 选中支付方式
        if payment_mode == '支付宝':
            # 选中支付方式
            self.select_alipay()
            # 点击前往支付/去支付/去预存
            self.click_confirm_payment_button(loc)
            # 等待页面标题改变
            # self.wait_title_change('支付宝 - 网上支付', 20)
            # 等待微信支付弹框显示
            self.is_visibility(self.__zhifubao_payment_window_loc, 30)
            from pages.paymentProcessPages.alipayPaymentPage import AlipayPayment
            return AlipayPayment(self.driver)

        elif payment_mode == '微信':
            # 选中支付方式
            self.select_weixin()
            # 点击前往支付/去支付/去预存
            self.click_confirm_payment_button(loc)
            # 等待微信支付弹框显示
            self.is_visibility(self.__weixin_payment_window_loc, 30)
            from pages.paymentProcessPages.weixinPaymentPage import WeixinPayment
            return WeixinPayment(self.driver)

        elif payment_mode == '个人网银':
            # 选中支付方式
            self.select_personal_pay()
            # 点击前往支付/去支付/去预存
            self.click_confirm_payment_button(loc)
            # 等待页面标题改变
            self.wait_title_change('中金支付', 30)
            # 中金支付对应场景的个人网银支付流程
            page = entries[entry]()
            return page
        else:
            # 选中支付方式
            self.select_enterprise_pay()
            # 点击前往支付/去支付/去预存
            self.click_confirm_payment_button(loc)
            # 等待页面标题改变
            self.wait_title_change('中金支付', 80)
            # 中金支付对应场景的企业网银支付流程
            page = entries[entry](personal=False)
            return page

    def select_alipay(self):
        """选择支付宝支付"""
        # 判断是否已经被选中
        is_selected = 'u_radio_checked' in self.get_attribute_loc(self.__alipay_loc, 'class')
        # 若未选中，则点击选中
        if is_selected is False:
            self.click_loc(self.__alipay_loc)
        Log().info('选中支付方式 -- 支付宝')

    def select_weixin(self):
        """选择微信支付"""
        # 判断是否已经被选中
        is_selected = 'u_radio_checked' in self.get_attribute_loc(self.__weixin_loc, 'class')
        self.js_focus_element_loc(self.__weixin_loc, 'class')
        # 若未选中，则点击选中
        if is_selected is False:
            self.click_loc(self.__weixin_loc)
        Log().info('选中支付方式 -- 微信')

    def select_personal_pay(self):
        """选择个人网银"""
        # 判断是否已经被选中
        is_selected = 'u_radio_checked' in self.get_attribute_loc(self.__personal_pay_loc, 'class')
        # 若未选中，则点击选中
        if is_selected is False:
            self.js_focus_element_loc(self.__personal_pay_loc, bottom=False)
            self.click_loc(self.__personal_pay_loc)
        Log().info('选中支付方式 -- 个人网银')

    def select_enterprise_pay(self):
        """选择企业网银"""
        # 判断是否已经被选中
        is_selected = 'u_radio_checked' in self.get_attribute_loc(self.__enterprise_pay_loc, 'class')
        # 若未选中，则点击选中
        if is_selected is False:
            self.js_focus_element_loc(self.__enterprise_pay_loc, bottom=False)
            self.click_loc(self.__enterprise_pay_loc)
        Log().info('选中支付方式 -- 企业网银')

    def click_confirm_payment_button(self, loc):
        """
        ‘前往支付’，‘去支付’，‘去预存’等按钮
        :param loc: ‘前往支付’，‘去支付’，‘去预存’等按钮的定位
        :return:
        """
        self.js_focus_element_loc(loc, bottom=False)
        self.click_loc(loc)
