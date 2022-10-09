"""在线支付 -- 选择支付方法页面"""
from common.log import Log
from pages.paymentProcessPages.selectOnlinePaymentMode import PaymentMode


class OnlinePaymentMethod(PaymentMode):

    # 付款号即订单编号
    __payment_code_loc = ('xpath', "//div[@class='m_pay_info_l']/h3[@class='u_order_info']")
    # 应付金额
    __amount_payable_loc = ('xpath', '//*[@class="u_order_no"]')
    # # 订单详情
    # __order_detail_loc = ('xpath', "//input[@value='订单详情']")
    # 订单金额
    __order_amount_loc = ('xpath', "//p[contains(text(),'订单金额')]/span")
    # 在线支付金额
    __online_pay_amount_loc = ('xpath', '//*[@id="resultPayPrice"]')
    # 在线支付优惠金额
    __online_pay_discount_amount_loc = ('xpath', '//*[@id="yhPrice"]')
    # 前往支付按钮
    __go_to_pay_loc = ('xpath', "//input[@value='前往支付']")

    def select_payment_mode_go_to_pay(self, payment_mode):
        """
        选择支付方式，并前往支付，直至支付成功
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
        """
        return self.select_payment_mode(payment_mode=payment_mode, loc=self.__go_to_pay_loc, entry='下单')

    def get_order_code(self):
        """
        获取订单编号
        :return: 订单编号
        """
        text = self.get_text_loc(self.__payment_code_loc)
        order_code =text[-18:]
        return order_code

    def get_amount_payable(self):
        """
        获取应付金额
        :return:应付金额 -- float类型
        """
        return float(self.get_text_loc(self.__amount_payable_loc))

    def get_order_amount(self):
        """
        获取订单金额
        :return: 订单金额 -- float类型
        """
        text = self.get_text_content_loc(self.__order_amount_loc)
        order_amount = text[:-1]
        return float(order_amount)  # by 胡耀康_2019.2.14

    def get_online_payment_amount(self):
        """
        获取在线支付金额
        :return: 在线支付金额 -- float类型
        """
        text = self.get_text_loc(self.__online_pay_amount_loc)
        payment_amount = text[:-1]
        return float(payment_amount)  # by 胡耀康_2019.2.14

    def get_online_payment_discount(self):
        """
        获取在线支付优惠金额
        :return: 在线支付优惠金额 -- float类型
        """
        discount = self.get_text_content_loc(self.__online_pay_discount_amount_loc)
        discount = (0 if discount == '' else discount)
        return float(discount)


