from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
import cx_Oracle
from tools.config import sqlserver, sqluser, sqlpw, service_name, appserverservlet
# Create your views here.


def findanimailpts(studynum, pretestnum):
    """传入专题编号，或者pretestid 查找返回cx_Oracle结果"""
    dsn = cx_Oracle.makedsn(sqlserver, 1521, service_name=service_name)
    dbc = cx_Oracle.connect(sqluser, sqlpw, dsn, encoding="UTF-8")
    cr = dbc.cursor()  #创建游标
    sql = """SELECT
                SR.STUDY_NUMBER,
                SA.ANIMAL_ID,
                SA.STDANM_ID,
                SA.DATE_TIME_ENTERED,
                GA.ASSIGN_DATE,
                A.SEX,
                SA.PRETEST_NUMBER,
                decode(
                    sa.subgroup_number,
                    NULL,
                    ga.subgroup_number,
                decode( ga.subgroup_number, NULL, sa.subgroup_number )) AS SUBGROUP_NUMBER,
                GA.STUDY_ANIMAL_NUMBER,
                PGN.GROUP_NUMBER,
                SP.NAME AS SPECIES,
                ST.NAME AS STRAIN,
                SR.TYPES 
            FROM
                STUDY_ANIMAL SA,
                ANIMAL A,
                GROUP_ASSIGNMENT GA,
                PRO_GROUP_NAMES PGN,
                PRO_GRP_SPEC PGS,
                PRO_REFERENCE SR,
                STRAIN ST,
                SPECIES SP 
            WHERE
                PGN.PGRPNM_ID ( + ) = PGS.PGRPNM_ID 
                AND PGS.PROGRP_ID ( + ) = GA.PROGRP_ID 
                AND A.LATEST = 'Y' 
                AND SA.ANIMAL_ID = A.ANIMAL_ID 
                AND SA.STDANM_ID = GA.STDANM_ID ( + ) 
                AND SA.PROREF_ID = SR.PROREF_ID 
                AND SP.SPECIE_ID = SR.SPECIE_ID 
                AND ST.STRAIN_ID = A.STRAIN_ID 
                AND SA.DATE_TIME_ENTERED >= to_date(
                '2019-01-01 00:00:00',
                'yyyy-mm-dd hh24:mi:ss' 
                )"""
    if pretestnum:  # 拼接sql语句
        pretestsql = r" AND SA.PRETEST_NUMBER = '{}'".format(pretestnum)
        sql = sql + pretestsql
    if studynum:
        studysql = r" AND SR.STUDY_NUMBER LIKE '%{}%'".format(studynum)
        sql = sql + studysql
    cr.execute(sql) #sql 查询
    fetchall = cr.fetchall() #获取全部
    # cr.fetchone() #逐行获取，每次一条
    cr.close()
    dbc.close()
    return fetchall

def animalid(request):
    ''' 动物详情直接查询来自oracle- pathtox数据库  '''
    column=    ['专题编号',
                'PTS动物ID',
                '性别',
                'PretestID',
                'Study动物ID',
                'SPECIES',
                '数据更新日期',
                ]
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    # [r'<a href=http://74pracapp.kunshan.cti-cert.com/74pracapp/servlet/AnimalHistory?pts_animal_id={}>{}</a>'.format(z[1], z[1])]
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        FPID = request.GET.get('PID', None)  # 得到搜索PretestID编号
        if Fstudyid or FPID:  # 判断是否传入数据
            if len(Fstudyid) < 18 or len(FPID) < 15:  # 长度检查防注入
                adate = findanimailpts(studynum=Fstudyid, pretestnum=FPID)
                adate = [[z[0]]+[r'<a href=http://{}/servlet/AnimalHistory?pts_animal_id={} target="_blank">{}</a>'.format(appserverservlet,z[1], z[1])]+
                        [z[5]]+[z[6]]+[z[8] if z[8] else 'N/A']+[z[10]]+
                        [z[3].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]  # 列表生成数据格式
        else:  # 没有传入参数返回空
            adate = []
    context = {'animaldata': adate ,'columnstitle': columns,}
    return render(request, 'animalid.html', context)

def F_1F(request):
    ''' 1F入口 '''
    context = {'tdata':12}
    return render(request, '1F.html', context)

def F_2F(request):
    ''' 2F入口 '''
    context = {'tdata':12}
    return render(request, '2F.html', context)

def F_3F(request):
    ''' 3F入口 '''
    context = {'tdata':12}
    return render(request, '3F.html', context)

def F_4F(request):
    ''' 4F入口 '''
    context = {'tdata':12}
    return render(request, '4F.html', context)