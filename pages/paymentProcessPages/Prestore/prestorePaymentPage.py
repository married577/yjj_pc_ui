"""预存的支付页面"""
from pages.paymentProcessPages.selectOnlinePaymentMode import PaymentMode
from random import random
from selenium.common.exceptions import TimeoutException
from common.log import Log
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class PrestorePaymentPage(PaymentMode):

    """ =======================================预存专题页=============================================== """
    # 【立即预存】按钮
    __immediate_preStore = ('xpath', '//a[@href="/payment/cfcaPay/payPrestore.htm"]')

    # 点击【立即预存】按钮，进入预存选择支付方式页面
    def click_immediate_preStore(self):
        self.click_loc(self.__immediate_preStore)
        Log().info(u"点击【立即预存】按钮")
        self.wait_until_windows_open()
        # 切换窗口
        self.switch_window()
        # 等待窗口title变成
        WebDriverWait(self.driver, timeout=30).until(EC.title_contains('预存'))

    # '去预存'按钮
    __goto_prestore = ('xpath', '//div[@class="u_recharge_amount"]/input')
    # 预存金额
    __prestore_1_loc = ('xpath', '//div[@class="m_chose_box clearfix"]//p[text()="1元"]')

    def select_amount_and_payment_go_to_pay(self, amount, payment_mode):
        """
        选择预存金额，以及支付方式，前往支付，直至支付成功
        :param amount: 预存金额
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
        """
        # 选择充值金额
        self.select_amount(amount)
        # 选择充值方式
        return self.select_payment_mode_go_to_pay(payment_mode)

    def select_payment_mode_go_to_pay(self, payment_mode):
        """
        选择支付方式，并前往支付，一直支付成功
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 若选择支付宝/微信支付，则返回支付宝/微信页面，否则返回相应的支付成功页面
        """
        return self.select_payment_mode(payment_mode=payment_mode, loc=self.__goto_prestore, entry='预存')

    def select_amount(self, amount):
        """
        选择预存金额，若amount的值，在页面有选项，则选中相应的充值金额，否则，随机选择一个充值金额。
        :param amount:
        :return:
        """
        if amount == '1':
            # 点击‘1元’
            self.click_loc(self.__prestore_1_loc)
        else:
            # 随机选取一个卡片
            self.getPrice_clickCard()

    def compare_sumPrice_prestore(self):
        """
        比较去预存'总价'=预存卡片的金额
        :return:
        """
        a = float(self.get_price_of_prestore())
        b = float(self.get_price_sum())
        if(a == b):
            return True
        else:
            return False

    # 选中的预存卡片的金额
    __price_of_prestore = ('xpath', '//div[@class="m_chose_box clearfix"]/'
                                    'div[@class="u_cont_box combox current"]/p[@class="u_price"]')

    # 选中的预存卡片的奖励金额
    __reward_amount = ('xpath', '//div[@class="m_chose_box clearfix"]/'
                                'div[@class="u_cont_box combox current"]/p[@class="col-yellow"]')

    # 获取选中的预存卡片的金额，0.02元 、2元
    def get_price_of_prestore(self):
        price = self.get_text_loc(self.__price_of_prestore)
        Log().info('预存卡片的金额: %s' % price[:-1])
        return float(price[:-1])

    # 获取选中的预存卡片的奖励金额，例如送奖励金0.00元
    def get_reward_amount(self):
        amount = self.get_text_loc(self.__reward_amount)
        Log().info('预存卡片的奖励金额: %s' % amount[4:8])
        return float(amount[4:8])

    # 所有预存卡片的定位
    __card_list = ('xpath', '//div[@class="m_chose_box clearfix"]/div[contains(@class,"u_cont_box combox")]')

    def __get_card_list(self):
        """
        获取预存卡片列表对象
        :return: 预存卡片列表对象的list
        """
        card_list = []
        try:
            card_list = self.find_elements(self.__card_list)
        except TimeoutException:
            print("预存卡片无数据！")
        return card_list

    def __get_card_num(self):
        """
        获取预存卡片的数量
        :return: 预存卡片的数量
        """
        return len(self.__get_card_list())

    def get_random_num(self):
        """
        获取获取从1至卡片数量的随机整数
        :return: 1至卡片数量的随机整数
        """
        num = random.randrange(1, self.__get_card_num())
        return num

    def getPrice_clickCard(self):
        """
        随机点击一个预存卡片
        :return:
        """

        n = self.get_random_num()
        # 第n个卡片
        __card_n_click = ('xpath', "//div[@class='m_chose_box clearfix']/"
                                   "div[contains(@class,'u_cont_box combox')][" + str(n) + "]")

        # 点击第n个卡片
        self.click_loc(__card_n_click)

    # 去预存'总价'
    __sum_price = ('xpath', '//span[@class="u_recharge_sum"]/span[@id="price_sum"]')

    # 获取去预存'总价' ,例如￥0.02
    def get_price_sum(self):
        amount = self.get_text_loc(self.__sum_price)
        Log().info('去预存总价金额: %s' % amount[1:5])
        return amount[1:5]

