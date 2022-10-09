"""客商往来账查询页面"""

from common.log import Log
from pages.topCommonMenu.baseMenus import BaseMenus


class kswlInfoPage(BaseMenus):

    # 客商往来点击查询
    __click_merchants_select_loc = ('xpath', '//input[@id="searchAccountDetail"]')

    def click_merchants_select(self):
        """点击客商往来帐查询"""
        try:
            self.js_focus_element_loc(self.__click_merchants_select_loc)
            self.click_loc(self.__click_merchants_select_loc)
        except:
            Log().info('点击客商往来帐查询错误')

    # 获取日期数据元素
    __merchants_date_loc = ('xpath', '//span[@class="u_field_date"]')

    def check_merchants_data(self):
        """获取客商往来日期数据"""
        try:
            text = self.get_text_loc(self.__merchants_date_loc)
            return text
        except:
            Log().info('目前客商往来无数据')