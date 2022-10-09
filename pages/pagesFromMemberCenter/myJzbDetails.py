"""我的九州币明细页面
/member/jzb/index.htm"""

from common.basePage import Action
from common.log import Log


class myJzbDetails(Action):

    # 我的九州豆明细第一条记录的详细说明
    __first_message = ('xpath', '//tbody/tr[1]/td[2]/span')
    # 我的九州豆明细第一条记录的收入/支出
    __first_money = ('xpath', '//tbody/tr[1]/td[@class="u_jzb_num"]')

    def get_text_first_message(self, n):
        """
        获取我的九州豆明细第一条记录的详细说明
        :param n: n =1 代表第一条， n =2 代表第二条
        :return: 我的九州豆明细第一条记录的详细说明
        """
        # 我的九州豆明细第n条记录的详细说明
        __first_message = ('xpath', '//tbody/tr[' + str(n) + ']/td[2]/span')
        first_message = self.get_text_loc(__first_message)
        Log().info('九州豆明细第%s条记录的详细说明:%s' % (n, first_message))
        return first_message

    def get_text_first_money(self, n):
        """
        获取我的九州豆明细第一条记录的收入/支出
        :param n: n =1 代表第一条， n =2 代表第二条
        :return: 我的九州豆明细第一条记录的收入/支出
        """
        # 我的九州豆明细第n条记录的收入/支出
        __first_money = ('xpath', '//tbody/tr[' + str(n) + ']/td[@class="u_jzb_num"]')
        first_money = self.get_text_loc(__first_money)
        Log().info('九州豆明细第%s条记录的收入/支出:%s' % (n, first_money))
        return first_money

    def get_text_first(self, n):
        """
        获取我的九州豆明细第n条记录的详细说明和收入/支出
        :param n: n =1 代表第一条， n =2 代表第二条
        :return: 我的九州豆明细第n条记录的详细说明和收入/支出
        """
        first_message = self.get_text_first_message(n)
        first_money = self.get_text_first_money(n)
        return first_message, first_money
