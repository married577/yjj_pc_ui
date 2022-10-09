# coding=utf-8
"""首页"""
from common.basePage import Action
from common.log import Log
from time import sleep


class ZhongJingPayment(Action):

    # 登录按钮
    __login_loc = ('xpath', '//*[@id="leftBtn"]/input')
    # 确认支付
    __confirm_order_loc = ('xpath', '//*[@id="cfgBtn"]/input')
    # 登录网银复核
    __double_confirm_loc = ('xpath', '//*[@id="noticeBtn"]/input')
    # 返回商品取货
    __back_to_get = ('xpath', '//*[@id="noticeBtn"]/input')

    def sign_bank_payment(self, personal=True):
        """
        签约特供通过个人网银或企业网银支付成功
        :param personal: 默认值为True，使用个人网银支付，否则使用企业网银支付
        :return: 签约特供开通成功页面
        """
        if personal:
            self.__personal_pay()
            try:
                self.continue_enterprise_pay()
            except:
                pass
        else:
            self.__enterprise_pay()
        self.wait_title_change('权限开通结果页(成功) - 开通签约特惠权限', timeout=180)
        Log().info(u'跳转到权限开通结果页(成功) - 开通签约特惠权限成功页面')
        from pages.paymentProcessPages.signSpecialOffer.signSpecialOfferSuccessPage import SignSpecialOfferSuccess
        return SignSpecialOfferSuccess(self.driver)

    def prestore_bank_payment(self, personal=True):
        """
        预存通过个人网银或企业网银支付成功
        :param personal: 默认值为True，使用个人网银支付，否则使用企业网银支付
        :return: 预存支付成功页面
        """
        if personal:
            self.__personal_pay()
            try:
                self.continue_enterprise_pay()
            except:
                pass
        else:
            self.__enterprise_pay()
            self.continue_enterprise_pay()
        self.wait_title_change('预存成功 - 订单支付', timeout=180)
        Log().info(u'跳转到预存支付成功页面')
        from pages.paymentProcessPages.Prestore.payPrestorePageSuccess import PrestoreSuccess
        return PrestoreSuccess(self.driver)

    def received_payments_bank_payment(self, personal=True):
        """
        回款即充值，通过个人网银或企业网银支付成功
        :param personal: 默认值为True，使用个人网银支付，否则使用企业网银支付
        :return: 回款支付成功页面
        """
        if personal:
            self.__personal_pay()
            try:
                self.continue_enterprise_pay()
            except:
                pass
        else:
            self.__enterprise_pay()
            self.continue_enterprise_pay()
        self.wait_title_change('选择支付方法 - 订单支付', timeout=180)
        Log().info(u'跳转到充值成功页面')
        from pages.paymentProcessPages.receivedPayments.receivedPaymentsSuccessPage import ReceivedPaymentsSuccess
        return ReceivedPaymentsSuccess(self.driver)

    def online_order_payment(self, personal=True):
        """
        在线支付，通过个人网银或企业网银支付成功
        :param personal: 默认值为True，使用个人网银支付，否则使用企业网银支付
        :return: 在线支付成功页面
        """
        if personal:
            self.__personal_pay()
            try:
                self.continue_enterprise_pay()
            except:
                pass
        else:
            self.__enterprise_pay()
            self.continue_enterprise_pay()
        self.wait_url_contains('/payment/cfcaPay/cfcaPay',timeout=180)
        Log().info(u'跳转到订单支付成功 - 订单支付页面')
        from pages.paymentProcessPages.placeOrder.onlineOrderSubmitSuccessPage import OnlineOrderSuccessPage
        return OnlineOrderSuccessPage(self.driver)

    def __personal_pay(self):
        """个人网银支付流程：1.登录 2.确认支付 3.返回商城取货"""
        self.click_loc(self.__login_loc)
        Log().info('中金支付页面点击登录按钮')
        # 确认支付
        self.click_loc(self.__confirm_order_loc)
        Log().info('点击确认支付按钮')
        # # 再次确认支付
        # self.click_loc(self.__confirm_order_loc)
        # Log().info('再次点击确认支付按钮')
        # 返回商城取货
        self.click_loc(self.__back_to_get)
        Log().info('点击返回商城取货')

    def __enterprise_pay(self):
        """企业网银支付流程：1.登录 2.确认支付 3.登录网银复核 4.登录 5.确认支付 6.返回商城取货"""
        # 登录
        self.click_loc(self.__login_loc)
        Log().info('中金支付页面点击登录按钮')
        # 确认支付
        self.click_loc(self.__confirm_order_loc)
        Log().info('点击确认支付按钮')
        # 登录网银复核
        self.click_loc(self.__double_confirm_loc)
        Log().info('点击登录网银复核支付按钮')
        # 登录
        self.click_loc(self.__login_loc)
        Log().info('中金支付页面点击登录按钮')
        # 确认支付
        self.click_loc(self.__confirm_order_loc)
        Log().info('点击确认支付按钮')
        # 返回商城取货
        self.click_loc(self.__back_to_get)
        Log().info('点击返回商城取货')

    __continue_enterprise_pay_loc = ('xpath','//button[@id="proceed-button"]')

    def continue_enterprise_pay(self):
        """提交成功后网站存在校验任需提交的提示"""
        url = self.get_url()
        print(url)
        # 个人网银
        url2 = 'http://test.cpcn.com.cn/bmr/simulator_b2c'
        # 企业网银
        url3 = 'http://test.cpcn.com.cn/bmr/simulator_b2b'
        if ((url2 in url) or (url3 in url)) and (self.is_located(self.__continue_enterprise_pay_loc)):
            try:
                self.js_focus_element_loc(self.__continue_enterprise_pay_loc)
                self.click_loc(self.__continue_enterprise_pay_loc)
            except:
                Log().info('提交成功后网站不正确')





