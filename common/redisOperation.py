import redis


class RedisOperation(object):

    def __init__(self, connections):
        # 创建连接池
        # pool = redis.ConnectionPool(host='10.3.5.42', port='6379', db='3')
        pool = redis.ConnectionPool(**connections)
        self.r = redis.Redis(connection_pool=pool)

    def string_get(self, key):
        """
        redis的数据类型为string时，通过key获取value
        :param key:
        :return:
        """
        value = self.r.get(key)
        if value:
            value = value.decode('utf8')
        return value

    def string_set(self, key, value):
        """
        redis的数据类型为string时，更新key的value，若key不存在，则新增
        :param key:
        :param value:
        :return:
        """
        self.r.set(key, value)


if __name__ == "__main__":
    # 获取redis连接
    from common.fileReader import IniUtil
    ini = IniUtil()
    section = "redis_" + 'test'
    con = ini.get_value_of_option(section, 'b2b')
    import json
    connection = json.loads(con)
    r = RedisOperation(connection)
    rs = r.string_get('bigDataCustPro:DWI00022231FDG')
    print(rs)
    print(type(rs))
    rs = eval(rs)
    print(rs)
    print(type(rs))


