# coding=utf-8
"""回款的支付成功页面"""
from common.basePage import Action
from common.log import Log


class ReceivedPaymentsSuccess(Action):
    # 支付金额
    __price_of_prestore = ('xpath', '//span[@class="cor-or vm"]')

    # 获取预存支付成功页面-支付金额' ,例如￥0.02
    def get_price_pay(self):
        amount = self.get_text_loc(self.__price_of_prestore)
        Log().info('预存支付成功页面-支付金额: %s' % amount[1:])
        return float(amount[1:])
