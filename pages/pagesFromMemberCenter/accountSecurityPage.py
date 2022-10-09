"""账号安全页面"""
from common.log import Log
from pages.topCommonMenu.baseMenus import BaseMenus


class AccountSecurityPage(BaseMenus):
    # 修改密码类型元素定位
    __modify_username_pwd_loc = ('xpath', '//a[text()="修改密码"]')
    # 输入原密码
    __old_username_pwd_loc = ('xpath', '//input[@id="UserSPwd"]')
    # 输入新密码
    __new_username_pwd_loc = ('xpath', '//input[@id="UserNPwd"]')
    # 新密码确认
    __comfirm_username_pwd_loc = ('xpath', '//input[@id="UserCPwd"]')
    # 修改确认按钮
    __comfirm_pwd_loc = ('xpath', '//button[@id="SubmitRegister"]')
    # 获取再次确认弹框文本元素
    __aganin_comfirm_text_loc = ('xpath', '//p[@class="f_tac u_tit"]')
    # 点击弹框确认按钮
    __click_comfirm_button_loc = ('xpath', '//a[@class="layui-layer-btn0"]')

    def click_modify_username(self):
        """点击修改密码类型"""
        try:
            self.js_focus_element_loc(self.__modify_username_pwd_loc)
            self.click_loc(self.__modify_username_pwd_loc)
        except:
            Log().info('目前无修改密码类型')

    # 输入框输入员密码
    def input_old_username_pwd(self, pwd):
        self.send_keys_loc(self.__old_username_pwd_loc, pwd)

    # 输入框输入新密码
    def input_new_username_pwd(self, pwd):
        self.send_keys_loc(self.__new_username_pwd_loc, pwd)

    # 输入框输入新密码确认
    def input_comfirm_username_pwd(self, pwd):
        self.send_keys_loc(self.__comfirm_username_pwd_loc, pwd)

    # 点击确认按钮
    def click_comfirm_pwd(self):
        """点击确认按钮"""
        self.js_focus_element_loc(self.__comfirm_pwd_loc)
        self.click_loc(self.__comfirm_pwd_loc)

    def get_again_comfirm_text(self):
        """获取修改密码后再次登录弹窗文本"""
        try:
            text = self.get_text_loc(self.__aganin_comfirm_text_loc)
        except:
            text = ''
            Log().info('获取修改密码后再次登录弹窗文本错误')
        return text

    def new_login_click_cmfirm_button(self):
        """修改密码后再次登录确认"""
        try:
            self.js_focus_element_loc(self.__click_comfirm_button_loc)
            self.click_loc(self.__click_comfirm_button_loc)
        except:
            Log().info('修改密码后点击重新登录按钮错误')