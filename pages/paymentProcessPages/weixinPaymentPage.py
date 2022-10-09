"""微信支付弹出框"""
from common.basePage import Action
from common.log import Log


class WeixinPayment(Action):

    # 微信支付弹框标题
    __title_loc = ('xpath', '//*[@id="WXPayLayer"]//dt')
    # 收款商家
    __collection_merchant_loc = ('xpath', "//*[@id='WXPayLayer']//dd[contains(text(), '收款商家')]")
    # 流水号
    __serial_number_loc = ('xpath', '//dd[@id="trxW"]')
    # 交易金额
    __deal_amount_loc = ('xpath', '//span[@id="amountW"]')
    # 弹框关闭按钮
    __close_button_loc = ('xpath', "//*[@id='WXPayLayer']//i[contains(@class, 'fa-close')]")

    def get_deal_amount(self):
        """
        获取交易金额
        :return: 交易金额 -- float
        """
        deal_amount = self.get_text_loc(self.__deal_amount_loc)
        return float(deal_amount)

    def get_serial_number(self):
        """
        获取流水号
        :return: 流水号
        """
        text = self.get_text_loc(self.__serial_number_loc)
        serial_number = text.split(':')[1]
        return serial_number

    def get_collection_merchant(self):
        """
        获取收款商家
        :return:收款商家
        """
        text = self.get_text_loc(self.__collection_merchant_loc)
        print(text)
        merchant = text.split('：')[1]
        return merchant

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
        weixin_window = page.select_payment_mode_go_to_pay('微信')
        serial_number2 = weixin_window.get_serial_number()
        result = True if serial_number1 != serial_number2 else False
        return result



