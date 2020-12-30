import urllib.request, http.cookiejar
import urllib.parse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import pandas as pd
import datetime
import time
from .config import ptsAPIserverUrl, ptsDeviceID, ptsUserNameID, ptsUserPassword, Meas_list, ABC_UC_list, Urine_str, Urine_Sediment_display
from .config import sqlserver, service_name, appserverservlet, sqluser, sqlpw

ptsAPIserverUrl = ptsAPIserverUrl
UserNameID = ptsUserNameID
UserPassword = ptsUserPassword
DeviceID = ptsDeviceID

class PTS_RQ_RS:
    """
    pristima 系统传输 API 扩展
    参考手册:Pristima API User Documentation and Reference Guide
    RQ 提交数据
    RS 返回数据
    数据格式为xml
    urllib 用于提交和返回数据 注意编码
    服务器地址: pristima API 服务器servlet地址
    用户名：注意先建立在pristima系统中
    密码:注意先建立在pristima系统中
    设备ID 注意先建立在pristima系统中
    """
    def __init__(self, PtsUrl: str, UserID: str, UserPW: str, DeviceID: str):
        self.PtsUrl = PtsUrl
        self.UserId = UserID
        self.UserPW = UserPW
        self.DeviceID = DeviceID
        self.cookie = http.cookiejar.CookieJar()
        # 声明一个CookieJar对象实例来保存cookie
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 利用urllib库的HTTPCookieProcessor对象来创建cookie处理器
        self.opener = urllib.request.build_opener(self.handler)
        # 通过handler来构建opener
        self.headers = {'Connection': 'keep-alive', 'Content-Type': 'text/xml;charset=UTF8', 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    def _failure(self, pts_rs):
        """查询xml异常返回FailureMessage内容"""
        pts_rs_rd = pts_rs.read().decode('utf8')
        root = ET.fromstring(pts_rs_rd)
        for item in root.findall('Doctype'):  # 查询确认是否返回异常
            if 'pts_rs_failure' in item.text:
                try:
                    error_message = root.findall('FailureMessage')[0].text
                    return False, error_message
                except:
                    return False, '登入出错,检查账号密码设备名称等'
        return pts_rs_rd

    def get_cookie(self):
        """建立链接获取cookie"""
        request = urllib.request.Request(self.PtsUrl)
        self.res = self.opener.open(request)  # 1.get  获取cookie 建立连接

    def login(self):
        """登入系统
        设备ID 用户 密码 2次提交返回
        """
        device_rq = r'<?xml version="1.0" encoding="UTF-8" ?><PTS><Doctype>pts_rq_device_access</Doctype><DeviceID>{}</DeviceID></PTS>'
        device_rq = device_rq.format(self.DeviceID)
        self.post_data(device_rq)
        """---登入---"""
        login = r'<?xml version="1.0" encoding="UTF-8"?><PTS><Doctype>pts_rq_login</Doctype><UserID>{}</UserID><Password>{}</Password></PTS>'
        login = login.format(self.UserId, self.UserPW)
        self.post_data(login)

    def logout(self):
        """登出回话"""
        logout = r'<?xml version="1.0" encoding="UTF-8" ?><PTS><Doctype>pts_rq_logout</Doctype><AccessStatus>0</AccessStatus></PTS>'
        self.post_data(logout)

    def post_data(self, xml_str):
        """编码提交
        urllib.request.request数据提交返回
        """
        if isinstance(xml_str, (str)):
            data_b = bytes(xml_str, encoding='utf8')
        else:
            data_b = xml_str
        data_req = urllib.request.Request(self.PtsUrl, data_b, self.headers)
        try:
            data_rq = self.opener.open(data_req)
            opread = self._failure(data_rq)
            if not opread[0]:
                return opread[1]
            return opread
        except urllib.error.HTTPError as e:
            print(' '.join([e, '一般为会话问题']))

    def run(self):
        self.get_cookie()
        self.login()

    def PTS_RQ(self, Category, **kwargs):
        """
        PTS_RQ_STUDY_DATA
        Category 需要查询的内容 例如: 给药 DirectDosing
        **kwargs 参数字典 例如:StudyName = PTS-OQ-24
        return xml str
        """
        RQ_0 = r'<?xml version="1.0" encoding="UTF-8" ?><PTS><Doctype> PTS_RQ_STUDY_DATA </Doctype><Category>{}</Category></PTS>'
        RQ_0 = RQ_0.format(Category)
        root = ET.fromstring(RQ_0)
        for key in kwargs:  # 添加字典内容到xml tree
            element = Element(key)  # 定义节点
            element.text = kwargs.get(key)  # 定义节点内容
            root.append(element)  # 合并
        RQ_0_bytes = ET.tostring(root)  # 转化为字符串b
        opread = self.post_data(RQ_0_bytes)
        # 或者返回ET.fromstring(opread) ET_tree 格式
        return opread

    def PTS_RS_query(self, ET_tree, keylist):  # 暂时停用没想到好办法
        """
        PTS_RS_STUDY_DATA
        传入需要读取的参数列表keylist
        return [{key:value}]
        """
        value_list = []
        item_dict = {}
        for item in keylist:
            item_dict.clear()
            for ita in ET_tree.iter(item):  # 全文查找.建议最好知道规格.
                item_dict.update({ita.tag:ita.text})
                print(item_dict)
            value_list.append(item_dict)
        return value_list


def get_BodyWeight(StudyName):
    """输入StudyName
       返回DF 仅为最近一次体重详情
    """
    pts = PTS_RQ_RS(ptsAPIserverUrl, UserNameID, UserPassword, DeviceID)
    # 初始化类
    pts.run()
    # 启动类链接
    BW = pts.PTS_RQ('BodyWeight ',
                    StudyName=StudyName,
                    StudyAnimalOnly='Y',
                    LatestDataOnly='Y',)
    pts.logout()
    root = ET.fromstring(BW)
    rock=[['StudyAnimalNumber','RawWeight','StorageUnit','DateTaken',]]
    for item in root.findall('BodyWeightInfo'):
        rock.append([item.find(i).text for i in rock[0]])
    df_BW = pd.DataFrame(rock[1:], columns=rock[0])
    df_BW['DateTaken'] = pd.to_datetime(df_BW['DateTaken'])
    df_g = df_BW.groupby('DateTaken')
    now_time = datetime.datetime.now()
    jgzj_data = now_time - df_BW['DateTaken'].apply(lambda x: now_time - x).min()
    df_g = df_g.get_group(jgzj_data)
    df_g.loc[:,'DateTaken'] = df_g.loc[:,'DateTaken'].apply(lambda x:time.mktime(x.timetuple()))
    df_g.loc[:,'DateTaken'] = df_g.loc[:,'DateTaken'].apply(lambda x:time.strftime('%Y-%m-%d',time.localtime(x)))
    # df_g.values.tolist()
    return df_g


def get_BW_Group(BW: pd.DataFrame):
    """组装分组求体重和
       返回:体重详情及分组球和后DataFrame
    """
    import copy
    BW_DF = copy.deepcopy(BW)
    BW_DF.insert(0, 'GroupNumber', BW_DF['StudyAnimalNumber'].apply(lambda x: x[0])) # 插入一列Group
    BW_DF['RawWeight'] = BW_DF['RawWeight'].astype('float')
    BW_DF.insert(1, 'ForM', BW_DF['StudyAnimalNumber'].apply(lambda x: x[1]))  # 插入一列性别
    BW_DF['RawWeight'] = BW_DF['RawWeight'].apply(lambda x: x/1000 if 'g' in BW_DF['StorageUnit'].values else x )  # 判断体重是否为'g' 转化为kg 
    BW_DF_G = BW_DF.groupby(['GroupNumber','ForM'])  # 用性别和组进行分组
    BW_DF_G = pd.DataFrame([[n[0],n[1],v['RawWeight'].agg('sum')] for n, v in BW_DF_G], columns=['GroupNumber','ForM','RawWeightSum'])  # 分组求汇总体重
    BW_DF_G = BW_DF_G.pivot_table(values='RawWeightSum', index='GroupNumber', columns=['ForM'])  # 透视表格长转宽
    BW_DF_G.rename(columns={'F':'FBWSum','M':'MBWSum',},inplace=True)
    BW_DF_G = BW_DF_G.applymap(lambda x: 0 if pd.isnull(x) else x)  # 判断是否为空体重. 空就为0 
    BW_DF_G['BWSum'] = BW_DF_G.apply(lambda x: x['FBWSum']+x['MBWSum'], axis=1)  # 增加新列体重和
    BW_DF_G = BW_DF_G.reset_index()
    return BW, BW_DF_G


def get_ProArticle(StudyName):
    """输入StudyName
       返回df_PA
    """
    pts = PTS_RQ_RS(ptsAPIserverUrl, UserNameID, UserPassword, DeviceID)
    # 初始化类
    pts.run()
    # 启动类链接
    PA = pts.PTS_RQ('ProArticle ',
                    StudyName=StudyName,
                    LatestDataOnly='Y',)
    pts.logout()
    root = ET.fromstring(PA)
    rock=[['GroupNumber','FemaleDosage','MaleDosage','Units']]
    for item in root.findall('ProArticleInfo'):
        for oo in item.findall('ProCompoundInfo'):
            for zz in oo.findall('ProGroupDosageInfo'):
                y = zz.find('GroupNumber').text
                rock.append([y,zz.find('FemaleDosage').text, zz.find('MaleDosage').text, zz.find('Units').text])
    df_PA = pd.DataFrame(rock[1:], columns=rock[0])
    for i in ['FemaleDosage','MaleDosage']:  # 修改数据类型
        df_PA[i] = df_PA[i].astype('float')
    return df_PA


def BW_AND_PA(BW_DF_G: pd.DataFrame, df_PA: pd.DataFrame):
    """
    输入 体重df, 给药的两个df, 
    返回  给药结果df
    """
    df_PA = df_PA.pivot_table(values=None, index=['GroupNumber'], columns='Units', aggfunc='max')  # 透视数据长变宽
    df_PA.columns = ['FDmL/kg', 'FDmg/kg', 'MDmL/kg', 'MDmg/kg'] # 修改列名称
    df_PA= df_PA.reset_index() # 重置索引才好排序合并
    df_PA['FnongD'] = df_PA.apply(lambda x: x['FDmg/kg']/x['FDmL/kg'], axis=1)
    df_PA['MnongD'] = df_PA.apply(lambda x: x['MDmg/kg']/x['MDmL/kg'], axis=1)
    df_PA = df_PA.merge(BW_DF_G, how='left', on='GroupNumber',)  # 合并数据给药和体重
    df_PA['Fml/kg'] = df_PA.apply(lambda x: x['FDmL/kg']*x['FBWSum'], axis=1)
    df_PA['Mml/kg'] = df_PA.apply(lambda x: x['MDmL/kg']*x['MBWSum'], axis=1)
    df_PA['Summl/kg'] = df_PA.apply(lambda x: x['Fml/kg']+x['Mml/kg'], axis=1)
    df_PA = df_PA[['GroupNumber','FDmg/kg','MDmg/kg','FDmL/kg','MDmL/kg','FnongD','MnongD','FBWSum','MBWSum','BWSum','Fml/kg','Mml/kg','Summl/kg']]  # 重新排序
    
    return df_PA


def find_Panel(proref_id):
    import cx_Oracle
    """传入专题编号 proref_id 查找返回cx_Oracle结果"""
    dsn = cx_Oracle.makedsn(sqlserver, 1521, service_name=service_name)
    dbc = cx_Oracle.connect(sqluser, sqlpw, dsn, encoding="UTF-8")
    cr = dbc.cursor()  #创建游标
    sql = """SELECT
                pm.PROREF_ID,
                pm.pmeapro_id,
                pm.collection_meas_proc_id,
                pm.prophs_id,
                pm.NAME,
                pm.sessions,
                pm.scheduled,
                NVL( m.NAME, m.NAME ),
                NVL( pn.NAME, pn.NAME ),
                pm.NO_PATH_EXCLUSIVE 
              FROM
                PRO_MEASUREMENT_PROCESS pm,
                PERSONNEL p,
                PHASE_NAMES pn,
                PRO_PHASE pp,
                MEASUREMENT m,
                ( SELECT MIN( TP ) AS MTP, pmeapro_id FROM PRO_MEASUREMENT_SCHEDULE GROUP BY pmeapro_id ) s 
              WHERE
                pm.person_id = p.person_id 
                AND pm.prophs_id = pp.prophs_id 
                AND pp.phsnam_id = pn.phsnam_id 
                AND pm.meadat_id = m.meadat_id 
                AND pm.pmeapro_id = s.pmeapro_id ( + ) 
                """
    studysql = r"AND pm.PROREF_ID ='{}'".format(proref_id)
    sql = sql + studysql
    cr.execute(sql) #sql 查询
    fetchall = cr.fetchall() #获取全部
    # cr.fetchone() #逐行获取，每次一条
    cr.close()
    dbc.close()
    return fetchall


def ProSchedule_Parameter(StudyName: str):
    """
    in: 专题编号
    ~~: 查询ProSchedule和ProParameter 等等 合并后导出list
    out: df
    """
    pts = PTS_RQ_RS(ptsAPIserverUrl, UserNameID, UserPassword, DeviceID)
    # 初始化类
    pts.run()
    # 启动类链接
    ProSchedule = pts.PTS_RQ('ProSchedule',
                    StudyName=StudyName,)
    ProParameter = pts.PTS_RQ('ProParameter',
                    StudyName=StudyName,
                    ActiveOnly='Y')
    AnimalPhase = pts.PTS_RQ('AnimalPhase',
                    StudyName=StudyName,
                    StudyAnimalOnly='Y')
    ProPhase = pts.PTS_RQ('ProPhase',
                StudyName=StudyName,)
    pts.logout()
    root_ProSchedule = ET.fromstring(ProSchedule)
    root_ProParameter = ET.fromstring(ProParameter)
    root_AnimalPhase = ET.fromstring(AnimalPhase)
    root_ProPhase = ET.fromstring(ProPhase)
    # ET.ElementTree(root_ProSchedule).write('root_ProSchedule.xml')

    """ df_ProSchedule """
    rock=[['ProtocolID','ProPhaseID', 'PhaseName','PmeaProID','MeasurementName','Day']]
    for item in root_ProSchedule.findall('ProScheduleInfo'):
        for getd in item.findall('ProScheduleDays'):
            for zz in getd.findall('Day'):
                # print(zz.text)
                try:
                    rock.append([item.find('ProtocolID').text, 
                                 item.find('ProPhaseID').text, 
                                 item.find('PhaseName').text, 
                                 item.find('PmeaProID').text,
                                 item.find('MeasurementName').text, 
                                 zz.text])
                except:
                    rock.append([item.find('ProtocolID').text, 
                                 item.find('ProPhaseID').text, 
                                 item.find('PhaseName').text, 
                                 item.find('PmeaProID').text,
                                 item.find('MeasurementName').text, 
                                 zz.text])
    df_ProSchedule = pd.DataFrame(rock[1:], columns=rock[0])  # 试验计划的DF
    df_ProSchedule = df_ProSchedule.loc[df_ProSchedule['MeasurementName'].isin(ABC_UC_list)]
    df_ProSchedule['PmeaProID'] = df_ProSchedule['PmeaProID'].astype('int64')  # 转换列为object 用于统一合并
    
    """ df_ProParameter """
    rock=[['PMeaProID','Abbrevation',]]
    for item in root_ProParameter.findall('ProParameterInfo'):
        rock.append([item.find(i).text for i in rock[0]])
    df_ProParameter = pd.DataFrame(rock[1:], columns=rock[0])  # 试验参数measure的df 
    df_g_pp = df_ProParameter.groupby('PMeaProID')
    PPIDAbbSum = pd.DataFrame([[name, ','.join(sorted(dfv['Abbrevation'].tolist()))] for name, dfv in df_g_pp], columns=['PmeaProID','AbbSum'])  # 合并参数到一行增加换行符每5pcs
    PPIDAbbSum.rename(columns={'PmeaProID':'PProID'}, inplace=True)
    PPIDAbbSum['PProID'] = PPIDAbbSum['PProID'].astype('int64')  # 转换列为object 用于统一合并
    PPIDAbbSum['AbbSum'] = PPIDAbbSum['AbbSum'].apply(lambda x: Urine_str if x in 'BLD,LEUk,TURB' else x)
    
    """ df_AnimalPhase """
    rock=[['ProPhsID','StudyAnimalNumber',]]
    for item in root_AnimalPhase.findall('AnimalPhaseInfo'):
        try:
            rock.append([item.find('ProPhsID').text, item.find('StudyAnimalNumber').text])
        except:
            rock.append([item.find('ProPhsID').text,  'N/A'])
    df_AnimalPhase = pd.DataFrame(rock[1:], columns=rock[0])  # 试验参数measure的df 
    df_AnimalPhase.drop(df_AnimalPhase[df_AnimalPhase.StudyAnimalNumber == 'N/A'].index, inplace=True)  # 删除满足条件行    
    df_AnimalPhase_g = df_AnimalPhase.groupby('ProPhsID')  # 对阶段分组
    Animal_PSANSum_count = pd.DataFrame([[phase, dfv['StudyAnimalNumber'].agg('count')] for phase, dfv in df_AnimalPhase_g], columns=['ProPhsID','count'])  # 计数用于合并
    Animal_PSANSum = pd.DataFrame([[phase, ','.join(sorted(dfv['StudyAnimalNumber'].tolist()))] for phase, dfv in df_AnimalPhase_g], columns=['ProPhsID','SAMSUM'])  # 新建立合并动物编号单元格
    Animal_PSANSum.rename(columns={'ProPhsID':'ProPhaseID'}, inplace=True)
    Animal_PSANSum_count.rename(columns={'ProPhsID':'ProPhaseID'}, inplace=True)
    # print(Animal_PSANSum)
    """ df_ProPhase """
    rock=[['ProtocolID', 'ProPhaseID',  'PhaseName', 'StartDate',]]
    for item in root_ProPhase.findall('ProPhaseInfo'):
        rock.append([item.find(i).text for i in rock[0]])
    df_ProPhase = pd.DataFrame(rock[1:], columns=rock[0])  # 试验参数measure的df 
    
    """get_Panel 从数据库中依据ProtocolID 获取Panel  df """
    proref_id = root_ProPhase.findall('ProPhaseInfo')[0].find('ProtocolID').text  # 从阶段获取专题编号对应的proref_id
    meas_proc = pd.DataFrame(find_Panel(proref_id),columns=['ProtocolID',
                                            'PmeaProID',
                                            'collection_meas_proc_id',
                                            'ProPhaseID',
                                            'NAME',
                                            'sessions',
                                            'scheduled',
                                            'MeasurementName',
                                            'PhaseName',
                                            'NO_PATH_EXCLUSIVE'])
    meas_proc = meas_proc.loc[meas_proc['MeasurementName'].isin(Meas_list)]  # 按条件筛选满足在Meas_list 的参数名称表
    meas_proc = meas_proc[['PmeaProID', 'collection_meas_proc_id','MeasurementName',]]  # 筛选需要的列并排序列名称
    meas_proc['collection_meas_proc_id'] = meas_proc['collection_meas_proc_id'].astype('int64')  # 转换列为object 用于统一合并
    meas_proc.rename(columns={'PmeaProID':'PProID','collection_meas_proc_id':'PmeaProID', 'MeasurementName':'Panel'}, inplace=True)  #  重名命列名称

    """and _ merge"""
    df = df_ProSchedule.merge(meas_proc,how='left',on='PmeaProID').merge(df_ProPhase, how='left').merge(PPIDAbbSum, how='left').merge(Animal_PSANSum).merge(Animal_PSANSum_count)
    
    def urine_find_nan(abbsumpanel):  #  用于根据尿沉渣查询nan 并替换
        if abbsumpanel['Panel'] == 'Urine Sediment' and pd.isna(abbsumpanel['AbbSum']):
            return Urine_Sediment_display
        else:
            return abbsumpanel['AbbSum'] 
    
    df['AbbSum'] = df.apply(urine_find_nan, axis=1)  # 替换空裂为尿沉渣
    df['StartDate'] = pd.to_datetime(df['StartDate'])  # 修改为时间类型
    df['Day'] = df['Day'].astype('int32')  # 先转换为整数
    df['Day'] = df['Day'].apply(lambda x: pd.Timedelta(days=x) - pd.Timedelta(days=1)) # 在转换为Timedelta days 当天减一
    df['Days'] = df['StartDate'] + df['Day']  # 相加得到具体日期datetime
    df['Days'] = df['Days'].apply(lambda x:time.mktime(x.timetuple()))
    df['Days'] = df['Days'].apply(lambda x:time.strftime('%Y-%m-%d',time.localtime(x)))  # 转换为时间字符串
    df = df[['Days','PhaseName','MeasurementName', 'Panel',  'AbbSum', 'SAMSUM', 'count']] # 选取需要的列
    #for  x ,y in df.groupby(['Days','PhaseName']):   # 分组写入到word
        #print(x,y)
    return df

if __name__ == "__main__":
    pts = PTS_RQ_RS(ptsAPIserverUrl, UserNameID, UserPassword, DeviceID)
    # 初始化类
    pts.run()
    # 启动类链接
    BW = pts.PTS_RQ('BodyWeight ',
                    StudyName='A2018022-T012-01',
                    StudyAnimalOnly='Y',
                    LatestDataOnly='Y',
                    PhaseName='Dosing Phase',
                    StartDateTime='01-NOV-2018 00:00:00',
                    EndDateTime='10-NOV-2019 00:00:00')
    # ET.ElementTree(ET.fromstring(BW)).write('BW.xml')
    PA = pts.PTS_RQ('ProArticle ',
                    StudyName='A2018022-T012-01',
                    LatestDataOnly='Y',)
    # ET.ElementTree(ET.fromstring(PA)).write('PA.xml')
    # print(BW, PA)
    ID = pts.PTS_RQ('IndirectDosing',
                   StudyName='A2018022-T012-01',)
    ET.ElementTree(ET.fromstring(ID)).write('ID.xml')
    pts.logout()
    StudyName = 'A2018022-T012-01'
    GBW=get_BodyWeight(StudyName) # 得到体重数据
    GPA=get_ProArticle(StudyName) # 得到给药数据
    BW, BW_DF_G = get_BW_Group(GBW)  # 计算并整形体重数据
    df_PA = BW_AND_PA(BW_DF_G, GPA)







