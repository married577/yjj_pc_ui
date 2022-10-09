# coding=utf-8
"""预存支付成功页面"""
from common.basePage import Action
from common.log import Log


class PrestoreSuccess(Action):
    # 支付金额
    __price_of_prestore = ('xpath', '//div[@class="column column2 verifyContainer"]/span[@class="cor-or vm"]')

    # 获得的奖励金
    __reward_amount = ('xpath', '//span[@class="ft"]/span')

    # 获取预存支付成功页面-支付金额' ,例如￥0.02
    def get_price_pay(self):
        amount = self.get_text_loc(self.__price_of_prestore)
        money = str(amount).strip('¥')
        Log().info('预存支付成功页面-支付金额: %s' % money)
        return float(money)

    # 获取获得的奖励金
    def get_reward_amount(self):
        amount = self.get_text_loc(self.__reward_amount)
        Log().info('预存支付成功页-奖励金额: %s' % amount[1:5])
        return float(amount[1:5])




