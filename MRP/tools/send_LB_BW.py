# -*- coding: utf-8 -*-
"""
本脚本用于导出临检骨髓系统报表用于SEND转换。LB_BW
用户 王琳 李胜
前置条件 数据库服务器开机,账号密码链接成功.
"""
import pymssql
import os
import pandas as pd

db_port = '1433'
db_host = ''
db_user = 'jedaread'
db_pwd = 'jedaread'
db_name = 'RMSGS-new'

class SqlServerOperate(object):

    def __init__(self, server, port, user, password, db_name, as_dict=False):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = self.get_connect(as_dict=as_dict)
        pass

    def __del__(self):
        self.conn.close()

    def get_connect(self, as_dict=False):
        conn = pymssql.connect(
            server=self.server,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db_name,
            as_dict=as_dict,
            charset="utf8"
        )
        return conn

    def exec_query(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        result_list = list(cur.fetchall())
        cur.close()

        # 使用with语句（上下文管理器）来省去显式的调用close方法关闭连接和游标
        # print('****************使用 with 语句******************')
        # with self.get_connect() as cur:
        #     cur.execute(sql)
        #     result_list = list(cur.fetchall())   # 把游标执行后的结果转换成 list
        #     # print(result_list)

        return result_list

    def df_sql_query(self, sql):
        '''返回pandas.df DateFrame格式'''
        df = pd.read_sql(sql, self.conn)
        self.conn.close()
        return df


def sql_query():
    '''
    根据SendOffice专题编号列 数据库键值去重查询
    return 一个列表
    '''
    ms = SqlServerOperate(db_host, db_port, db_user, db_pwd, db_name)
    # sql_string = "SELECT PointName, PointID FROM dbo.RawDigital WHERE (PointName LIKE '%%')"
    sql_string = '''SELECT DISTINCT SendOffice  FROM [RMSGS-new].[dbo].[VIEW_GSCG] '''
    # 去重查询专题编号 SELECT DISTINCT
    temp_result_list = [x[0] for x in ms.exec_query(sql_string)]
    return temp_result_list

def df_query(SendOffice):
    '''
    in: 专题编号SendOffice 精确匹配
    out: pandas.df 格式
    '''
    ms = SqlServerOperate(db_host, db_port, db_user, db_pwd, db_name)
    sql_string = '''SELECT  *  FROM [RMSGS-new].[dbo].[VIEW_GSCG] WHERE SendOffice = '{}'
                    '''.format(SendOffice)
    return ms.df_sql_query(sql_string) 

# df = df_query('A2019028-T014-01').drop_duplicates(['CheckCode', 'PatientName'],keep='last',inplace=True).to_excel('sql.xlsx') # 根据ID 列去重 并导出excel
