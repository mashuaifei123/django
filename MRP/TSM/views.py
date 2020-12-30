from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from TSM.models import tsmconfstatus, tsmreceiveinfo
from studys.models import studysinfo, studysprogressstatus
from django.core.serializers import serialize  # models 序列化json
from django.db.models import Sum
import datetime
from tools.dateTO import holiday


def confstatusfind(request):
    """
    查询TSM配制信息 以试验编号或者日期
    """
    column = ['专题编号', '项目负责人', '领药日期', '状态', '录入者','更新时间', '备注',]
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    pzdict = {0:r'<label class="label label-default">未完成</label>',
              1:r'<label class="label label-warning">已领取</label>',
              2:r'<label class="label label-warning">已配待领</label>',
              3:r'<label class="label label-success">已返还</label>'}
    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        if Fstudyid:
            q1.children.append(('studyno__studyno__icontains', Fstudyid))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('deliverydate__gte', start_date))
            q1.children.append(('deliverydate__lte', end_date))
    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询
    adate = tsmconfstatus.objects.filter(con)
    adate = adate.values('studyno__studyno',
                         'studyno__studydirector__username',
                         'deliverydate',
                         'status',
                         'operatedby__username',
                         'update_time',
                         'remarks',
                         )  #  查询数据
    adate = [[z['studyno__studyno']]+
             [z['studyno__studydirector__username']]+
             [z['deliverydate'].strftime('%Y-%m-%d')]+
             [pzdict.get(z['status'])]+
             [z['operatedby__username']]+
             [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')]+
             [z['remarks']] for z in adate]  # 列表生成数据格式
    context = {'tsmdata':adate, 'columnstitle': columns, }  # 传入到render变量参数用于被脚本调用
    return render(request, 'confstatus.html', context)

def confstatus(request):
    """
    供试品配制状态
    :param request:
    :return:
    """
    # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色 
    return render(request, 'confstatus.html',)

def inventoryinfofind(request):
    """
    查询供试品库存管理信息 以项目编号或者供试品名称/代号或阅片状态变更日期范围统计
    """
    column = ['项目编号', '供试品名称/代号', '状态', '状态变更日期', '录入者', '录入日期', '备注']
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    dt1 =  {0:r'<label class="label label-warning">预试样已接收</label>',
            1:r'<label class="label label-success">正式样已接收</label>',
            2:r'<label class="label label-info">已剩余处理</label>',
            3:r'<label class="label label-default">未知</label>',}
        # <label class="label label-success"> 内容字符串 </label>  颜色代码label
        # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色
    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR'
    if request.method == 'GET':
        Fproid = request.GET.get('q', None)  # 得到搜索关键词项目编号
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Ftestname = request.GET.get('tsn', None)  # 得到供试品名称

        if Fproid:
            q1.children.append(('projectno__projectnumber__icontains', Fproid))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('statusdate__gte', start_date))
            q1.children.append(('statusdate__lte', end_date))
        if Ftestname:
            q1.children.append(('nameorid__testtrarticlename__icontains', Ftestname))

    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询

    adate = tsmreceiveinfo.objects.filter(con)  # 拼接的Q查询返回Queryset 
    adate = adate.values('projectno__projectnumber',
                         'nameorid__testtrarticlename',
                         'status',
                         'statusdate',
                         'operatedby__username',
                         'update_time',
                         'remarks',
                         )  #  查询数据
    adate = [[z['projectno__projectnumber']]+
             [z['nameorid__testtrarticlename']]+
             [dt1.get(z['status'])]+
             [z['statusdate'].strftime('%Y-%m-%d')]+
             [z['operatedby__username']]+
             [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')]+
             [z['remarks']] for z in adate]  # 列表生成数据格式
    context = {'invdata':adate, 'columnstitle': columns, }  # 传入到render变量参数用于被脚本调用
    return render(request, 'inventoryinfo.html', context)

def inventoryinfo(request):
    """
    显示7日内阅片信息
    :param request:
    :return:
    """
    
    return render(request, 'inventoryinfo.html',)

