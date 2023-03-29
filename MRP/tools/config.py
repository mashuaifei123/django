'''pristima 数据库地址配置'''
sqlserver = ".kunshan.cti-cert.com"
service_name = ".kunshan.cticert.com"
appserverservlet =  r'.kunshan.cti-cert.com/74papp'
sqluser = "PTS_Server"
sqlpw = "pts_password"

'''pristima API 服务器地址配置'''
ptsAPIserverUrl = 'http://.kunshan.cti-cert.com/74papi/servlet/PtsAPIServlet'
ptsUserNameID = ''
ptsUserPassword = ''
ptsDeviceID = ''

'''临检申请单函数参数设定'''
# 仪器过滤列表
Meas_list = ['Blood Biochemistry (cobas 6000)', 'Urine Analysis (AX-4030)', 'Coagulation (CA-7000)', 'Hematology (ADVIA 2120i)', 'BD FACSCalibur', 'Urine Sediment']
# 尿液或者采血名称过滤列表
Urine_str = '☑常规检查Routine Examination'
Urine_Sediment_display = '☑尿沉渣Urinary Sediment'
ABC_UC_list = ['Animal Blood Collection', 'Urine Collection']
outputfilepath = r'\\fileserver\部门共享\SetsOut'
