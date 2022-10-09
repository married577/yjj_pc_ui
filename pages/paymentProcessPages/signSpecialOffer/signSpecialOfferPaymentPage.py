# coding=utf-8
"""签约特供的支付页面"""
from pages.paymentProcessPages.selectOnlinePaymentMode import PaymentMode
from pages.homePage import HomePage
from common.log import Log

class PaymentSignSpecialOffer(PaymentMode):

    # 前往支付按钮
    __confirm_payment = ('xpath', '//div[@id="onlinepaydiv"]//input[@value="前往支付" ]')

    def select_payment_mode_go_to_pay(self, payment_mode):
        """
        选择支付方式，并前往支付，直至支付成功
        :param payment_mode: '支付宝'表示支付宝支付，‘微信’表示微信支付，‘个人网银’表示个人网银支付，否则表示企业网银支付
        :return: 返回相应的支付成功页面
        """
        return self.select_payment_mode(payment_mode=payment_mode, loc=self.__confirm_payment, entry='签约特供')

    # 支付金额,期望结果是300.00
    __pay_amount = ('xpath', '//span[@id="PayAmount"]')


    """ =======================================签约特供页面=============================================== """


    # 签约特供页面顶部的的4个元素

    # 左上角的提示信息
    __leftTop_loc = ('xpath','//div[@class="m_tips_layout"]/div[@class="fl"]')
    # 左上角的提示信息
    __leftTop_message_loc = ('xpath', '//div[@class="fl"]/span[1]')

    # 左上角的',阅读'文字
    __leftTop_readtext_loc = ('xpath','//div[@class="fl"]/span[contains(text(),"阅读")]')

    # 左上角的《签约特供指南》链接
    ___leftTop_sign_specialOffer_guide_loc = ('xpath', '//div[@class="fl"]/a[@href="/activity/sign/toSign.htm?showIframe=1"]')

    # 页面中间的《签约特供指南》链接
    ___middle_sign_specialOffer_guide_loc = ('xpath', '//a[@href="/activity/sign/toSign.htm?showIframe=1"]')

    # "去开通"链接    ('xpath', '//div[@class="fl"]/span[contains(text(),'阅读')])
    ___sign_open_up_loc = ('xpath', '//div[@class="fl"]/a[@href="/activity/sign/PayPro.htm"]')

    # 去缴费按钮
    __pay_fee_loc =('xpath', '//a[@href="/payment/cfcaPay/paySpeoffer.htm"]')


    # 点击左上角的《签约特供指南》链接
    def click_sign_specialOffer_guide(self):
        self.click_loc(self.___leftTop_sign_specialOffer_guide_loc)
        Log().info(u"签约特供页面点击左上角的《签约特供指南》链接")

    # 点击"去开通"链接
    def click_sign_open_up(self):
        self.click_loc(self.___sign_open_up_loc)
        Log().info(u'点击"去开通"链接')

    # 点击"去缴费"链接
    def click_pay_fee(self):
        self.click_loc(self.__pay_fee_loc)
        Log().info(u'点击"去缴费"链接')

    # 点击页面中间的《签约特供指南》链接
    def click_middle_sign_specialOffer_guide(self):
        self.click_loc(self.___middle_sign_specialOffer_guide_loc)
        Log().info(u"点击页面中间的《签约特供指南》链接")

    # 检查未签约用户左上角的信息显示：尊敬的客户，您还未开通特供专区商品购买权限 ，阅读 《签约特供指南》  或   去开通'
    def compare_text_leftTop(self):
        text = self.get_text_loc(self.__leftTop_loc)
        expected_text = '尊敬的客户，您还未开通特供专区商品购买权限 ，阅读 《签约特供指南》  或   去开通'
        if (expected_text ==text):
            return True
        else:
            return False

    # 检查已签约用户左上角的信息显示：恭喜您！您的特供权限已开通并赠送了优惠券 ， 我的优惠券   。
    def compare_text_leftTop_sign(self):
        text = self.get_text_loc(self.__leftTop_loc)
        expected_text = '尊敬的客户，恭喜您！您的特供权限已开通并赠送了优惠券 ， 我的优惠券   。 不再提示'
        if (expected_text ==text):
            return True
        else:
            return False

    # 检查未缴费的用户左上角的信息显示：尊敬的客户，您已签订协约，请尽快去缴费，已便为您提供更好的服务我知道了
    def compare_text_leftTop_nopay(self):
        text = self.get_text_loc(self.__leftTop_loc)
        expected_text = '尊敬的客户，您已签订协约，请尽快去缴费，已便为您提供更好的服务我知道了'
        if (expected_text == text):
            return True
        else:
            return False

    # 我的优惠券按钮
    __my_coupon = ('xpath', '//div[@class="fl"]/a[@href="/front/newCoupon/myCoupon.json"]')
    # 已签约特供的用户，进入到签约特供专题页，点击“我的优惠券”
    def click_my_coupon(self):
        self.click_loc(self.__my_coupon)
        Log().info('点击我的优惠券')
        self.wait_title_change('我的优惠券 - 会员中心 - 九州通网', timeout=30)



    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #签约特供指南页面 # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 签约特供指南页面的title
    __guide_title_loc = ('xpath','//div[@class="m_tit"]/span')
    # 检查签约特供指南页面的title='签约特供指南'
    def get_text_guide(self):
        text = self.get_text_loc(self.__guide_title_loc)
        expected_text = '签约特供指南'
        if (text in expected_text):
            return True
        else:
            return False

    # 签约特供指南页面的“去开通”按钮
    __guide_sign_open_up_loc = ('xpath','//a[@href="/activity/sign/PayPro.htm"]/b')

    # 点击签约特供指南页面的“去开通”按钮
    def click_guide_sign_open_up(self):
        self.click_loc(self.__guide_sign_open_up_loc)
        Log().info(u'点击签约特供指南页面的“去开通”按钮')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 开通签约特供权限页面 # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # 我已仔细阅读并同意协议的勾选框
    __read_agree_protocol_loc = ('xpath','//span[@class="btb"]')

    # 下一步，确认并且缴费
    __next_pay_loc = ('xpath', '//input[@value="下一步，确认并缴费"]')


    # 勾选我已仔细阅读并同意协议的勾选框
    def click_read_agree_protocol(self):
        self.click_loc(self.__read_agree_protocol_loc)
        Log().info('勾选我已仔细阅读并同意协议的勾选框')


    # 点击【"下一步，确认并缴费"】
    def click_next_pay(self):
        self.click_loc(self.__next_pay_loc)
        Log().info('点击下一步，确认并缴费')

    # 从开通签约特供权限页面进入签约特供支付页面的流程
    def from_signUp_come_into_signSpecialOffer_payment(self):
        # 勾选我已仔细阅读并同意协议的勾选框
        self.click_read_agree_protocol()
        # 点击【"下一步，确认并缴费"】
        self.click_next_pay()


    #从首页签约特供banner进入缴费支付页面
    def from_home_to_signSpecialOffer_payment1(self):
        homepage = HomePage(self.driver)
        # 首页点击签约特供banner
        homepage.click_sign_specialOffer()
        # # 等待新窗口打开
        # homepage.wait_until_windows_open()
        # # 切换到签约特供页面
        # homepage.switch_window()
        # 点击去开通按钮
        self.click_sign_open_up()

        # 等待新窗口打开
        self.wait_until_windows_open()
        # 切换到开通签约特供权限页面
        self.switch_window()
        # 勾选我已仔细阅读并同意协议的勾选框然后点击【"下一步，确认并缴费"】
        self.from_signUp_come_into_signSpecialOffer_payment()
        self.wait_title_change('线上支付 - 开通签约特惠权限', timeout=30)
        from pages.paymentProcessPages.signSpecialOffer.signSpecialOfferPaymentPage import PaymentSignSpecialOffer
        return PaymentSignSpecialOffer(self.driver)


    # 左上角的提示信息没有时，首页-签约特供banner-中间的签约特供指南链接--去开通--勾选同意协议--确认缴费
    def from_home_to_signSpecialOffer_payment(self):
        homepage = HomePage(self.driver)

        # 首页点击签约特供banner
        homepage.click_sign_specialOffer()

        # 点击页面中间的签约特供指南
        self.click_middle_sign_specialOffer_guide()

        # 等待新窗口打开
        self.wait_until_windows_open()
        # 切换到签约特供指南页面
        self.switch_window()
        # 点击签约特供指南页面的去开通按钮
        self.click_guide_sign_open_up()

        # 等待新窗口打开
        self.wait_until_windows_open()
        # 切换到开通签约特供权限页面
        self.switch_window()

        # 勾选我已仔细阅读并同意协议的勾选框然后点击【"下一步，确认并缴费"】
        self.from_signUp_come_into_signSpecialOffer_payment()

        self.wait_title_change('线上支付 - 开通签约特惠权限', timeout=30)
        from pages.paymentProcessPages.signSpecialOffer.signSpecialOfferPaymentPage import PaymentSignSpecialOffer
        return PaymentSignSpecialOffer(self.driver)





