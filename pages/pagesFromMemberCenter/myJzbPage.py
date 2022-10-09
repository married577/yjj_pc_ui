"""我的九州币页面
/member/credits/index.htm"""
from common.basePage import Action
from common.log import Log
from common.commonMethod import CommonMethod
import datetime
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException
from time import sleep
import re

class myJzbPage(Action):

    # 我的九州币值
    __my_jzb = ('xpath', '//div[@class="m_myjzb_quick z_three_panel"]//b')
    # 九州币图标
    __jzb_icon = ('xpath', '//div[@class="item item1"]//span[@class="icon"]')
    # 九州币明细
    __jzb_detail = ('xpath', '//div[@class="item item2"]//a[@href="/member/jzb/index.htm"]')
    # 九州币玩法
    __jzb_wanfa = ('xpath', '//div[@class="item item2"]//a[@class="jzbPlay"]')
    # 九州币玩法的title
    __jzb_wanfa_title = ('xpath', '//div[@class="layui-layer-title"]')
    # 九州币玩法弹框的确定按钮
    __jzb_wanfa_confirm = ('xpath', '//a[@class="layui-layer-btn0"]')
    # 签到文字
    __jzb_qiandao = ('xpath', '//div[@class="signIn f_fr"]/span')
    # 签到领币按钮
    __jzb_sign_button = ('xpath', '//div[@class="signInButton"]/button')
    # 提示：今天已签到
    __jzb_sign_today = ('xpath', '//div[@class="signInButton"]/span')
    # 非会员用户签到后弹出框的签到获赠九州币
    __pop_up_jzb = ('xpath', '//span[@class="signInInclude"]')
    # 会员用户签到后弹出框的会员回馈九州币
    __pop_up_huiuan = ('xpath', '//span[@class="signInOther"]')
    # VIP会员店
    __vip_huiuan = ('xpath', '//div[@class="signIn_after"]')
    # 好礼超值兑的更多好礼
    __more_gift = ('xpath', '//p[@class="m_title"]/a[@href="/member/jzb/mall.htm"]')
    # 兑换记录
    __exchange_record = ('xpath', '//p[@class="m_title"]/a[@href="/member/jzb/recordList.htm"]')
    # 底部-查看更多好礼
    __buttom_more_gift = ('xpath', '//a[@class="u_jzb_more"]')


    # 等待页面刷新
    def wait_page_refresh(self, timeout=10):
        """等待页面某元素过期，即等带页面刷新,此页面用我的九州币判断"""
        try:
            self.wait_element_staleness(self.__my_jzb, timeout)
        except (TimeoutException, NoSuchElementException):
            pass

    def get_into_myJzbPage(self):
        """
        通过url进入我的九州币页面
        :return:
        """
        __url_myJzbPage = CommonMethod().get_endpoint('myJzbPage')
        self.open(__url_myJzbPage, '我的九州币')
        self.wait_title_change('我的九州币')
        Log().info('打开我的九州币页面')

    def get_my_jzb(self):
        """
        获取九州币值
        :return: 九州币值
        """
        my_jzb = self.get_text_loc(self.__my_jzb)
        Log().info('我的页面九州币值为：%s' % my_jzb)
        return my_jzb

    def my_jzb_minus(self, b, n):
        """
        比较签到前后的九州币值的差=期望值
        :param b:
        :param n:
        :return:
        """
        a = self.get_my_jzb()
        jzb = int(a) - int(b)
        Log().info('签到后新增的九州币为：%s' % jzb)
        if jzb == n:
            return True
        else:
            return False

    def click_my_jzb(self):
        """
        点击我的九州币
        :return:
        """
        self.click_loc(self.__my_jzb)
        Log().info('点击我的九州币')
        self.wait_url_contains('/member/jzb/index.htm', 5)
        from pages.pagesFromMemberCenter.myJzbDetails import myJzbDetails
        return myJzbDetails(self.driver)

    def click_jzb_detail(self):
        """
        点击九州币明细
        :return:
        """
        self.click_loc(self.__jzb_detail)
        Log().info('点击九州币明细按钮')
        self.wait_url_contains('/member/jzb/index.htm', 5)
        from pages.pagesFromMemberCenter.myJzbDetails import myJzbDetails
        return myJzbDetails(self.driver)

    def click_jzb_wanfa(self):
        """
        点击九州币玩法
        :return:
        """
        self.click_loc(self.__jzb_wanfa)
        Log().info('点击九州币玩法')

    def check_wanfa_title(self):
        """
        验证九州币玩法弹框的title
        :return:
        """
        text = self.get_text_loc(self.__jzb_wanfa_title)
        if text == '九州币玩法':
            return True
        else:
            return False

    def click_wanfa_confirm(self):
        """
        九州币玩法弹框点击确定按钮
        :return:
        """
        self.click_loc(self.__jzb_wanfa_confirm)
        Log().info('九州币玩法弹框点击确定按钮')

    def check_huiuan_icon_display(self):
        """
        检查“VIP会员店 >”文本显示
        :return:
        """
        try:
            self.is_visibility(self.__vip_huiuan)
            result = True
            msg = '会员用户正确显示VIP标签'
        except TimeoutException:
            result = False
            msg = '会员用户没有显示VIP标签'
        return result, msg

    def convert_time_minus(self, n):
        """
        把时间2019-02-09转换成类似：2019-2-9
        :param n: n =0 代表当天，n =1 代表昨天，n = 2 代表前天，依次类推
        :return:
        """
        current_time = datetime.datetime.now() + datetime.timedelta(days=-n)
        start_time = str(current_time)[:10]
        # 将时间中的-0 替换-,去掉0
        new_time = start_time.replace('-0', '-')
        Log().info('获取的时间为：%s' % new_time)
        return new_time

    def convert_time_plus(self, n):
        """
        把时间2019-02-09转换成类似：2019-2-9
        :param n: n =0 代表当天，n =1 代表明天，n = 2 代表后台，依次类推
        :return:
        """
        current_time = datetime.datetime.now() + datetime.timedelta(days=+n)
        start_time = str(current_time)[:10]
        # 将时间中的-0 替换-,去掉0
        new_time = start_time.replace('-0', '-')
        Log().info('获取的时间为：%s' % new_time)
        return new_time

    def jzb_sign(self, n):
        """
        日历中判断一天的九州币是否签到
        :param n: n =0 代表当天，n =1 代表昨天，n = 2 代表前天，依次类推
        :return:
        """
        time = self.convert_time_minus(n)
        __jzb_sign = ('xpath', '//td[@lay-ymd="' + time + '"]/span/img')
        if 'jzb-dayQ.png' in self.get_attribute_loc(__jzb_sign, 'src'):
            Log().info("已签到")
            return True
        else:
            return False

    def jzb_sign_n(self, list):
        """
        日历中判断连续多天九州币是否签到
        :param list: 例如[0] [0,1] [0,1,2]
        :return:
        """
        result = True
        for a in list:
            if self.jzb_sign(a) == False:
                result = False
        return result

    def is_jzb_sign_exit(self, n):
        """
        判断没有签到
        :return:
        """
        time = self.convert_time_minus(n)
        __jzb_sign = ('xpath', '//td[@lay-ymd="' + time + '"]/span/img')
        if self.is_located(__jzb_sign) is False:
            Log().info("当天没有签到")
            return True
        else:
            return False

    def is_jzb_gift_exit(self, n):
        """
        判断连续签到的第3天或者第7天有礼物的图标
        :param n: n =0 代表当天，n =1 代表明天，n = 2 代表后天，依次类推
        :return:
        """
        time = self.convert_time_plus(n)
        __jzb_sign = ('xpath', '//td[@lay-ymd="' + time + '"]/span/img')
        # print(self.get_attribute_loc(__jzb_sign, 'src'))
        if 'jzb-gift.png' in self.get_attribute_loc(__jzb_sign, 'src'):
            msg = "连续签到的第3天或者第7天有礼物的图标"
            Log().info("连续签到的第3天或者第7天有礼物的图标")
            return True, msg
        else:
            msg = "连续签到的第3天或者第7天,没有找到礼物的图标"
            return False, msg

    def get_text_qiandao(self):
        """
        获取签到底部的文字
        :return:
        """
        string = self.get_text_loc(self.__jzb_qiandao)
        qiandao = re.findall(r"\d+\.?\d*", string)
        Log().info('签到底部的文字为：%s' % qiandao)
        return qiandao

    def is_sign_button_display(self):
        """
        判断签到领币按钮是否显示
        :return:
        """
        try:
            self.is_visibility(self.__jzb_sign_button, 10)
            result = True
        except TimeoutException:
            result = False
        return result

    def click_sign_button(self):
        """
        我的九州币页面点击签到领币按钮
        :return:
        """
        if self.is_sign_button_display():
            self.click_loc(self.__jzb_sign_button)
            Log().info(u'我的九州币页面点击"签到领币"按钮')

    def is_tick_indisplay(self, n):
        """
        判断7天时间轴不显示显示打钩
        :return:True 或者 False
        """
        # 打钩的图标
        __click_icon = ('xpath', '//li[' + str(n) + ']/div[@class="jzb-signIn"]/img[contains(@src,"/static/content/images/member/jzb-Q.png")]')
        try:
            self.is_invisibility(__click_icon, 10)
            result = True
        except TimeoutException:
            result = False
        return result

    def is_tick_display(self, n):
        """
        判断7天时间轴显示打钩
        :return:True 或者 False
        """
        # 打钩的图标
        __click_icon = ('xpath', '//li[' + str(n) + ']/div[@class="jzb-signIn"]/img[contains(@src,"/static/content/images/member/jzb-Q.png")]')
        try:
            self.is_visibility(__click_icon, 20)
            result = True
        except TimeoutException:
            result = False
        return result

    def check_sign_today(self):
        """
        检查是否显示'今天已签到'
        :return:
        """
        text = self.get_text_loc(self.__jzb_sign_today)
        if text == '今天已签到':
            return True
        else:
            return False

    def check_round_jzb(self, n):
        """
        获取7天时间轴，圆圈上方显示的签到九州币
        :param n: n的取值为1-7, n=1 代表第一天
        :return:
        """
        # 7天时间轴，圆圈上方显示的签到九州币
        __upper_round = ('xpath', '//div[@class="signInAwards"]/ul/li[' + str(n) + ']/div[1]')
        jzb = self.get_text_loc(__upper_round)
        a = re.findall(r"\d+\.?\d*", jzb)
        Log().info('第%s天圆圈上方显示的签到九州币为%s' % (n, a[0]))
        return a[0]

    def check_pop_jzb(self, value):
        """
        获取签到弹出框--签到获赠的九州币值
        :return: 签到弹出框--签到获赠的九州币值
        """
        jzb = self.get_text_loc(self.__pop_up_jzb)
        Log().info('签到弹出框--签到获赠的九州币值为%s' % jzb)
        if jzb == value:
            return True
        else:
            return False

    def check_huiuan_pop(self, value):
        """
        获取会员用户签到后弹出的会员回馈九州币值
        :param value: 会员用户签到后弹出的会员回馈九州币值
        :return:
        """
        jzb = self.get_text_loc(self.__pop_up_huiuan)
        a = re.findall(r"\d+\.?\d*", jzb)
        Log().info('签到弹出框--会员回馈九州币值为%s' % a[0])
        if a[0] == value:
            return True
        else:
            return False

    def click_more_gift(self):
        """
        点击更多好礼
        :return:
        """
        self.click_loc(self.__more_gift)
        Log().info('点击更多好礼')
        self.wait_title_change('九州币商城', 10)
