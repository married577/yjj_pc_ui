# coding=utf-8
"""订单支付成功页 ---- 在线支付

页面标题：订单支付成功 - 订单支付
1. 当应付金额大于0，即未使用余额支付，或余额不足的情况时，订单提交成功
url:/payment/cfcaPay/cfcaPayResult.htm
2. 应付金额等于0，即使用了余额支付且余额足够时，订单提交成功
url:/member/order/successPage.htm

注：虽然url不一致，但页面title，以及页面元素一致，故当做同一个页面处理，即选择在线支付提交订单成功之后的页面
"""
from common.log import Log
from pages.topCommonMenu.baseMenus import BaseMenus


class OnlineOrderSuccessPage(BaseMenus):

    # 支付方式
    __payment_mode_loc = ('xpath', "//span[text()='支付方式：']//following-sibling::div[1]")
    # 支付金额
    __order_amount_loc = ('xpath', "//span[text()='支付金额：']/following-sibling::b")
    # 订单优惠
    __order_discount_loc = ('xpath', "//span[text()='订单优惠：']/following-sibling::b")
    # 钱包余额
    __wallet_balance_loc = ('xpath', "//span[text()='钱包余额：']/following-sibling::b")
    # 点击去充值
    __click_to_recharge_loc = ('', "//a[text()='点击去充值']")
    # 逛逛首页
    __return_to_homepage_loc = ('xpath', "//button[text()='逛逛首页']")
    # 查看订单
    __view_order_loc = ('xpath', "//button[text()='查看订单']")
    # 网银支付方式，订单支付成功页支付金额
    __price_of_prestore = ('xpath', '//div[@class="part part3"]//b')

    # 获取预存支付成功页面-支付金额' ,例如￥0.02
    def get_price_pay(self):
        amount = self.get_text_loc(self.__price_of_prestore)
        print(amount)
        Log().info('预存支付成功页面-支付金额: %s' % amount[1:])
        return float(amount[1:])

    def get_payment_mode(self):
        """
        获取订单支付方式
        :return: 返回订单支付方式
        """
        return self.get_text_loc(self.__payment_mode_loc)

    def get_order_amount(self):
        """
        获取订单金额
        :return: 订单金额 -- float类型
        """
        # 文本：¥133.5
        text = self.get_text_loc(self.__order_amount_loc)
        amount = float(text[1:])
        return amount

    def get_order_discount(self):
        """
        获取订单优惠金额 -- 只有订单使用了优惠时，该字段才显示
        :return: 订单优惠金额 -- float类型
        """
        # 文本：¥133.5
        try:
            text = self.get_text_loc(self.__order_discount_loc)
        except:
            discount = float(0)
        else:
            discount = float(text[1:])
        return discount

    # 获取所有需要校验的金额将入列表(订单金额、优惠金额)
    def get_online_order_prices_all_list(self):
        # 获取支付金额
        amount_sum = self.get_order_amount()
        # 获取订单优惠金额
        amount_yh = self.get_order_discount()
        # 返回金额列表
        all_amount_list = [amount_sum, amount_yh]
        return all_amount_list

    def get_wallet_balance(self):
        """
        获取钱包余额 --- 只有使用了余额支付时，该字段才显示
        :return:钱包余额 -- float类型
        """
        # 文本：¥133.5
        text = self.get_text_loc(self.__wallet_balance_loc)
        balance = float(text[1:])
        return balance

    def go_to_recharge(self):
        """
        点击去充值
        :return: 去充值的页面对象
        """
        # 点击去充值
        Log().info('点击去充值链接')
        self.click_loc(self.__click_to_recharge_loc)
        Log().info('等待页面跳转到充值页面')
        self.wait_url_contains('/payment/cfcaPay/payBalance.htm')
        from pages.paymentProcessPages.receivedPayments.receivedPaymentsPaymentPage import ReceivedPaymentsPayment
        return ReceivedPaymentsPayment(self.driver)

    def back_to_homepage(self):
        """
        跳转到首页
        :return: 首页页面对象
        """
        Log().info('点击逛逛首页按钮')
        self.click_loc(self.__return_to_homepage_loc)
        Log().info('等待页面跳转到首页')
        self.wait_title_change('九州通')
        from pages.homePage import HomePage
        return HomePage(self.driver)

    def go_to_my_order_page(self):
        """
        跳转到我的订单页面
        :return: 我的订单页面对象
        """
        Log().info('点击我的订单按钮')
        self.click_loc(self.__view_order_loc)
        Log().info('等待页面跳转到我的订单页面')
        self.wait_title_change('我的订单')
        from pages.myOrderPage import MyOrder
        return MyOrder(self.driver)
