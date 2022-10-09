"""通过数据库修改或新增数据的方法"""
from common.commonMethod import CommonMethod
import datetime,requests

from common.fileReader import IniUtil
from common.log import Log
import math


class OperationInDB(object):

    def __init__(self):
        self.com = CommonMethod()
        self.db = self.com.connect_db('b2b')
        self.env = IniUtil().get_value_of_option('test_env', 'env')

    def set_member_price_from_db(self, prod_no, prod_name, leaguer_price=''):
        """
        通过数据库设置商品的会员价
        :param prod_no: 商品编码
        :param leaguer_price: 会员价
        :return:
        """
        # 1. 删除测试商品数据库里面的记录
        sql = 'delete from tb_merchandise_leaguer where prod_no="%s";' % prod_no
        self.db.update(sql)
        if leaguer_price != '':
            # 2. 获取表tb_merchandise_leaguer中leaguer_id的最大数
            sql = 'select leaguer_id from tb_merchandise_leaguer order by leaguer_id desc limit 1;'
            result = self.db.search_one(sql)
            activity_id = str(int(result['leaguer_id'])+2)
            # 活动开始时间
            start_time = str(datetime.datetime.now() + datetime.timedelta(days=-1))[:19]
            # 活动结束时间
            end_time = str(datetime.datetime.now() + datetime.timedelta(days=1))[:19]
            # 2. 插入数据 -- 设置会员价
            sql = "INSERT INTO tb_merchandise_leaguer (`leaguer_id`, `branch_id`, `prod_no`, " \
                  "`prod_name`, `start_date`, `end_date`, `is_view`, `leagua_price`, `activity_policy`," \
                  " `activity_storage_number`, `highest_amount`, `lowest_amout`, `sort`," \
                  " `update_name`, `create_name`, `create_at`, `update_at`, `erpid`) VALUES " \
                  "('%s', 'FDG', '%s', '%s', '%s', '%s', '1', '%s', '111111', NULL, NULL, NULL, NULL, '湖北管理员', " \
                  "'湖北管理员', '2019-02-20 17:19:52', '2019-02-25 10:22:06', NULL);" % \
                  (activity_id, prod_no, prod_name, start_time, end_time, leaguer_price)
            self.db.update(sql)

    def add_prod_to_activity_from_db(self, prod_no, activity_type=None, activity_modular_id=None,
                                     start_time=None, end_time=None, price=''):
        """
        通过数据来给活动添加商品
        :param activity_type: 活动类型
        :param activity_modular_id: 活动id
        :param prod_no: 商品编码
        :param start_time: 活动开始时间
        :param end_time: 活动结束时间
        :param price: 活动价格
        :return:
        """

        # 1. 先删除同类活动同个商品的数据
        sql = "delete from tb_sale_activity where prod_no='%s' and activity_type='%s'" % (prod_no, activity_type)
        self.db.update(sql)
        if price != '':
            # 获取表tb_sale_activity的activity_id的最大值
            sql = "select activity_id from tb_sale_activity order by activity_id desc limit 1;"
            # # 链接数据库
            rs = self.db.search_one(sql)
            activity_id = str(int(rs['activity_id']) + 2)
            # 往活动上添加商品
            sql = "INSERT INTO `tb_sale_activity` (`activity_id`, `activity_modular_id`, `prod_no`, `start_date`, " \
                  "`end_date`, `activity_type`, `activity_policy`, `lowest_amount`, `branch_id`, `activity_order`," \
                  " `leve_name`, `activity_title`, `cust_type`, `area_id`, `cust_name`, `activity_price`, " \
                  "`activity_storage_number`, `highest_amount`, `activity_use_coupon`, `parent_id`," \
                  " `activity_group_id`, `create_at`, `update_at`, `cust_id`) VALUES ('%s', '%s', '%s', '%s', '%s'," \
                  " '%s', '自动化测试', NULL, 'FDG', NULL, NULL, '', '', '', NULL, '%s', NULL, NULL, '1', " \
                  "NULL, NULL, '2019-02-25 11:01:20', '2019-02-25 11:01:20', NULL);" % \
                  (activity_id, activity_modular_id, prod_no, start_time,end_time, activity_type, price)
            self.db.update(sql)

    def clear_sign_record(self, username):
        """
        删除签到表和签到客户表里面的记录
        :param username:
        :return:
        """
        # 通过用户登录名称查询cust_id
        sql = "SELECT data_id FROM tb_user_agent WHERE login_name= '%s'" % username
        result = self.db.search_one(sql)
        custid = str(int(result['data_id']))
        # print('用户的cust_id为：%s' % custid)

        # 删除签到表和签到客户表里面的记录
        sql = 'delete from tb_jzb_sign_record where cust_id = %s;' % custid
        print(sql)
        self.db.update(sql)
        sql = 'delete from tb_jzb_sign_cust where cust_id = %s;' % custid
        print(sql)
        self.db.update(sql)
        # 关闭数据库连接
        # self.db.close_db()

    def insert_sign_record(self, n, username):
        """
        插入签到记录表---连续型
        :param n: 截止到今天连续签到的天数，不算今天
        :param username: 用户名称
        :return:
        """
        # 通过用户登录名称查询cust_id
        sql = "SELECT data_id FROM tb_user_agent WHERE login_name= '%s'" % username
        result = self.db.search_one(sql)
        custid= str(int(result['data_id']))
        print('用户的cust_id为：%s' % custid)

        # 删除签到表和签到客户表里面的记录
        sql = 'delete from tb_jzb_sign_record where cust_id = %s;' % custid
        self.db.update(sql)
        sql = 'delete from tb_jzb_sign_cust where cust_id = %s;' % custid
        self.db.update(sql)

        # 当前时间
        current_time = datetime.datetime.now()
        # print(current_time)
        # 执行签到记录表n条数据
        for i in list(range(1, n + 1)):
            start_time = str(current_time + datetime.timedelta(days=-i))[:19]
            # print(start_time)
            # 获取表tb_jzb_sign_record中sign_record_id的最大数
            sql = 'select sign_record_id from tb_jzb_sign_record order by sign_record_id desc limit 1;'
            result = self.db.search_one(sql)
            sign_record_id = str(int(result['sign_record_id']) + 1)
            print(sign_record_id)
            sql1 = "insert into tb_jzb_sign_record VALUES ('%s','%s','%s','30','%s','%s',NULL,NULL)" % \
                  (sign_record_id, custid, start_time, start_time, start_time)
            print('签到记录表插入的sql为%s' % sql1)
            self.db.update(sql1)
        # 最后一天签到
        start_time = str(current_time + datetime.timedelta(days=-1))[:19]
        print(start_time)
        # 3.获取表tb_jzb_sign_cust中sign_cust_id的最大数
        sql = 'select sign_cust_id from tb_jzb_sign_cust order by sign_cust_id desc limit 1;'
        result = self.db.search_one(sql)
        sign_cust_id = str(int(result['sign_cust_id']) + 1)
        # 执行签到客户表 一条数据
        sql2 = "insert into tb_jzb_sign_cust VALUES ('%s','%s','FDG','%s','%s','%s','%s')" % \
               (sign_cust_id, custid, n, start_time, start_time, start_time)
        print('签到客户表插入一条数据的sql为%s' % sql2)
        self.db.update(sql2)
        # 关闭数据库连接
        # self.db.close_db()

    def insert_sign_interrupt(self, n, username):
        """
        插入签到记录表---非连续
        :param n: 截止到今天之前非连续签到的天数
        :param username: 用户编码
        :return:
        """
        # 通过用户登录名称查询cust_id
        sql = "SELECT data_id FROM tb_user_agent WHERE login_name= '%s'" % username
        result = self.db.search_one(sql)
        custid = str(int(result['data_id']))
        print('用户的cust_id为：%s' % custid)

        # 删除签到表和签到客户表里面的记录
        sql = 'delete from tb_jzb_sign_record where cust_id = %s;' % custid
        self.db.update(sql)
        sql = 'delete from tb_jzb_sign_cust where cust_id = %s;' % custid
        self.db.update(sql)

        # 当前时间
        current_time = datetime.datetime.now()
        # print(current_time)
        # 执行签到记录表n条数据
        for i in list(range(1, n + 1)):
            start_time = str(current_time + datetime.timedelta(days=-i-1))[:19]
            print(start_time)
            # 获取表tb_jzb_sign_record中sign_record_id的最大数
            sql = 'select sign_record_id from tb_jzb_sign_record order by sign_record_id desc limit 1;'
            result = self.db.search_one(sql)
            sign_record_id = str(int(result['sign_record_id']) + 1)
            print(sign_record_id)
            sql1 = "insert into tb_jzb_sign_record VALUES ('%s','%s','%s','30','%s','%s',NULL,NULL)" % \
                  (sign_record_id, custid, start_time, start_time, start_time)
            print('签到记录表插入的sql为%s' % sql1)
            self.db.update(sql1)

        # 昨天不签到，前天进行签到
        start_time = str(current_time + datetime.timedelta(days=-2))[:19]
        print(start_time)
        # 3.获取表tb_jzb_sign_cust中sign_cust_id的最大数
        sql = 'select sign_cust_id from tb_jzb_sign_cust order by sign_cust_id desc limit 1;'
        result = self.db.search_one(sql)
        sign_cust_id = str(int(result['sign_cust_id']) + 1)
        # 执行签到客户表 一条数据
        sql2 = "insert into tb_jzb_sign_cust VALUES ('%s','%s','FDG','%s','%s','%s','%s')" % \
               (sign_cust_id, custid, n, start_time, start_time, start_time)
        print('签到客户表插入一条数据的sql为%s' % sql2)
        self.db.update(sql2)

    def update_customer_order_limit_price(self, username, limit_type='', limit_price=''):
        """
        更新客户的订单起配金额
        :param username:客户的登录用户名
        :param limit_type: 订单起配金额拦截类型：''-不设置,1-不拦截,2-当天第一笔拦截,3-全部拦截,默认为不设置客户起订金额
        :param limit_price: 客户订单起配金额，默认值为空
        :return:
        """
        sql = "update tb_cust_main set order_limit_type='%s',order_limit_price = '%s' where cust_id=" \
              "(SELECT data_id FROM tb_user_agent WHERE login_name='%s')" % \
              (limit_type, limit_price, username)
        # 更新
        self.db.update(sql)

    def update_branch_order_limit_price(self, limit_type, limit_price, branch_id='FDG'):
        """
        更新分公司的订单起配金额
        :param limit_type: 订单起配金额拦截类型1-不拦截,2-当天第一笔拦截,3-全部拦截
        :param limit_price: 分公司订单起配金额
        :param branch_id: 分公司branch_id
        :return:
        """
        sql = "update tb_branch_configure set order_limit_type='%s', order_limit_price='%s' where branch_id='%s'" % \
              (limit_type, limit_price, branch_id)
        # 更新
        self.db.update(sql)

    def set_branch_and_customer_order_limit_price(self, branch_limit_type, branch_limit_price, username,
                                                  cust_limit_type='', cust_limit_price='', branch_id='FDG'):
        """
        同时设置分公司和客户的起配金额
        :param branch_limit_type: 分公司订单起配金额拦截类型1-不拦截,2-当天第一笔拦截,3-全部拦截
        :param branch_limit_price: 分公司订单起配金额
        :param username: 客户的登录用户名
        :param cust_limit_type: 客户订单起配金额拦截类型：''-不设置,1-不拦截,2-当天第一笔拦截,3-全部拦截,默认为''
        :param cust_limit_price: 客户订单起配金额，默认值为空
        :param branch_id: 分公司branch_id
        :return:
        """
        self.update_branch_order_limit_price(branch_limit_type, branch_limit_price, branch_id)
        self.update_customer_order_limit_price(username, cust_limit_type, cust_limit_price)
        self.db.close_db()

    def get_custid_by_login_name(self, username):
        """
        通过登录用户名获取客户的custid
        :param username: 登录用户名
        :return:
        """
        sql = "SELECT data_id FROM tb_user_agent WHERE login_name='%s'" % username
        result = self.db.search_one(sql)
        cust_id = result['data_id']
        self.db.close_db()
        return cust_id

    def get_danw_nm_by_login_name(self, username):
        """
        通过登录用户名获取客户的danw_nm
        :param username:
        :return: danw_nm
        """
        sql = "SELECT danw_nm FROM tb_cust_main WHERE cust_id=" \
              "(SELECT data_id FROM tb_user_agent WHERE login_name='%s')" % username
        result = self.db.search_one(sql)
        danw_nm = result['danw_nm']
        self.db.close_db()
        return danw_nm

    def get_password_by_login_name(self, username):
        """
        通过用户名获取密码
        :param username:
        :return: 登录密码
        """
        sql = "select login_pwd from tb_user_agent where branch_id='FDG' and login_name = '%s'" % username
        result = self.db.search_one(sql)
        if result:
            login_pwd = result['login_pwd']
            return login_pwd
        else:
            print("登录用户名【%s】不存在！" % username)
            return None

    def calculate_group_price(self, gid):
        """
        根据套餐组合的gid计算套餐组合套餐价
        :param gid: 套餐组合的gid
        :return: 返回组合套餐的价格
        """
        sql = "select sum(group_price * group_num) as price from tb_group_merchandise where group_id = '%s';" % gid
        result = self.db.search_one(sql)
        price = float(result['price'])
        self.db.close_db()
        return price

    def check_jiuzhoudou(self):
        # 获取有流水的客户
        sql1 = "select  biz_id_2 as cust_id from tb_dou_account GROUP BY biz_id_2;"
        result = self.db.search_all(sql1)
        i = 1
        sum = 0
        for item in result:
            # 客户id
            cust_id = item['cust_id']
            # 查客户总账表 获取总账，以及custid  139470  36971   where cust_id = '139470'
            sql = "select dou_amount, last_amount, last_account_id from tb_dou_cust where cust_id = '%s'" % cust_id
            result = self.db.search_one(sql)
            # 获取该客户最后一条数据的
            sql = "select account_id, snap_dou_amount, account_amount from tb_dou_account where biz_id_2 = '%s'  order by account_id desc LIMIT 1;" % cust_id
            result_last = self.db.search_one(sql)
            # ====================================================
            # 比较最后一条流水和总账表的数据是否一致
            # if result['last_account_id'] != result_last['account_id']:
            #     # 流水号
            #     Log().info("客户:%s，总账表的最后发生的流水号:%s跟流水表最后一条流水号%s不一致" % (cust_id, result['last_account_id'],result_last['account_id']))
            # 总账余额

            # 总账表余额
            zz_sum = math.floor(result['dou_amount'])
            # 最后一笔流水的余额
            zz_ls = math.floor(result_last['snap_dou_amount'])
            if zz_sum != zz_ls:
                # ①检查总账表的余额，是否跟最后一笔流水表的余额一致
                Log().info("客户:%s，总账表的余额:%s跟流水表最后一条记录的余额%s不一致" % (cust_id, zz_sum, zz_ls))
            if result['last_amount'] != result_last['account_amount']:
                # ②检查总账表的最后一次九州豆变更金额，是否跟流水表的最后一次发生金额一致
                Log().info("客户:%s，总账表的最后一次发生数额:%s跟流水表最后一条记录的余额%s不一致" % (cust_id, result['last_amount'],result_last['account_amount']))
            # else:
            #     print("客户：%s,总账表与最后一笔流水的数据一致" % cust_id)
            # =======================================================
            # ③检查流水表变更金额之和，是否跟总账表的总账一致
            sql = "select sum(account_amount) as sum from tb_dou_account where biz_id_2 = '%s';" % cust_id
            result_amount = self.db.search_one(sql)
            # 流水表合计
            zz_count = math.floor(result_amount['sum'])
            if zz_sum != zz_count:
                Log().info("客户:%s，总账表余额：%s与流水表计算余额：%s不一致" % (cust_id, zz_sum, zz_count))
            else:
                print('客户：%s， 总账表余额与流水表计算余额一致' % cust_id)
            # =========================================================
            # =========================
            # ④检查当前流水的余额+下一笔流水的变更金额 = 下一笔流水的余额
            sql = "select snap_dou_amount, account_amount from tb_dou_account where biz_id_2 = '%s'  order by account_id " % cust_id
            result = self.db.search_all(sql)
            j = 0
            result_list = {}
            for rs in result:
                result_list[j] = (rs['snap_dou_amount'], rs['account_amount'])
                j = j + 1
            count = len(result_list)
            for i in list(range(count - 1)):
                # 当前余额
                ye = result_list[i][0]
                # 下一条的变更
                cha = result_list[i + 1][1]
                # 下一条的余额
                ye_next = result_list[i + 1][0]
                if ye_next != ye + cha:
                    Log().info("客户%s的第%s条流水和第%s条流水的计算有误,即(%s!=%s+%s)" % (cust_id, i + 1, i + 2, ye_next, ye, cha))
            sum = sum + 1
            i = i + 1
        Log().info("检查了%s条数据" % sum)

    def delete_fan_dian_activity(self):
        """
        通过数据库删除正在进行的返点活动
        :return:
        """
        sql = ""
        self.db.update(sql)
        self.db.close_db()

    def update_prods_stock(self, prod_info):
        """
        修改商品库存
        :param prod_info: {prod:number, prod2:number2}
        :return:
        """
        sqls = []
        for item in prod_info.items():
            sql = "update tb_merchandise_storage set storage_number = '%s' " \
                  "where branch_id='FDG' and prod_no = '%s' ;" % (item[1], item[0])
            sqls.append(sql)
        # print(sqls)
        # 执行
        self.db.excute_multiple(sqls)

    def get_current_datetime(self):
        """
        获取数据库的当前日期和时间
        :return:
        """
        sql = "SELECT SYSDATE()"
        current_time = self.db.search_one(sql)
        current_time = current_time['SYSDATE()']
        print("数据库的当前时间为：", current_time)
        # 关闭数据库连接
        self.db.close_db()
        return current_time

    def delete_coupon(self, name):
        """
        删除优惠券活动，根据活动名称
        :param name:
        :return:
        """
        sql = "delete from tb_coupon where coupon_name = '%s'" % name
        self.db.update(sql)
        self.db.close_db()

    def select_fenlei(self, name):
        """
        查询首页分类
        :param name:1,药品分类；2，器械分类
        :return:
        """
        sql = "update tb_branch_configure set cms_top_default_catalog = '%s'" % name
        self.db.update(sql)
        self.db.close_db()


    def delete_activity_bounty(self):
        """
        结束正在进行的“下单返奖励金”优惠券
        :return:
        """
        sql = "UPDATE tb_reward_activity SET end_time = DATE_ADD(NOW(), INTERVAL - 2 MINUTE) WHERE NOW()  BETWEEN start_time AND end_time AND create_by='湖北管理员' AND delete_flag = '0'"
        self.db.update(sql)


    def active_bounty(self,name):
        """
        根据名字激活下单返奖励金
        :param name:
        :return:
        """
        sql = "UPDATE tb_reward_activity SET start_time = DATE_ADD(NOW(), INTERVAL - 2 MINUTE) " \
              ", end_time = DATE_ADD(NOW(), INTERVAL + 60 MINUTE) where create_by='湖北管理员' " \
              "and delete_flag = '0' and  activity_name='%s'" % name
        self.db.update(sql)

    def get_acitivity_bounty(self):
        """
        得到正在使用的返奖励金活动的名字
        :return: 返回奖励金的名字
        """
        sql = "SELECT activity_name FROM `tb_reward_activity` WHERE NOW()  BETWEEN start_time AND end_time " \
              "AND create_by='湖北管理员' AND delete_flag = '0';"
        result = str(self.db.search_one(sql))

        if eval(result):
            Log().info("result=" + eval(result)["activity_name"])

            return eval(result)["activity_name"]
        else:
            Log().info("没有正在使用的返奖励金活动")

            return ""

    def get_shouyepeizhi(self):
        """
        得到正在使用的首页配置,1是1.0,2是2.0
        :return: 返回是1 or 2
        """
        sql = "select pc_version_using FROM tb_branch_configure  WHERE branch_id='FDG';"
        result = self.db.search_one(sql)
        result = result["pc_version_using"]
        # result = 2
        # self.db.close_db()
        return result

    def get_moneyback(self):
        """
        得到正在使用的充值返利活动
        :return: 返回是活动的数量
        """
        sql = "SELECT COUNT(*) FROM tb_activity_base a WHERE a.activity_type = '105' AND a.STATUS = '1' " \
              "AND a.branch_id = 'FDG' AND NOW()  BETWEEN begin_time AND end_time ;"
        result = self.db.search_one(sql)
        count = result['COUNT(*)']
        # print("当前正在进行的充值返利活动数量为：%s" % count)
        Log().info("当前正在进行的充值返利活动的数量为: %s" % count)

        return count

    def get_searchpeizhi(self):
        """
        得到正在使用的搜索配置,1是列表模式,2是大图模式
        :return: 返回是1 or 2
        """
        sql = "select searchPageConfiguration FROM tb_branch_configure  WHERE branch_id='FDG';"
        result = self.db.search_one(sql)
        result = result['searchPageConfiguration']
        # self.db.close_db()
        # result = 2
        return result

    def get_database_address_info(self):
        """
        查询上线公司地址名称(首页顶部显示)
        :return:
        """
        sql = 'select map_company from tb_site_map where is_pc_show = "1"'
        text = self.db.search_all(sql)
        return [i['map_company'] for i in text]
        # text = ['安徽', '北京', '重庆', '赤峰', '长春', '大连', '达州', '恩施', '福建', '广东', '广西', '广元', '广州', '贵州', '湖北', '湖南', '黄冈', '河南', '杭州', '黑龙江', '淮安', '河源', '江苏', '江西', '荆州', '荆门', '江汉', '辽宁', '兰州', '凉山', '泸州', '绵阳', '内蒙古', '宁德', '南充', '南平', '宁夏', '平顶山', '四川', '石家庄', '上海', '十堰', '商丘', '遂宁', '随州', '三明', '深圳', '天津', '温州', '万州', '芜湖', '新疆', '襄阳', '厦门', '信阳', '咸宁', '台州', '应城', '宜昌', '湛江', '肇庆', '驻马店', '陕西', '海南', '北京器械', '浙江器械', '福建器械', '临汾', '亳州', '安阳', '运城', '贵港', '太原药材', '宁波', '云南', '山东药九九', '安心中药', '榆林', '岳阳', '渭南', '连云港', '无锡', '和田', '重庆药九九', '苏州', '阳泉', '赣州九州通']
        # return text

    def get_order_data_resource(self):
        """
        查询订单的数据来源，1 代表：同步1.0， 2 代表：同步：2.0
        :return: 返回 1 or 2
        """
        sql = "select order_data_resource from tb_branch_configure WHERE branch_id = 'FDG';"
        result = self.db.search_one(sql)
        result = result['order_data_resource']
        # self.db.close_db()
        # result = 2
        return result

    def get_user_useragenid(self,name,sign=1,branchid='FDG'):
        """
        获取绑定手机号的useragenid
        :param name: 绑定手机号或者账号
        :param branchid:
        :return:
        """
        if sign == 1:
            sql = 'select user_agent_id from tb_user_agent where bind_mobile="{}" and branch_id="{}"'.format(name,branchid)
        else:
            sql = 'select user_agent_id from tb_user_agent where login_name="{}" and branch_id="{}"'.format(name,branchid)
        result = self.db.search_one(sql)['user_agent_id']
        return result

    def get_bind_phone_password(self,username):
        """通过账号获取useragenid"""
        if self.env == 'pre':
            useragenid = self.get_user_useragenid(username)
            url = 'http://10.4.9.111:31354/api/auth_gateway/account/get_password?platform=b2b&userAgentId={}'.format(useragenid)
            password = requests.get(url=url).json()['password']
        elif self.env == 'prod':
            useragenid = self.get_user_useragenid(username,branchid='fr9')
            url = 'http://10.161.0.47:30198/api/auth_gateway/account/get_password?platform=b2b&userAgentId={}'.format(useragenid)
            password = requests.get(url=url).json()['password']
        else:
            url = ''
            password = ''
        return password



#
if __name__ == '__main__':
    d = OperationInDB()
    print(d.get_user_useragenid('13041169694'))
