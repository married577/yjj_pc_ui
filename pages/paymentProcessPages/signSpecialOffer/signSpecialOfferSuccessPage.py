# coding=utf-8
"""签约特供成功的页面"""
from common.basePage import Action
from common.log import Log


class SignSpecialOfferSuccess(Action):

    # 开通成功提示信息
    __signSpecialOffer_success = ('xpath', '//h3[@class="s_result_tit"]')

    # 签约成功后获取的优惠券张数
    __signSpecialOffer_couponNUm = ('xpath', '//h3[@class="s_result_quan"]/em')

    def get_success_message(self):
        success_message = self.get_text_loc(self.__signSpecialOffer_success)
        Log().info('签约特供开通成功的提示信息: %s' % success_message)
        if '您签约特供商品购买权限已开通成功～' in success_message:
            return True
        else:
            return False

    def get_coupon_num(self):
        couponNum = self.get_text_loc(self.__signSpecialOffer_couponNUm)
        Log().info('签约特供开通成功获取的优惠券：%s' % couponNum)
        return couponNum


