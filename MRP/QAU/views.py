from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
import pandas as pd
from django.db.models import Count, Min, Max, Sum
from tools.sddayset import dayset  # 导入日程计划日期关联关系
from QAU.models import checkingplan, qauusersinfo
from tools.dateTO import holiday
import datetime
from django.contrib.auth.decorators import login_required  # 确认是否已经登入装装饰器
from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.models import Permission, ContentType, User  # 系统默认的模块 权限和用户模块



@login_required() # 登入才能查看
@permission_required('QAU.view_checkingplan', raise_exception=True) # 只有有相应权限才可以查看
def checkplan(request):
    pe = qauusersinfo.objects.all().values_list('id', 'username')
    pedata = [{'id':o[0], 'text':o[1]} for o in pe]  # 字典生成式加列表
    context = {'pedata':pedata}
    return render(request, 'checkplan.html', context)

@login_required() # 登入才能查看
@permission_required('QAU.view_checkingplan', raise_exception=True) # 只有有相应权限才可以查看
def checkplanfind(request):
    ''' 病理查询页面 '''
    pe = qauusersinfo.objects.all().values_list('id', 'username')
    pedata = [{'id':o[0], 'text':o[1]} for o in pe]  # 字典生成式加列表
    column=    ['检查日期',
                '周',
                '专题编号',
                '检查项目',
                '责任人',
                '备注',
                '更新时间'
                ]
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典

    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Fpe = request.GET.getlist('pe', None)  # 得到人员

        if Fstudyid:
            q1.children.append(('studyno__studyno__icontains', Fstudyid))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('checkdate__gte', start_date))
            q1.children.append(('checkdate__lte', end_date))
        if Fpe:
            for x in Fpe:
                q2.children.append(('person', x))
    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询
    adate = checkingplan.objects.filter(con)  # 拼接的Q查询返回Queryset 
    bl = []
    for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装 参与人员
        iddate = list(checkingplan.objects.filter(pk=pk).values_list('checkitem__checkname'))
        ab = [','.join([y for y in [','.join(x) for x in iddate]])]
        bl.append(ab)
    adate = adate.values('checkdate',
                         'studyno__studyno',
                         'person__username',
                         'remarks',
                         'update_time',)  #  查询数据
    adate = [[z['checkdate'].strftime('%Y-%m-%d')]+
             [z['studyno__studyno']]+
             [z['person__username']]+
             [z['remarks']]+
             [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]  # 列表生成数据格式
    for i in range(len(bl)):  # 拼接值班人员和数据表
        adate[i][0:1] = list(holiday(adate[i][0]))  # 修改日期图示
        adate[i][3:3] = bl[i]

    context = {'pedata':pedata, 'qaucheckdata': adate, 'columnstitle': columns}
    return render(request, 'checkplan.html', context)