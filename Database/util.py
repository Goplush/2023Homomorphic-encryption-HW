# -*- coding: utf-8 -*-

'''
实现基础包
'''
import pymysql, hashlib, json

def read_db_conf():
    # 读取 JSON 文件到字典
    with open('../database_config.json', 'r') as json_file:
        loaded_config = json.load(json_file)

    # 返回读取到的字典
    return dict(loaded_config)


def md5(s, salt='gytwl!@#$'):
    '''
    对用户密码进行哈希处理
    '''
    s = (str(s) + salt).encode('utf-8')
    return hashlib.md5(s).hexdigest()

class Database(object):
    '''
    连接数据库
    '''
    def __init__(self, mysql_info):
        self._connection = pymysql.connect(**mysql_info)

    def __del__(self):
        self._connection.close()
    
    def _execute(self, query):
        '''
        返回执行语句的查询结果
        '''
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            s = query.split()[0]

            res = None
            if s == 'update' or s == 'insert' or s == 'delete':
                self._connection.commit()
                cursor.close()
            elif s == 'select':
                res = cursor.fetchall()
                cursor.close()
            return (True, res)
        except Exception as e:
            self._connection.rollback()
            return (False, e)

mysql_info = read_db_conf()

db = Database(mysql_info)

def op_mysql(sql:str):
    return db._execute(sql)

def login(usr, pwd):
    '''
    登录情况处理:
    1 用户密码正确
    0 数据库错误
    -1 用户不存在
    -2 密码错误
    '''
    usr = md5(usr)
    pwd = md5(pwd)

    sql = "select usr from account where usr = '%s'" % (usr)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0 # 数据库错误
    if len(res) == 0:
        return -1 # 用户不存在
    
    sql = "select pwd from account where usr = '%s'" % (usr)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0 # 数据库错误
    for x in res:
        if x[0] == pwd:
            return 1 # 密码正确
    return -2 #密码错误

def register(usr, pwd):
    '''
    注册情况处理:
    1 成功注册
    0 数据库错误
    -1 用户已存在
    '''
    usr = md5(usr)
    pwd = md5(pwd)

    sql = "select usr from account where usr = '%s'" % (usr)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0   # 数据库错误
    if len(res) != 0:
        return -1  # 用户已存在

    sql = "insert into account(usr, pwd) values ('%s', '%s')" % (usr, pwd)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0   # 数据库错误
    return 1 # 成功注册

def test():
    # print(login('ss', '1234'))
    # print(register('ff', '123456'))
    print('test')

if __name__ == "__main__":
    test()