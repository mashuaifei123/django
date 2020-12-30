import pymssql
# import pandas as pd
from datetime import datetime, timedelta
import numpy as np

db_port = '1433'
db_host = '10.10.91.180'
db_user = 'sa'
db_pwd = 'XMG3-Rel.1'
db_name = 'JCIHistorianDB'
Room_pid = [('1132', 23, 15),
            ('1133', 24, 16),
            ('1134', 25, 17),
            ('1135', 26, 18),
            ('1142B', 28, 20),
            ('1142A', 29, 21),
            ('1141A', 30, 22),
            ('1140', 39, 31),
            ('1159', 40, 32),
            ('1158', 41, 33),
            ('1157', 42, 34),
            ('1156', 14, 9),
            ('1153', 43, 35),
            ('1152', 44, 36),
            ('1151', 45, 37),
            ('1248A', 123, 111),
            ('1249A', 124, 112),
            ('1250A', 125, 113),
            ('1251A', 126, 114),
            ('1252A', 162, 141),
            ('1253A', 163, 142),
            ('1254A', 164, 143),
            ('1255A', 165, 144),
            ('1241A', 47, 145),
            ('1242A', 166, 146),
            ('1243A', 167, 147),
            ('1244A', 97, 86),
            ('1245A', 98, 87),
            ('1246A', 109, 100),
            ('1247A', 110, 101),
            ('1262A', 48, 127),
            ('1263A', 138, 128),
            ('1264A', 139, 129),
            ('1265A', 140, 130),
            ('1266A', 192, 168),
            ('1267A', 193, 169),
            ('1268A', 194, 170),
            ('1256A', 195, 171),
            ('1257A', 196, 172),
            ('1258A', 197, 173),
            ('1259A', 198, 174),
            ('1260A', 199, 175),
            ('1261A', 82, 75),
            ('1332', 247, 231),
            ('1333', 248, 232),
            ('1336', 249, 233),
            ('1342', 250, 234),
            ('1341', 251, 235),
            ('1340', 252, 236),
            ('1339', 253, 237),
            ('1338', 254, 238),
            ('1359', 268, 255),
            ('1358', 269, 256),
            ('1357', 270, 257),
            ('1356', 271, 258),
            ('1355', 272, 259),
            ('1352A', 273, 260),
            ('1351A', 274, 261),
            ('1432', 312, 300),
            ('1433', 313, 301),
            ('1434', 314, 302),
            ('1444', 316, 304),
            ('1443', 354, 335),
            ('1442A', 355, 336),
            ('1441', 356, 337),
            ('1440', 357, 338),
            ('1465', 329, 318),
            ('1464', 330, 319),
            ('1463', 331, 320),
            ('1462', 332, 321),
            ('1461', 333, 322),
            ('1460', 334, 323),
            ('1459', 358, 339),
            ('1456A', 359, 340),
            ('1455A', 360, 341),
            ('1454A', 361, 342),
            ('1453', 362, 343)]
roomid = [{'id':i, 'text': Room_pid[i][0] } for i in range(len(Room_pid))]

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


def sql_query(wpsid, data0, data1):
    '''
    根据pid 开始结束时间返回一个元组列表
    '''
    ms = SqlServerOperate(db_host, db_port, db_user, db_pwd, db_name)
    # sql_string = "SELECT PointName, PointID FROM dbo.RawDigital WHERE (PointName LIKE '%%')"
    sql_string = '''SELECT PointSliceID, UTCDateTime, ActualValue 
                    FROM FloatSampleView
                    WHERE (UTCDateTime >= '{}')
                    AND (UTCDateTime < '{}')
                    AND (PointSliceID = '{}')
                    '''.format(data0, data1, wpsid)
    # print(sql_string)
    temp_result_list = ms.exec_query(sql_string)
    return temp_result_list


def room_to_id(room_id):
    '''
    房间号匹配温度湿度pid无法匹配返回False
    '''
    for x, y, z in Room_pid:
        if room_id == x:
            wd_pid = y
            sd_pid = z
            if wd_pid or sd_pid:
                return wd_pid, sd_pid


def wsd_query(wd_pid, sd_pid, data0, data1):
    '''
    输入:开始结束时间及房间号码
    返回:修正格式后温度湿度列表
    '''
    wd_list = sql_query(wpsid=wd_pid, data0=data0, data1=data1)
    sd_list = sql_query(wpsid=sd_pid, data0=data0, data1=data1)
    #print(len(wd_list))
    # 时间加8小时系统默认记录0时区时间.UTC +08:00
    # 把None值替换为0，再把错误数据换回到原始位置
    wd_list = [(x, '{}'.format((y + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M %S")), 0) if z == None else (
        x, '{}'.format((y + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M %S")), '{:.1f}'.format(float(z)))
               for x, y, z in wd_list]
    wd_list.sort()
    sd_list = [(x, '{}'.format((y + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M %S")), 0) if z == None else (
        x, '{}'.format((y + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M %S")), '{:.1f}'.format(float(z)))
               for x, y, z in sd_list]
    sd_list.sort()
    if len(wd_list) % 96 == 0:
        return wd_list, sd_list
    else:
        print('数据异常不等于96倍数请检查')


def datetformat(dateinput):
    '''
    输入:时间字符串
    输出:格式化后的时间格式转换为可以调用标准字符-8时区
    '''
    date_out = datetime.strptime(dateinput, '%Y%m%d')
    date_out = date_out - timedelta(hours=8)
    return date_out


def get_data( b, c, d):

    # study_number = a
    # study_name = input('请输入实验名称:')
    # room_id = input('房间ID:')
    #room_id = b
    # s_datetime = input('起始日期:举例(20190725)')
    s_datetime = c
    # t_datetime = input('结束日期:举例(20190725)')
    t_datetime = d
    data = {}
    rew_wd_list = []
    res_sd_list = []
    wdmax_lsit = []
    sdmax_lsit = []
    wdmin_list = []
    sdmin_list = []
    wdpass_lsit = []
    wdunpass_list = []
    wdpassrate_lsit = []
    sdpass_lsit = []
    sdunpass_list = []
    sdpassrate_lsit = []
    roomid_list = []

    temperature1 = (26, 16)  # 兔狗猴 1F 3F 4F
    temperature2 = (29, 18)  # 豚鼠
    temperature3 = (26, 20)  # SPF 2F
    # start anal
    for i in b:
        room_id = roomid[int(i)].get('text')
        roomid_list.append(room_id)

        wd_pid, sd_pid = room_to_id(room_id)
        data0, data1 = datetformat(s_datetime), datetformat(t_datetime) + timedelta(hours=24)  # 加24小时才能与时间对应包含输入的那一天.
        rew_list, res_list = wsd_query(wd_pid, sd_pid, data0, data1)
        data['rew_date'] = [x[1] for x in rew_list]
        wd = [x[2] for x in rew_list]
        sd = [x[2] for x in res_list]
        rew_wd_list.append(wd)
        res_sd_list.append(sd)

        wdmax_lsit.append(np.max([float(i) for i in wd]))
        wdmin_list.append(np.min([float(i) for i in wd if float(i) > 0]))
        sdmax_lsit.append(np.max([float(i) for i in sd]))
        sdmin_list.append(np.min([float(i) for i in sd if float(i) > 0]))

        room_id_2 = int(room_id[1:2])
        if room_id in ['1151', '1152', '1153']:
            wdpass = len([x for x in wd if temperature2[1] < float(x) < temperature2[0]])
        elif room_id_2 == 2:
            wdpass = len([x for x in wd if temperature3[1] < float(x) < temperature3[0]])
        elif room_id_2 in [1, 3, 4]:
            wdpass = len([x for x in wd if temperature1[1] < float(x) < temperature1[0]])
        wdpass_lsit.append(wdpass)
        wdunpass_list.append(len(rew_list) - wdpass)
        wdpassrate_lsit.append('%.2f'% (wdpass / len(rew_list) * 100)+'%')

        sdpass_lsit.append(len([x for x in sd if 40 < float(x) < 70]))
        sdunpass_list.append(len(rew_list) - len([x for x in sd if 40 < float(x) < 70]))
        sdpassrate_lsit.append('%.2f'%(len([x for x in sd if 40 < float(x) < 70]) / len(res_list) * 100)+'%')

    wd = ['温度']
    sd = ['湿度']

    room_wd = [i+j for i in roomid_list for j in wd]
    room_sd = [i + j for i in roomid_list for j in sd]
    room_wsd = room_wd + [''] + room_sd

    data['wd_box'] = room_wd
    data['sd_box'] = room_sd
    data['wsd_box'] = room_wsd
    data['rew_wd'] = rew_wd_list
    data['res_date'] = [x[1] for x in res_list]
    data['res_sd'] = res_sd_list
    data['wdmax'] = wdmax_lsit
    data['wdmin'] = wdmin_list
    data['sdmax'] = sdmax_lsit
    data['sdmin'] = sdmin_list

    data['wdpass'] = wdpass_lsit
    data['wdunpass'] = wdunpass_list
    data['wdpass_rate'] = wdpassrate_lsit

    data['sdpass'] = sdpass_lsit
    data['sdunpass'] = sdunpass_list
    data['sdpass_rate'] = sdpassrate_lsit

    #data['studyid'] = study_number
    data['s_time'] = s_datetime
    data['t_time'] = t_datetime
    data['roomid'] = roomid
    data['room_now_id'] = ','.join(roomid_list)
    date = c[:4] + '-' + c[4:6] + '-' + c[6:] + '+-+' + d[:4] + '-' + d[4:6] + '-' + d[6:]
    data['date'] = date
    # 暂时满足

    # 多房间分析表
    print(len(roomid_list))
    if len(roomid_list) >= 2:
        data['room_now_id_m'] = ','.join(roomid_list)
        multiple = [{'a': roomid_list[i], 'b': wdmax_lsit[i], 'c': wdmin_list[i], 'd': wdunpass_list[i], 'e': wdpass_lsit[i], 'f': wdpassrate_lsit[i], 'g': sdmax_lsit[i], 'h': sdmin_list[i], 'i': sdunpass_list[i], 'j': sdpass_lsit[i], 'k': sdpassrate_lsit[i], 'l': b[i]} for i in range(len(roomid_list))]

    else:
        data['room_id'] = roomid_list[0]
        data['wdmax0'] = wdmax_lsit[0]
        data['wdmin0'] = wdmin_list[0]
        data['sdmax0'] = sdmax_lsit[0]
        data['sdmin0'] = sdmin_list[0]

        data['wdpass0'] = wdpass_lsit[0]
        data['wdunpass0'] = wdunpass_list[0]
        data['wdpass_rate0'] = wdpassrate_lsit[0]

        data['sdpass0'] = sdpass_lsit[0]
        data['sdunpass0'] = sdunpass_list[0]
        data['sdpass_rate0'] = sdpassrate_lsit[0]
        multiple = [{}]
        data['room_now_id_m'] = ''
    data['multiple'] = multiple
    return {'data': data}


def get_day_data(b,c,d):

    data1 = get_data(b,c,d)
    data = data1['data']
    day ={}
    date1 = np.array(data['res_date'])

    wd = np.array([float(x) for x in data['rew_wd'][0]] )

    wd = [wd[i] for i in range(len(wd)) if i%96 ==0]

    print(wd)

    wd_bar = np.array(wd).mean()
    print(wd_bar)
    #move range

    #s_i = np.array([np.std(wd_list[i],ddof = 1) for i in range(len(wd_list))])

    wd_1  = wd[:-1]
    wd_2 = wd[1:]
    wd_mr = [abs(i-j) for i ,j in zip(wd,wd[1:]) ]
    wd_mr_bar = np.array(wd_mr).mean()
    print(wd_bar)
    print(wd_mr_bar)

    #e2 = 2.660
    e2 = 2.660
    wd_ucl = wd_bar + e2*wd_mr_bar
    wd_ucl_c = wd_bar + e2*wd_mr_bar * (1/3)
    wd_ucl_b = wd_bar + e2*wd_mr_bar * (2/3)
    wd_lcl = wd_bar - e2*wd_mr_bar
    wd_lcl_c =wd_bar - e2*wd_mr_bar * (1/3)
    wd_lcl_b = wd_bar - e2*wd_mr_bar * (2/3)


    #d4 = 3.268
    d4 = 3.268
    wd_mr_ucl = wd_mr_bar * d4
    wd_mr_ucl_c = wd_mr_bar + (wd_mr_ucl - wd_mr_bar)  *(1/3)
    wd_mr_ucl_b = wd_mr_bar + (wd_mr_ucl - wd_mr_bar) *(2/3)
    wd_mr_lcl = 0
    wd_mr_lcl_c = wd_mr_bar - (wd_mr_ucl - wd_mr_bar) *(1/3)
    wd_mr_lcl_b = wd_mr_bar - (wd_mr_ucl - wd_mr_bar) *(2/3)


    n = len(wd)
    day['wd_max'] = float("{:.2f}".format(np.max(wd)+0.3))
    day['wd_min'] = float("{:.2f}".format(np.min(wd)-0.3))
    day['mr_max'] = float("{:.2f}".format(np.max(wd_mr)+0.2))




    day['date1'] = [i for i in range(n)]
    day['wd'] = wd
    day['wd_bar'] = wd_bar

    day['wd_ucl'] = wd_ucl
    day['wd_ucl_c'] = wd_ucl_c
    day['wd_ucl_b'] = wd_ucl_b
    day['wd_lcl'] = wd_lcl
    day['wd_lcl_c'] = wd_lcl_c
    day['wd_lcl_b'] = wd_lcl_b



    day['wd_mr_ucl'] = wd_mr_ucl
    day['wd_mr_ucl_c'] = wd_mr_ucl_c
    day['wd_mr_ucl_b'] = wd_mr_ucl_b
    day['wd_mr_lcl'] = wd_mr_lcl
    day['wd_mr_lcl_c'] = wd_mr_lcl_c
    day['wd_mr_lcl_b'] = wd_mr_lcl_b
    day['wd_mr_bar'] = wd_mr_bar
    day['wd_mr'] = wd_mr

    day['s_time'] = data['s_time']
    day['t_time'] = data['t_time']
    day['roomid'] = data['roomid']
    day['room_id'] = data['room_id']
    day['wdmax0'] =  data['wdmax0']
    day['wdmin0'] = data['wdmin0']
    day['wdpass0'] = data['wdpass0']
    day['wdunpass0'] = data['wdunpass0']
    day['wdpass_rate0'] = data['wdpass_rate0']

    return {'day': day}







