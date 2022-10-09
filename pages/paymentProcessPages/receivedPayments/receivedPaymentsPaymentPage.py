# coding=utf-8
"""回款（充值）的支付页面"""
from pages.paymentProcessPages.selectOnlinePaymentMode import PaymentMode
from common.updateDataFromDB import OperationInDB
import random


class ReceivedPaymentsPayment(PaymentMode):

    db_operation = OperationInDB()
    # 充值金额
    __amount_100_loc = ('xpath', "//p[text()='100元']/..")
    __amount_500_loc = ('xpath', "//p[text()='500元']/..")
    __amount_1000_loc = ('xpath', "//p[text()='1,000元']/..")
    __amount_5000_loc = ('xpath', "//p[text()='5,000元']/..")
    __amount_10000_loc = ('xpath', "//p[text()='10,000元']/..")
    __amount_other_loc = ('xpath', "//p[text()='其它金额']/..")
    # 第6个卡片的定位
    __amount_6_loc = ('xpath', '//div[contains(@class,"u_cont_box")][6]')
    # 请输入充值金额
    __amount_input_loc = ('xpath', '//*[@id="in_price"]')
    # 确认按钮
    __confirm_amount_loc = ('xpath', "//button[@class='pay_button']")
    # 去充值按钮
    __qcz_loc = ('xpath', "//input[@value='去充值']")

    def select_amount_and_payment_go_to_pay(self, amount, payment_mode):
        """
        选择充值金额，选择支付方式，并去充值，直至充值成功
        :param amount: 充值金额
        :param payment_mode: 支付方式：'支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 返回充值成功页面
        """
        # 选择充值金额
        # self.select_amount(amount)
        expect_price = self.click_moneyback_card(amount)
        # 选择充值方式
        return self.select_payment_mode_go_to_pay(payment_mode), expect_price

    def select_amount(self, amount):
        """选择充值金额"""
        if amount == 100:
            # 点击100元
            self.click_loc(self.__amount_100_loc)
        elif amount == 500:
            # 点击500元
            self.click_loc(self.__amount_500_loc)
        elif amount == 1000:
            # 点击1000元
            self.click_loc(self.__amount_1000_loc)
        elif amount == 5000:
            # 点击5000元
            self.click_loc(self.__amount_5000_loc)
        elif amount == 10000:
            # 点击10000元
            self.click_loc(self.__amount_10000_loc)
        else:
            # 点击其他金额
            self.click_loc(self.__amount_other_loc)
            # 输入金额
            self.send_keys_loc2(self.__amount_input_loc, amount)
            # 点击确定按钮
            self.click_loc(self.__confirm_amount_loc)

    def get_clickCard(self):
        """
        随机点击第1到第6个预存卡片
        :return:
        """
        n = random.randrange(1, 6)
        # 第n个卡片
        __card_n_click = ('xpath', "//div[contains(@class,'u_cont_box')][" + str(n) + "]")
        # 获取第n个卡片的金额
        __card_n_price = ('xpath', "//div[contains(@class,'u_cont_box')][" + str(n) + "]/p[@class='u_price']")
        price = str(self.get_text_loc(__card_n_price))[:-1]
        # 如果金额为4位数，需要去掉中间的'，'，例如 '10,000' 变成 '10000'
        price = price.replace(',', '')
        print("第：%s 个卡片的金额为：%s " % (n, price))
        # 点击第n个卡片
        self.click_loc(__card_n_click)
        return float(price)

    def select_payment_mode_go_to_pay(self, payment_mode):
        """
        选择支付方式，并前往支付，直至支付成功
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
        """
        return self.select_payment_mode(payment_mode=payment_mode, loc=self.__qcz_loc, entry='回款')

    def click_moneyback_card(self, amount):
        """
        当期配置了充值返利活动，随机点击1-6个
        :param amount:
        :return:
        """
        count = self.db_operation.get_moneyback()
        if count >= 1:
            # 随机点击1-6个卡片
            price = self.get_clickCard()
            expect_price = price
        else:
            # 手动输入卡片的金额，例如100000
            self.click_loc(self.__amount_6_loc)
            # 输入金额
            self.send_keys_loc2(self.__amount_input_loc, amount)
            # 点击确定按钮
            self.click_loc(self.__confirm_amount_loc)
            expect_price = amount
        return expect_price











