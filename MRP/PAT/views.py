from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
import pandas as pd
from django.db.models import Count, Min, Max, Sum
from tools.sddayset import dayset  # 导入日程计划日期关联关系
from studys.models import studysinfo, studyproperty, studysprogressstatus, sdmanager, phase, projectinfo
from assets.models import testsystem
from PAT.models import patinfo
from tools.dateTO import holiday
import datetime
from django.contrib.auth.decorators import login_required  # 确认是否已经登入装装饰器
from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.models import Permission, ContentType, User  # 系统默认的模块 权限和用户模块



# @login_required() # 登入才能查看
# @permission_required('PAT.view_patinfo', raise_exception=True) # 只有有相应权限才可以查看
def info(request):
    ''' 病理查询入口 '''
    """
    在 views里取值是这样的
    request.user.username
    而在模板页面取值是这样的：
    {{request.user}}
    判断是否通过验证是这样的
    {% if request.user.is_authenticated %}
    """
    # usern = request.user.username
    # userid = User.objects.get(username=usern)  # 注意用户模型属于contrib.auth.models User
    # print(userid.get_all_permissions())  查询用户所有权限
    # print(userid.get_group_permissions())  查询用户组所有权限
    ts = testsystem.objects.all().values_list('id', 'testsystemname')
    tdata = [{'id':o[0], 'text':o[1]} for o in ts]  # 字典生成式加列表
    context = {'tdata':tdata}
    return render(request, 'patinfo.html', context)


"""
def test():
    dic = {'id':123,'name':'alex'}
    models.UserInfo.objects.filter(**dic)
    if mobile:
        data_list = data_list.filter(mobile=mobile)
    if id_no:
        data_list = data_list.filter(id_no=id_no)
    # 传入条件进行查询:

    q1 = Q()
    q1.connector = 'OR'              #连接方式
    q1.children.append(('id', 1))
    q1.children.append(('id', 2))
    q1.children.append(('id', 3))
        
    models.Tb1.objects.filter(q1)
    # 合并条件进行查询:
    con = Q()

    q1 = Q()
    q1.connector = 'OR'
    q1.children.append(('id', 1))
    q1.children.append(('id', 2))
    q1.children.append(('id', 3))

    q2 = Q()
    q2.connector = 'OR'
    q2.children.append(('status', '在线'))

    con.add(q1, 'AND')
    con.add(q2, 'AND')

    models.Tb1.objects.filter(con)
    if request.method=="POST":
        gender=request.POST.get("gender")
        AH=request.POST.getlist("aihao")
"""

def infofind(request):
    ''' 病理查询页面 '''
    ts = testsystem.objects.all().values_list('id', 'testsystemname')  #  试验系统
    tdata = [{'id':o[0], 'text':o[1]} for o in ts]  # 字典生成式加列表
    sumcolumn = ['项目','动物数量']
    sumcolumns = [{"title": x} for x in sumcolumn]  # 拼接为前端需要样式字典
    column=    ['解剖日期',
                '周',
                '专题编号',
                '专题负责人',
                '试验系统',
                '阶段',
                '解剖动物数量',
                '制片状态',
                '制片日期',
                '阅片状态',
                '阅片日期',
                '参与人员',
                '备注',
                '更新时间'
                ]
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    zpdict = {0:r'<label class="label label-default">未开始</label>',
              1:r'<label class="label label-warning">制片中</label>',
              2:r'<label class="label label-success">制片完成</label>'}
    rsdict = {0:r'<label class="label label-default">未开始</label>',
              1:r'<label class="label label-warning">阅片中</label>',
              2:r'<label class="label label-success">阅片完成</label>'}

    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Fts = request.GET.getlist('ts', None)  # 得到试验系统列表
        Fzp = request.GET.getlist('zp', None)  # 得到制片列表
        Frs = request.GET.getlist('rs', None)  # 得到阅片列表

        if Fstudyid:
            q1.children.append(('studyno__studyno__studyno__icontains', Fstudyid))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('studyno__dates__gte', start_date))
            q1.children.append(('studyno__dates__lte', end_date))
        if Fts:
            for x in Fts:
                q2.children.append(('studyno__studyno__testsystem', x))
        if Fzp:
            for x in Fzp:
                q2.children.append(('slidespreparationstatus', x))
        if Frs:
            for x in Frs:
                q2.children.append(('histopathologystatus', x))

    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询

    adate = patinfo.objects.filter(con)  # 拼接的Q查询返回Queryset 
    bl = []
    for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装 参与人员
        iddate = list(patinfo.objects.filter(pk=pk).values_list('observedby__username'))
        ab = [','.join([y for y in [','.join(x) for x in iddate]])]
        bl.append(ab)
    sumdata = adate.aggregate(anmailnums=Sum('studyno__anmailnum'))  # 对查询数据进行求和
    sumdata = [['总计'] + list(sumdata.values())] # 和值
    adate = adate.values('studyno__dates',
                         'studyno__studyno__studyno',
                         'studyno__studyno__studydirector__username',
                         'studyno__studyno__testsystem__testsystemname',
                         'studyno__phasename__phasename',
                         'studyno__anmailnum',
                         'slidespreparationstatus',
                         'slidesdate',
                         'histopathologystatus',
                         'histodate',
                         'remarks',
                         'update_time',)  #  查询数据
    adate = [[z['studyno__dates'].strftime('%Y-%m-%d')]+
             [z['studyno__studyno__studyno']]+
             [z['studyno__studyno__studydirector__username']]+
             [z['studyno__studyno__testsystem__testsystemname']]+
             [z['studyno__phasename__phasename']]+
             [z['studyno__anmailnum']]+
             [zpdict.get(z['slidespreparationstatus'])]+
             [z['slidesdate'].strftime('%Y-%m-%d')]+
             [rsdict.get(z['histopathologystatus'])]+
             [z['histodate'].strftime('%Y-%m-%d')]+
             [z['remarks']]+
             [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]  # 列表生成数据格式
    for i in range(len(bl)):  # 拼接值班人员和数据表
        adate[i][0:1] = list(holiday(adate[i][0]))  # 修改日期图示
        adate[i][11:11] = bl[i]

    context = {'tdata':tdata, 'patdata': adate, 'columnstitle': columns,  'sumdata': sumdata,  'sumcolumns':sumcolumns }
    return render(request, 'patinfo.html', context)