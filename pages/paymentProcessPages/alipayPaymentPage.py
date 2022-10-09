"""支付宝支付页面"""
from common.basePage import Action
from common.log import Log


class AlipayPayment(Action):

    """金额"""
    # 右上角的金额
    __price_of_SignSpecialOffer_topRight = ('xpath', '//span[@class="payAmount-area"]/strong')
    # 二维码上面的支付金额
    __price_of_SignSpecialOffer_middle = ('xpath', '//div[@class="ft-center qrcode-header-money"]')
    # 支付宝付款页面订单详情的按钮
    __order_detail_loc = ('xpath', '//a[@class="order-ext-trigger"]')
    # 详情下拉框中的金额
    __price_of_order_detail = ('xpath', '//li[@class="order-item"]//tr[4]/td')
    # 交易金额
    __deal_amount_loc = ('xpath', '//span[@id="amountZ"]')
    # 收款商家
    __collection_merchant_loc = ('xpath', "//*[@id='AliPayLayer']//dd[contains(text(), '收款商家')]")
    # 流水号
    __serial_number_loc = ('xpath', '//dd[@id="trxZ"]')
    # 弹框关闭按钮
    __close_button_loc = ('xpath', "//*[@id='AliPayLayer']//i[contains(@class, 'fa-close')]")

    def get_deal_amount(self):
        """
        获取交易金额
        :return: 交易金额 -- float
        """
        deal_amount = self.get_text_loc(self.__deal_amount_loc)
        return float(deal_amount)

    def get_collection_merchant(self):
        """
        获取收款商家
        :return:收款商家
        """
        text = self.get_text_loc(self.__collection_merchant_loc)
        print(text)
        merchant = text.split('：')[1]
        return merchant

    def get_serial_number(self):
        """
        获取流水号
        :return: 流水号
        """
        text = self.get_text_loc(self.__serial_number_loc)
        serial_number = text.split(':')[1]
        return serial_number

    def close_weixin_payment_window(self, page_object):
        """
        关闭微信/支付宝支付弹框
        :param page_object: 微信支付窗口所在的支付页面对象
        :return:
        """
        self.click_loc(self.__close_button_loc)
        return page_object

    def compare_serial_number(self, page_object):
        """
        比较同一个订单，重复打开微信支付方式，流水号应该不一致
        :param page_object: 当前的选择支付页面对象
        :return: 两次流水号一致，返回False， 否则返回True
        """
        # 获取当前微信窗口的流水号
        serial_number1 = self.get_serial_number()
        # 关闭当前微信支付窗口
        page = self.close_weixin_payment_window(page_object)
        # 再次选择微信，并去支付/充值
        weixin_window = page.select_payment_mode_go_to_pay('支付宝')
        serial_number2 = weixin_window.get_serial_number()
        result = True if serial_number1 != serial_number2 else False
        return result

    def get_price_of_alipay(self):
        """
        获取支付宝付款页面：右上角、二维码上面、详情下拉框中的金额
        :return: 右上角、二维码上面、详情下拉框中的金额
        """
        # 获取右上角的金额
        topRight_price = self.__get_price_of_top_right()
        # 获取二维码上面的支付金额
        middle_price = self.__get_price_of_middle()
        # 获取详情下拉框中的金额
        order_detail_price = self.__get_price_order_detail()
        return topRight_price, middle_price, order_detail_price

    # 获取右上角的金额
    def __get_price_of_top_right(self):
        topRight_price = self.get_text_loc(self.__price_of_SignSpecialOffer_topRight)
        Log().info('获取右上角的金额: %s' % topRight_price)
        return float(topRight_price)

    # 获取二维码上面的支付金额
    def __get_price_of_middle(self):
        middle_price = self.get_text_loc(self.__price_of_SignSpecialOffer_middle)
        Log().info('获取二维码上面的支付金额: %s' % middle_price)
        return float(middle_price)

    # 获取详情下拉框中的金额
    def __get_price_order_detail(self):
        self.click_loc(self.__order_detail_loc)
        Log().info('点击订单详情按钮')
        order_detail_price = self.get_text_loc(self.__price_of_order_detail)
        Log().info('获取详情下拉框中的金额: %s' % order_detail_price)
        return float(order_detail_price)



