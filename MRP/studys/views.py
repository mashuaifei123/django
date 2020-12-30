from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
import pandas as pd
from django.db.models import Count, Min, Max
from .forms import NameForm, RegisterForm
from tools.sddayset import dayset  # 导入日程计划日期关联关系
from tools.colo import color  # 导入颜色板
from studys.models import studysinfo, studyproperty, studysprogressstatus, sdmanager, studydays, studyitem, itemindept
import datetime
from django.contrib.auth.decorators import login_required  # 确认是否已经登入装装饰器
from django.contrib.auth.decorators import permission_required
from CMDB.settings import BASE_DIR
from assets.models import deptinfo

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
    return render(request, 'studys/test.html', {'form': form})


def studydaysview(request):
    """
    日程
    :param request:
    :return:
    """
    C_list = ['专题编号','阶段', '日程日期', '期/天', '试验操作', 'Pro_Code_b' ]
    newdays = models.StudyDays.objects.filter(Study_No__Study_No='A2018').annotate(Count('Pristima_phase__Phase_name')).values_list('Study_No__Study_No', 'Pristima_phase__Phase_name', 'date_days', 'days_num', 'Program__Pro_name', 'Pro_Code_b')
    print(newdays)
    '''
    assets = models.StudyDays.objects.select_related('Study_No', 'Pristima_phase', 'Program') \
                .filter(Study_No__Study_No='A2018') \
                .values_list('Study_No__Study_No', 'Pristima_phase__Phase_name', 'date_days', 'days_num', 'Program__Pro_name', 'Pro_Code_b')
    df = pd.DataFrame(list(assets), columns=C_list)
    '''
    # assets = get_object_or_404(models.StudyInfo)
    return render(request, 'studys/studydays.html')


def study_daysinfo(request, studynum):
    """
    根据试验编号进行查询返回配置的信息
    通过多类的条件查询一类的数据：
    一类名.objects.filter(多类名小写__多类属性名__条件名)   # 关联属性没有定义在该类中,所以用多类名小写
    通过一类的条件查询多类的数据：
    多类名.objects.filter(关联属性__一类属性名__条件名)   # 关联属性定义在该类中,所以直接用关联属性名
    """
    assets = models.StudyDays.objects.filter(Study_No__Study_No=studynum)
    return render(request, 'studys/studydays.html', locals())


def studysGantt(request):
    """
    根据试验编号进行查询返回配置的信息
    通过多类的条件查询一类的数据：
    一类名.objects.filter(多类名小写__多类属性名__条件名)   # 关联属性没有定义在该类中,所以用多类名小写
    通过一类的条件查询多类的数据：
    多类名.objects.filter(关联属性__一类属性名__条件名)   # 关联属性定义在该类中,所以直接用关联属性名
    """
    
    # assets = models.StudyDays.objects.filter(Study_No__Study_No=studynum)
    return render(request, 'studys/studyGantt.html', locals())



@login_required() # 登入才能查看
@permission_required('studys.view_studydays', raise_exception=True) # 只有有相应权限才可以查看
def studyplancreate(request):
    '''增加专题日程,原理为读取excel文件中的专题编号.如果存在就删除在增加如果不存在就增加.'''
    excelFile = r'{}\tools\studyplan\plan.xlsx'.format(BASE_DIR)
    # 获取专题编号
    dfsn = pd.DataFrame(pd.read_excel(excelFile, skiprows=4, skipfooter=5))
    try:
        studyno = dfsn.columns[0].split('：')[1]
    except:
        studyno = dfsn.columns[0].split(':')[1]
    df = pd.DataFrame(pd.read_excel(excelFile, header=0, skiprows=7))  # 第六行开始
    # 获取备注
    try:
        remarks = df.iat[-3, 0].split('：')[1]
    except:
        remarks = df.iat[-3, 0].split(':')[1]
    df = df.drop(df.index[-3:], axis=0,)  # 删除倒数三行
    df = df.drop(df.index[0], axis=0,)  # 删除第0行
    df.iloc[:, 0:6] = df.iloc[:, 0:6].fillna(method='ffill', axis=0)  # 替换缺失值nan用上面的值
    df.iloc[:, 3] = df.iloc[:, 3].astype(int)  # 强制转换为int整数
    vars_list = df.columns[:6]  # 标示变量列名称不转换的列
    item_list = df.columns[6:]  # 需要转换的列名称
    df = df.melt(id_vars=vars_list, value_vars=item_list, var_name='试验操作', value_name='操作内容')  # 转置宽转长
    df.dropna(axis=0, how='any', inplace=True)  # 删除空值行
    df = df.reset_index()  # 重置索引
    df = df.iloc[:, 1:]  # 排除第一列的内容
    df_list = df.values.tolist()
    try:
        quetyset = studydays.objects.filter(studyno__studyno=studyno)
        if quetyset:
            print('删除数据{}成功'.format(studyno))
        quetyset.delete()  # 用来删除在日程表找到的已经存在的专题编号的相关记录
    except:
        pass
    try:
        infolist = set()
        quetyset = studysinfo.objects.filter(studyno=studyno)
        for a, b, c, d, e, o, f, g in df_list:
            if not studyitem.objects.filter(itemname=f):
                infolist.add(f)
        if not quetyset:
            print('没有找到这个专题编号')
            info = '导入失败日志见后台-没有找到这个{}专题编号,请新建专题编号'.format(studyno)
        if infolist:
            print('没有找到这些试验名称请检查增加')
            info = '导入失败日志见后台-没有找到这些<{}>试验名称请核实增加'.format('|'.join(infolist))
        else:
            for pk in [x.id for x in quetyset]:  # 根据ID  PK 查询
                sid = studysinfo.objects.get(pk=pk)
                for a, b, c, d, e, o, f, g in df_list:
                    # print(int(studyitem.objects.filter(itemname=f)[0].id))
                    studydays.objects.create(studyno=sid, 
                                                ptsdays = a,
                                                datedays = b,
                                                weekday = c,
                                                weekno = d,
                                                phasedays = e,
                                                sex = o,
                                                itemname = studyitem.objects.get(pk=studyitem.objects.filter(itemname=f)[0].id),
                                                itemactive = g,
                                                remarks = remarks)
            print('创建{}日程成功'.format(sid))
            info = '导入{}成功日志见后台'.format(excelFile)
    except:
        print('失败')
        info = '导入失败请联系管理员查看日志'
    return render(request, 'studyplancreate.html', {'info': info})

def studyplan(request):
    '''专题日程查询入口'''
    itemqs = studyitem.objects.all()
    itemdata = [{'id':o.id, 'text':o.itemname} for o in itemqs]  # 字典生成式加列表 生成前端用的试验操作itemname
    deptqs = deptinfo.objects.all()
    deptdata = [{'id':o.id, 'text':o.deptname} for o in deptqs]  # 字典生成式加列表 生成前端用的部门
    context = {'itemdata':itemdata, 'deptdata':deptdata}
    return render(request, 'studyplan.html', context)

def studyplanfind(request):
    '''专题日程查询'''
    column = ['专题编号', 'SD', '日程', '日期', '星期', '周', '试验阶段', '性别', '试验操作', '操作内容', '备注', '更新时间']
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    itemqs = studyitem.objects.all()
    itemdata = [{'id':o.id, 'text':o.itemname} for o in itemqs]  # 字典生成式加列表 生成前端用的试验操作itemname
    deptqs = deptinfo.objects.all()
    deptdata = [{'id':o.id, 'text':o.deptname} for o in deptqs]  # 字典生成式加列表 生成前端用的部门
    colordict = dict(zip(set(x.itemname for x in itemqs), set(color)))  # 生成字典和颜色配合用于生成前端带颜色的日历
    
    """ 合并判断查询部分"""
    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fsd = request.GET.get('sd', None)  # 得到部分人名称关键字
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Fsex = request.GET.getlist('sex', None) # 得到性别
        Fitem = request.GET.getlist('item', None)  # 得到部项目名称关键字id
        Fdept = request.GET.get('dept', None)  # 得到部们id
        
        if Fstudyid:  # 查询专题编号
            q1.children.append(('studyno__studyno__icontains', Fstudyid))
        if Fsd:  # 查询SD
            q1.children.append(('studyno__studydirector__username__icontains', Fsd))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('datedays__gte', start_date))
            q1.children.append(('datedays__lte', end_date))
        if Fsex:  # 查询项目
            for x in Fsex:
                q2.children.append(('sex', x))
            Fsex = ','.join(Fsex)
        if Fitem:  # 查询项目
            Fitems = [studyitem.objects.filter(id=x)[0].itemname for x in Fitem]
            Fitems = ','.join(Fitems)  # 返回实验操作提交的合集
            for x in Fitem:
                q2.children.append(('itemname', x))
        if Fdept: # 查询符合部门分组的试验操作
            Fdepts = deptinfo.objects.get(pk=Fdept).deptname
            Fitemslist = itemindept.objects.filter(deptname=Fdept).values_list('deptitem')
            for x in Fitemslist:
                q2.children.append(('itemname', x))

        """ 判断 查询参数部分 """
        Fstudyid = Fstudyid if Fstudyid else 'N/A'
        Fsd = Fsd if Fsd else 'N/A'
        Fdate = Fdate if Fdate else 'N/A'
        Fitems = Fitems if Fitem else 'N/A'
        Fsex = Fsex if Fsex else 'N/A'
        Fdept = Fdepts if Fdept else 'N/A'
        sno = '查询参数    专题编号:{};  专题负责人:{};  时间范围:{};  性别:{}; 试验操作:{}; 部门:{}'.format(Fstudyid, Fsd, Fdate, Fsex, Fitems, Fdept)

    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询
    adate = studydays.objects.filter(con).order_by('datedays')  # 拼接的Q查询返回Queryset order_by 排序

    """开始执行查询"""
    adate = adate.values('studyno__studyno', 'studyno__studydirector__username', 'ptsdays', 'datedays', 'weekday', 'weekno', 'phasedays', 'sex','itemname__itemname', 'itemactive', 'remarks', 'update_time',)
    evedata =  [{'title'         : x['itemname__itemname'],
                'start'          : x['datedays'].strftime('%Y-%m-%d'),
                'url'            : 'search?q={}&sd=&date=&item={}'.format(x['studyno__studyno'], studyitem.objects.filter(itemname=x['itemname__itemname'])[0].id),
                'backgroundColor': colordict.get(x['itemname__itemname']),
                'borderColor'    : colordict.get(x['itemname__itemname']),
                'description'    : x['studyno__studyno']} for x in adate] # 生成前端需要的日历格式字典数据 注意URL 调用关系部分
    adate = [[z['studyno__studyno']]+
            [z['studyno__studydirector__username']]+
            [z['ptsdays']]+
            [z['datedays'].strftime('%Y-%m-%d')]+
            [z['weekday']]+
            [z['weekno']]+
            [z['phasedays']]+
            [z['sex']]+
            [z['itemname__itemname']]+
            [z['itemactive']]+
            [z['remarks']]+
            [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]
    context = {'studydata':adate, 'columnstitle': columns, 'eventd':evedata, 'itemdata':itemdata, 'deptdata':deptdata, 'sno':sno}  # 传入到render变量参数用于被脚本调用
    return render(request, 'studyplan.html', context)


def sdmanagerinfo(request):
    ''' 毒理部专题进展查询入口 '''
    return render(request, 'sdmanager.html')

def sdmanagerfind(request):
    ''' 毒理部专题进展管理查询页面 '''
    d = datetime.timedelta  # 减去的时间函数(day=1)
    ds = datetime.datetime.strptime  # 把字符串转换为datetime.datetime格式
    column =   ['项目编号',
                '供试品名称/代号',
                '专题编号',
                'SD',
                '方案生效日期',
                '给药开始日期',
                '给药结束日期',
                '试验结束日期',
                '进展',
                '大动物资料接收日期',
                '骨髓报告日期',
                '病理报告初稿日期',
                'TK/ADA报告日期',
                '总结报告初稿日期',
                '给委托方初稿/返还',
                '资料递交QA日期',
                'QA返还日期',
                '终版报告签字日期',
                '归档日期',
                '备注',
                '更新时间'
                ]
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    lebp = r'<label class="label label-success">'
    lebw = r'<label class="label label-warning">'
    leb2 = r'</label>'

    def thc(date1, date2):  # 输入时间返回带判断颜色的网页代码
        date1 = datetime.datetime.date(date1)
        if date2: # 传入的date2是非空的
            rd = date2.strftime('%Y-%m-%d')
            if date1 >= date2:
                return '{}{}{}'.format(lebp, rd, leb2)
            if date1 < date2:
                return '{}{}{}'.format(lebw, rd, leb2)
        else:  # 传入的date2是none 返回空
            return r'<label class="label label-default">___</label>'

    def jh(date1, date2, daysdate):  #计划调用加函数
        if date2:
            return (date1 + d(days=date2)).strftime('%Y-%m-%d')
        else:
            return (date1 + d(days=daysdate)).strftime('%Y-%m-%d')
    
    def yuj(ysd, dyd, dys, mrd, mrs, syjsd):  #预计调用的函数
        """in: ysd  原始数据
               dyd  定义计划天
               dys  定义预计数据结合原始数据的数据
               mrd  默认计划天
               mrs  默认计划预计数据结合原始数据的数据天
               syjsd 试验结束日期
           out: 格式化后的计算结果日期
        """
        if ysd:  #原始数据存在
            if dys:  #定义预计天是否存在
                return (ysd+d(days=dys)).strftime('%Y-%m-%d')
            else: #不存在就返回默认预计天
                return (ysd+d(days=mrs)).strftime('%Y-%m-%d')
        else:
            if dyd: #定于预计天是否存在 返回实验结束日期加定义预计天
                return (syjsd+d(days=dyd)).strftime('%Y-%m-%d')
            else:
                return (syjsd+d(days=mrd)).strftime('%Y-%m-%d')


    def toplan1(adate):  # 返回计划数据
        adate = adate.values('studyno__projectno__projectnumber',
                            'studyno__projectno__testtrarticlename__testtrarticlenumber',
                            'studyno__studyno',
                            'studyno__studydirector__username',
                            'studyno__studysprogressstatus__initiationdate',
                            'studyno__studysprogressstatus__firstexposuredate',
                            'studyno__studysprogressstatus__lastexposuredate',
                            'studyno__studysprogressstatus__testenddate',
                            'biganimald',
                            'bmreportd',
                            'patreportd',
                            'tkadareportd',
                            'summaryreportd',
                            'returnd',
                            'dateqad',
                            'qareturnd',
                            'Finalsignatured',
                            'archived',
                            'remarks',
                            'update_time',
                            'studyno__studyplansetting__ddwzljsd',
                            'studyno__studyplansetting__gsbgd',
                            'studyno__studyplansetting__patd',
                            'studyno__studyplansetting__tkadad',
                            'studyno__studyplansetting__sumrepd',
                            'studyno__studyplansetting__wtfcfd',
                            'studyno__studyplansetting__sdwtfcfd',
                            'studyno__studyplansetting__sendqad',
                            'studyno__studyplansetting__sdsendqad',
                            'studyno__studyplansetting__qared',
                            'studyno__studyplansetting__sdqareturnd',
                            'studyno__studyplansetting__finalrd',
                            'studyno__studyplansetting__sdfinalrd',
                            'studyno__studyplansetting__activedd',
                            'studyno__studyplansetting__sdactivedd',)
        adate = [[z['studyno__projectno__projectnumber']]+
                [z['studyno__projectno__testtrarticlename__testtrarticlenumber']]+
                [z['studyno__studyno']]+
                [z['studyno__studydirector__username']]+
                [z['studyno__studysprogressstatus__initiationdate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__firstexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__lastexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__testenddate'].strftime('%Y-%m-%d')]+
                ['计划']+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__ddwzljsd'], dayset['ddwzljsd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__gsbgd'], dayset['gsbgd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__patd'], dayset['patd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__tkadad'], dayset['tkadad'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__sumrepd'], dayset['sumrepd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__wtfcfd'], dayset['wtfcfd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__sendqad'], dayset['sendqad'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__qared'], dayset['qared'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__finalrd'], dayset['finalrd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__activedd'], dayset['activedd'])]+
                [z['remarks']]+
                [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]
        return adate
    
    def expected1(adate):  # 返回 预计数据
        adate = adate.values('studyno__projectno__projectnumber',
                            'studyno__projectno__testtrarticlename__testtrarticlenumber',
                            'studyno__studyno',
                            'studyno__studydirector__username',
                            'studyno__studysprogressstatus__initiationdate',
                            'studyno__studysprogressstatus__firstexposuredate',
                            'studyno__studysprogressstatus__lastexposuredate',
                            'studyno__studysprogressstatus__testenddate',
                            'biganimald',
                            'bmreportd',
                            'patreportd',
                            'tkadareportd',
                            'summaryreportd',
                            'returnd',
                            'dateqad',
                            'qareturnd',
                            'Finalsignatured',
                            'archived',
                            'remarks',
                            'update_time',
                            'studyno__studyplansetting__ddwzljsd',
                            'studyno__studyplansetting__gsbgd',
                            'studyno__studyplansetting__patd',
                            'studyno__studyplansetting__tkadad',
                            'studyno__studyplansetting__sumrepd',
                            'studyno__studyplansetting__wtfcfd',
                            'studyno__studyplansetting__sdwtfcfd',
                            'studyno__studyplansetting__sendqad',
                            'studyno__studyplansetting__sdsendqad',
                            'studyno__studyplansetting__qared',
                            'studyno__studyplansetting__sdqareturnd',
                            'studyno__studyplansetting__finalrd',
                            'studyno__studyplansetting__sdfinalrd',
                            'studyno__studyplansetting__activedd',
                            'studyno__studyplansetting__sdactivedd',)
        adate = [[z['studyno__projectno__projectnumber']]+
                [z['studyno__projectno__testtrarticlename__testtrarticlenumber']]+
                [z['studyno__studyno']]+
                [z['studyno__studydirector__username']]+
                [z['studyno__studysprogressstatus__initiationdate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__firstexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__lastexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__testenddate'].strftime('%Y-%m-%d')]+
                ['预计']+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__ddwzljsd'], dayset['ddwzljsd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__gsbgd'], dayset['gsbgd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__patd'], dayset['patd'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__tkadad'], dayset['tkadad'])]+
                [jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__sumrepd'], dayset['sumrepd'])]+
                [yuj(z['summaryreportd'], z['studyno__studyplansetting__wtfcfd'], z['studyno__studyplansetting__sdwtfcfd'], dayset['wtfcfd'], dayset['sdwtfcfd'], z['studyno__studysprogressstatus__testenddate'])]+
                [yuj(z['returnd'], z['studyno__studyplansetting__sendqad'], z['studyno__studyplansetting__sdsendqad'], dayset['sendqad'], dayset['sdsendqad'], z['studyno__studysprogressstatus__testenddate'])]+
                [yuj(z['dateqad'], z['studyno__studyplansetting__qared'], z['studyno__studyplansetting__sdqareturnd'], dayset['qared'], dayset['sdqareturnd'], z['studyno__studysprogressstatus__testenddate'])]+
                [yuj(z['qareturnd'], z['studyno__studyplansetting__finalrd'], z['studyno__studyplansetting__sdfinalrd'], dayset['finalrd'], dayset['sdfinalrd'], z['studyno__studysprogressstatus__testenddate'])]+
                [yuj(z['Finalsignatured'], z['studyno__studyplansetting__activedd'], z['studyno__studyplansetting__sdactivedd'], dayset['activedd'], dayset['sdactivedd'], z['studyno__studysprogressstatus__testenddate'])]+
                [z['remarks']]+
                [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]
        return adate

    def actual1(adate): # 返回实际 数据
        nul = r'<label class="label label-default">___</label>'
        adate = adate.values('studyno__projectno__projectnumber',
                            'studyno__projectno__testtrarticlename__testtrarticlenumber',
                            'studyno__studyno',
                            'studyno__studydirector__username',
                            'studyno__studysprogressstatus__initiationdate',
                            'studyno__studysprogressstatus__firstexposuredate',
                            'studyno__studysprogressstatus__lastexposuredate',
                            'studyno__studysprogressstatus__testenddate',
                            'biganimald',
                            'bmreportd',
                            'patreportd',
                            'tkadareportd',
                            'summaryreportd',
                            'returnd',
                            'dateqad',
                            'qareturnd',
                            'Finalsignatured',
                            'archived',
                            'remarks',
                            'update_time',
                            'studyno__studyplansetting__ddwzljsd',
                            'studyno__studyplansetting__gsbgd',
                            'studyno__studyplansetting__patd',
                            'studyno__studyplansetting__tkadad',
                            'studyno__studyplansetting__sumrepd',
                            'studyno__studyplansetting__wtfcfd',
                            'studyno__studyplansetting__sdwtfcfd',
                            'studyno__studyplansetting__sendqad',
                            'studyno__studyplansetting__sdsendqad',
                            'studyno__studyplansetting__qared',
                            'studyno__studyplansetting__sdqareturnd',
                            'studyno__studyplansetting__finalrd',
                            'studyno__studyplansetting__sdfinalrd',
                            'studyno__studyplansetting__activedd',
                            'studyno__studyplansetting__sdactivedd',)
        adate = [[z['studyno__projectno__projectnumber']]+
                [z['studyno__projectno__testtrarticlename__testtrarticlenumber']]+
                [z['studyno__studyno']]+
                [z['studyno__studydirector__username']]+
                [z['studyno__studysprogressstatus__initiationdate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__firstexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__lastexposuredate'].strftime('%Y-%m-%d')]+
                [z['studyno__studysprogressstatus__testenddate'].strftime('%Y-%m-%d')]+
                ['实际']+
                [thc(ds(jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__ddwzljsd'], dayset['ddwzljsd']), '%Y-%m-%d'),  z['biganimald']) if z['biganimald'] else nul]+
                [thc(ds(jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__gsbgd'], dayset['gsbgd']), '%Y-%m-%d'),  z['bmreportd']) if z['bmreportd'] else nul]+
                [thc(ds(jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__patd'], dayset['patd']), '%Y-%m-%d'),  z['patreportd']) if z['patreportd'] else nul]+
                [thc(ds(jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__tkadad'], dayset['tkadad']), '%Y-%m-%d'),  z['tkadareportd']) if z['tkadareportd'] else nul]+
                [thc(ds(jh(z['studyno__studysprogressstatus__testenddate'], z['studyno__studyplansetting__sumrepd'], dayset['sumrepd']), '%Y-%m-%d'),  z['summaryreportd']) if z['summaryreportd'] else nul]+
                [(thc(ds(yuj(z['summaryreportd'], z['studyno__studyplansetting__wtfcfd'], z['studyno__studyplansetting__sdwtfcfd'], dayset['wtfcfd'], dayset['sdwtfcfd'], z['studyno__studysprogressstatus__testenddate']),'%Y-%m-%d'), z['returnd'])) if z['returnd'] else nul]+
                [(thc(ds(yuj(z['returnd'], z['studyno__studyplansetting__sendqad'], z['studyno__studyplansetting__sdsendqad'], dayset['sendqad'], dayset['sdsendqad'], z['studyno__studysprogressstatus__testenddate']),'%Y-%m-%d'), z['dateqad'])) if z['dateqad'] else nul]+
                [(thc(ds(yuj(z['dateqad'], z['studyno__studyplansetting__qared'], z['studyno__studyplansetting__sdqareturnd'], dayset['qared'], dayset['sdqareturnd'], z['studyno__studysprogressstatus__testenddate']),'%Y-%m-%d'), z['qareturnd'])) if z['qareturnd'] else nul]+
                [(thc(ds(yuj(z['qareturnd'], z['studyno__studyplansetting__finalrd'], z['studyno__studyplansetting__sdfinalrd'], dayset['finalrd'], dayset['sdfinalrd'], z['studyno__studysprogressstatus__testenddate']),'%Y-%m-%d'), z['Finalsignatured'])) if z['Finalsignatured'] else nul]+
                [(thc(ds(yuj(z['Finalsignatured'], z['studyno__studyplansetting__activedd'], z['studyno__studyplansetting__sdactivedd'], dayset['activedd'], dayset['sdactivedd'], z['studyno__studysprogressstatus__testenddate']),'%Y-%m-%d'), z['archived'])) if z['archived'] else nul]+
                [z['remarks']]+
                [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]  # 如果上一级日期不存在也返回空值存在就按照规则加时间在进行比较thc函数. 如果本级日期不存在也返回空值
        return adate

    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 

    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Fsd = request.GET.get('sd', None)  # 得到部分人名称关键字

        if Fstudyid:  # 查询专题编号
            q1.children.append(('studyno__studyno__icontains', Fstudyid))  # 查询专题编号
        
        if Fsd:  # 查询SD
            q1.children.append(('studyno__studydirector__username__icontains', Fsd))  # 查询SD

        if Fdate:  # 查询试验结束日期范围
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
            q1.children.append(('studyno__studysprogressstatus__testenddate__gte', start_date))
            q1.children.append(('studyno__studysprogressstatus__testenddate__lte', end_date))
    
    con.add(q1, 'AND')
    con.add(q2, 'AND')  # 合并查询

    adate = sdmanager.objects.filter(con)  # 拼接的Q查询返回Queryset     
    t = toplan1(adate)
    e = expected1(adate)
    a = actual1(adate)
    date = []
    for g in zip(t,e,a):  # 拼接三条列表数据
        for z in g:
            date.append(z)
    context = {'studysdata':date, 'columnstitle': columns}  # 传入到render变量参数用于被脚本调用
    return render(request, 'sdmanager.html', context)
