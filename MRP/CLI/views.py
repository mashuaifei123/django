from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.db.models import F
from CLI.models import cliitem, clireading
from studys.models import studysinfo, studysprogressstatus
import pandas as pd
from django.core.serializers import serialize  # models 序列化json
from django.db.models import Sum
import datetime
from tools.dateTO import holiday
from tools.send_LB_BW import df_query, sql_query
from django.http import StreamingHttpResponse, Http404

def Fhtlmred(strvalue):  # 输入str返回带颜色html代码
    return '<font color="red">{}</font>'.format(strvalue)



def cliinfofind(request):
    """
    查询cli信息 以试验编号或者日期并统计
    """
    column = ['日期','星期','值班人员','专题负责人','专题编号','动物品系','动物数量','CBA', '流式','血液学','生化','凝血','尿常规', '尿沉渣','PAgT','骨髓涂片','备注','注意1','注意2','更新时间']
    sumcolumn = ['项目','CBA','流式', '血液学','生化','凝血','尿常规', '尿沉渣', 'PAgT','骨髓涂片']
    
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    sumcolumns = [{"title": x} for x in sumcolumn]  # 拼接为前端需要样式字典
    
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围

        if Fstudyid:  # 如果输入了专题编号关键字就以专题编号进行查询
            adate = cliitem.objects.filter(studyno__studyno__icontains=Fstudyid)
            sumdata = adate.aggregate(cbaitems=Sum('cbaitem'), 
                                      urinarysediments=Sum('urinarysediment'), 
                                      flowcytometrys=Sum('flowcytometry'),
                                      hematologys=Sum('hematology'), 
                                      biochemistrys=Sum('biochemistry'), 
                                      coagulations=Sum('coagulation'), 
                                      urinaryroutines=Sum('urinaryroutine'), 
                                      pagts=Sum('pagt'), 
                                      bonemarrowsmears=Sum('bonemarrowsmear'), 
                                      )  # 对列求和 
            sumdata = [['总计'] + list(sumdata.values())] # 和值
            bl = []
            for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装
                iddate = list(cliitem.objects.filter(pk=pk).values_list('dutyofficer__username'))
                ab = [','.join([y for y in [','.join(x) for x in iddate]])]
                bl.append(ab)
            adate = adate.values('date', 
                                'studyno__studydirector__username',
                                'studyno__studyno', 
                                'studyno__testsystem__testsystemname',
                                'anmailnum',
                                'cbaitem',
                                'flowcytometry',
                                'hematology',
                                'biochemistry',
                                'coagulation',
                                'urinaryroutine',
                                'urinarysediment',
                                'pagt',
                                'bonemarrowsmear',
                                'remarks',
                                'remarks1',
                                'remarks2',
                                'update_time',
                                )
            adate = [[z['date'].strftime('%Y-%m-%d')]+
             [z['studyno__studydirector__username']]+
             [z['studyno__studyno']]+
             [z['studyno__testsystem__testsystemname']]+
             [z['anmailnum']]+
             [Fhtlmred(z['cbaitem'])]+
             [Fhtlmred(z['flowcytometry'])]+
             [z['hematology']]+
             [z['biochemistry']]+
             [z['coagulation']]+
             [z['urinaryroutine']]+
             [Fhtlmred(z['urinarysediment'])]+
             [Fhtlmred(z['pagt'])]+
             [Fhtlmred(z['bonemarrowsmear'])]+
             [z['remarks']]+
             [z['remarks1']]+
             [z['remarks2']]+
             [z['update_time'].strftime('%y-%m-%d %H:%M:%S')] for z in adate] # 对数据日期格式进行格式化生成新数据列表
            for i in range(len(bl)):  # 拼接值班人员和数据表
                adate[i][0:1] = list(holiday(adate[i][0]))
                adate[i][2:2] = bl[i]
            context = {'clidata':adate, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'cliinfo.html', context)
        
        if Fdate:  # 如果输入了日期范围进行查询
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])
            adate = cliitem.objects.filter(date__gte=start_date, date__lte=end_date) # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
            sumdata = adate.aggregate(cbaitems=Sum('cbaitem'), 
                                      urinarysediments=Sum('urinarysediment'), 
                                      flowcytometrys=Sum('flowcytometry'),
                                      hematologys=Sum('hematology'), 
                                      biochemistrys=Sum('biochemistry'), 
                                      coagulations=Sum('coagulation'), 
                                      urinaryroutines=Sum('urinaryroutine'), 
                                      pagts=Sum('pagt'), 
                                      bonemarrowsmears=Sum('bonemarrowsmear'), 
                                      )  # 对列求和 
            sumdata = [[Fdate,'总计'] + list(sumdata.values())] # 和值
            bl = []
            for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装
                iddate = list(cliitem.objects.filter(pk=pk).values_list('dutyofficer__username'))
                ab = [','.join([y for y in [','.join(x) for x in iddate]])]
                bl.append(ab)
            adate = adate.values('date', 
                                'studyno__studydirector__username',
                                'studyno__studyno', 
                                'studyno__testsystem__testsystemname',
                                'anmailnum',
                                'cbaitem',
                                'flowcytometry',
                                'hematology',
                                'biochemistry',
                                'coagulation',
                                'urinaryroutine',
                                'urinarysediment',
                                'pagt',
                                'bonemarrowsmear',
                                'remarks',
                                'remarks1',
                                'remarks2',
                                'update_time',
                                )
            adate = [[z['date'].strftime('%Y-%m-%d')]+
             [z['studyno__studydirector__username']]+
             [z['studyno__studyno']]+
             [z['studyno__testsystem__testsystemname']]+
             [z['anmailnum']]+
             [Fhtlmred(z['cbaitem'])]+
             [Fhtlmred(z['flowcytometry'])]+
             [z['hematology']]+
             [z['biochemistry']]+
             [z['coagulation']]+
             [z['urinaryroutine']]+
             [Fhtlmred(z['urinarysediment'])]+
             [Fhtlmred(z['pagt'])]+
             [Fhtlmred(z['bonemarrowsmear'])]+
             [z['remarks']]+
             [z['remarks1']]+
             [z['remarks2']]+
             [z['update_time'].strftime('%y-%m-%d %H:%M:%S')] for z in adate] # 对数据日期格式进行格式化生成新数据列表
            for i in range(len(bl)):  # 拼接值班人员和数据表
                adate[i][0:1] = list(holiday(adate[i][0]))
                adate[i][2:2] = bl[i]
            sumcolumns = [{"title": '时间范围'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adate, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'cliinfo.html', context)
    if Fstudyid == None:  # 当Fstudyid为none 返回错误必须输入参数
        return render(request, 'cliinfo.html', {'error': True})

    else:  # 没有提交GET请求返回一个错误页面
        return render(request, 'cliinfo.html', {'error': True})
        # return render(request, 'assets/Error.html')


    """
    # else:
        # assets = models.StudyInfo.objects.filter(pk=int(study_id))
    cliitem.objects.select_related()[0:150].values_list('date', 'studyno__studyno', 'studyno__studyname', 'cbaitem',)
    a = cliitem.objects.select_related()[0:150].values_list('date', 'studyno__studyno', 'studyno__studyname', 'cbaitem',)
    s = a.aggregate(CBA=Sum('cbaitem'), 鸟沉渣=Sum('flowcytometry'), urinasum=Sum('urinarysediment'), )  # 对列求和
    # select_related() 多对一join 用于提升效率
    # prefetch_related() 多对多join  用于提升效率
    # assets = get_object_or_404(models.StudyInfo)
    # json_data = serialize('json', a) # filter 用于直接转换 Queryset
    # https://www.cnblogs.com/baylorqu/p/7909892.html
    # 调用的时候需要了解的是：1、使用values进行调用返回的是valueQuerySet字段，而浊QuerySet,所以先转成list然后再使用json.dumps转成json
    #                      2、使用filter进行调用返回在是QuerySet对象，那么就可以直接使用serializers.serialize() 方法转化为json
    # json_data = json.loads(json_data) # 序列化成json对象
    # b = {"data":[{'studyno':, 'itemname':x[1], 'anmailnum':x[2]} for x in a ]}
    b = [[x[0].strftime('%Y-%m-%d'), x[1], x[2], x[3]] for x in a ]  # 把读取出的数据生成列表用于导入pandas DF 长转换宽
    # df = pd.DataFrame(data=b, columns=['studyno', 'studyname', 'item', 'num'])  # 生成 DF
    # df = df.pivot_table(index=['studyno', 'studyname'], columns='item')  # 数据透视长转宽
    # column = ['专题编号', '专题名称'] + list(df.columns.levels[1])  # 获取拼接后的列名称
    # df = df.reset_index() # 重排索引
    # data = df.values.tolist()
    # clidata = json.dumps(b)
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    context = {
        'clidata':b,
        'columnstitle': columns
    }  # 传入到render变量参数用于被脚本调用
    return render(request, 'cliinfo.html', context)
    """

def cliinfo(request):
    """
    显示当日-2+2 5天信息
    :param request:
    :return:
    """
    column = ['日期','星期','值班人员','专题负责人','专题编号','动物品系','动物数量','CBA','流式','血液学','生化','凝血','尿常规','尿沉渣','PAgT','骨髓涂片','备注','注意1','注意2','更新时间']
    sumcolumn = ['项目','CBA','流式','血液学','生化','凝血','尿常规','尿沉渣','PAgT','骨髓涂片']
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    sumcolumns = [{"title": x} for x in sumcolumn]  # 拼接为前端需要样式字典
    start_date = datetime.datetime.now()+datetime.timedelta(days=-2)
    end_date = datetime.datetime.now()+datetime.timedelta(days=2)
    Fdate = '{} - {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    adate = cliitem.objects.filter(date__gte=start_date, date__lte=end_date) # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
    sumdata = adate.aggregate(cbaitems=Sum('cbaitem'), 
                                urinarysediments=Sum('urinarysediment'), 
                                flowcytometrys=Sum('flowcytometry'),
                                hematologys=Sum('hematology'), 
                                biochemistrys=Sum('biochemistry'), 
                                coagulations=Sum('coagulation'), 
                                urinaryroutines=Sum('urinaryroutine'), 
                                pagts=Sum('pagt'), 
                                bonemarrowsmears=Sum('bonemarrowsmear'), 
                                )  # 对列求和 
    sumdata = [[Fdate,'总计'] + list(sumdata.values())] # 和值
    bl = []
    for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装
        iddate = list(cliitem.objects.filter(pk=pk).values_list('dutyofficer__username'))
        ab = [','.join([y for y in [','.join(x) for x in iddate]])]
        bl.append(ab)
    adate = adate.values('date', 
                        'studyno__studydirector__username',
                        'studyno__studyno', 
                        'studyno__testsystem__testsystemname',
                        'anmailnum',
                        'cbaitem',
                        'flowcytometry',
                        'hematology',
                        'biochemistry',
                        'coagulation',
                        'urinaryroutine',
                        'urinarysediment',
                        'pagt',
                        'bonemarrowsmear',
                        'remarks',
                        'remarks1',
                        'remarks2',
                        'update_time',
                        )
    adate = [[z['date'].strftime('%Y-%m-%d')]+
             [z['studyno__studydirector__username']]+
             [z['studyno__studyno']]+
             [z['studyno__testsystem__testsystemname']]+
             [z['anmailnum']]+
             [Fhtlmred(z['cbaitem'])]+
             [Fhtlmred(z['flowcytometry'])]+
             [z['hematology']]+
             [z['biochemistry']]+
             [z['coagulation']]+
             [z['urinaryroutine']]+
             [Fhtlmred(z['urinarysediment'])]+
             [Fhtlmred(z['pagt'])]+
             [Fhtlmred(z['bonemarrowsmear'])]+
             [z['remarks']]+
             [z['remarks1']]+
             [z['remarks2']]+
             [z['update_time'].strftime('%y-%m-%d %H:%M:%S')] for z in adate] # 对数据日期格式进行格式化生成新数据列表
    for i in range(len(bl)):  # 拼接值班人员和数据表
        adate[i][0:1] = list(holiday(adate[i][0]))
        adate[i][2:2] = bl[i]
    # <label class="label label-success"> 内容字符串 </label>  颜色代码label
    # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色 
    sumcolumns = [{"title": '时间范围'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
    context = {'clidata':adate, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
    return render(request, 'cliinfo.html', context)

def clireadinginfofind(request):
    """
    查询临检阅片信息 以试验编号或者日期或阅片状态并统计
    """
    column = ['专题负责人','专题编号','动物品系','动物来源','试验开始日期','试验结束日期','动物数量','骨髓制片', '阅片状态','阅片人员','阅片日期','报告日期','归档日期','备注', '更新时间']
    sumcolumn = ['项目','动物数量']
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    sumcolumns = [{"title": x} for x in sumcolumn]  # 拼接为前端需要样式字典

    def query_b(adate):
        '''根据查询Quetyset返回数据及求和数据'''
        sumdata = adate.aggregate(anmailnums=Sum('anmailnum'))  # 对列求和
        adatea = adate.values_list('studyno__studydirector__username', 
                                'studyno__studyno', 
                                'studyno__testsystem__testsystemname', 
                                'studyno__animalsource',
                                'studyno__studysprogressstatus__teststartdate',
                                'studyno__studysprogressstatus__testenddate',
                                )    # 前半段数据 
        bl = []
        for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装
            iddate = list(clireading.objects.filter(pk=pk).values_list('observedby__username'))
            ab = [','.join([y for y in [','.join(x) for x in iddate]])]
            bl.append(ab)
        adate = adate.values_list('anmailnum',
                                'bonemarrow',
                                'readingstatus',
                                'readingdate',
                                'reportdate',
                                'inputdate',
                                'remarks',
                                'update_time',
                                )
        adatea = [x[:4]+[x[4].strftime('%Y-%m-%d') if x[4] else ' ']+[x[5].strftime('%Y-%m-%d') if x[5] else ' '] for x in [list(z) for z in list(adatea)]]  # 前半段数据
        adateb = [x[0:3]+[x[3].strftime('%Y-%m-%d') if x[3] else ' ']+[x[4].strftime('%Y-%m-%d') if x[4] else ' ']+[x[5].strftime('%Y-%m-%d') if x[5] else ' ']+x[6:7]+[x[-1].strftime('%y-%m-%d %H:%M:%S')] for x in [list(z) for z in list(adate)]]  # 后半段数据及拼接
        dt1 =  {0:r'<label class="label label-warning">不阅片</label>',
                1:r'<label class="label label-primary">待阅片</label>',
                2:r'<label class="label label-info">阅片中</label>',
                3:r'<label class="label label-success">阅片完成</label>',
                4:r'<label class="label label-default">待定</label>',}
        zp1 = {0:'不制片', 1:'制片'}
        # <label class="label label-success"> 内容字符串 </label>  颜色代码label
        # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色
        for i in range(len(bl)):  # 拼接值班人员和数据表
            adateb[i][3:3] = bl[i]
            adateb[i][0:0] = adatea[i]
            adateb[i][7:8] = [zp1.get(adateb[i][7])]
            adateb[i][8:9] = [dt1.get(adateb[i][8])]
            
        return adateb, sumdata

    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        Fstutus = request.GET.get('rs', None) # 得到搜索阅片状态关键词
        Fzp = request.GET.get('zp', None) # 得到搜索制片关键词
        Fdaterep = request.GET.get('daterep', None) # 得到报告日期范围
            # Fdate = '{} - {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if Fstudyid:  # 查询专题编号
            adate = clireading.objects.filter(studyno__studyno__icontains=Fstudyid)  # 查询专题编号
            adateb, sumdata = query_b(adate)
            sumdata = [['总计'] + list(sumdata.values())] # 和值
            sumcolumns = [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'clireadinginfo.html', context)

        if Fdate:  # 查询时间范围
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            adate = clireading.objects.filter(studyno__studysprogressstatus__testenddate__gte=start_date, studyno__studysprogressstatus__testenddate__lte=end_date) # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
            adateb, sumdata = query_b(adate)
            sumdata = [[Fdate,'总计'] + list(sumdata.values())] # 和值
            sumcolumns = [{"title": '试验结束时间范围'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'clireadinginfo.html', context)

        if Fstutus:  # 查询状态
            dt1 =  {0:r'<label class="label label-warning">不阅片</label>',
                    1:r'<label class="label label-primary">待阅片</label>',
                    2:r'<label class="label label-info">阅片中</label>',
                    3:r'<label class="label label-success">阅片完成</label>',
                    4:r'<label class="label label-default">待定</label>',}
            adate = clireading.objects.filter(readingstatus=Fstutus)  # 查询阅片状态
            adateb, sumdata = query_b(adate)
            sumdata = [[dt1.get(int(Fstutus)),'总计'] + list(sumdata.values())] # 和值
            sumcolumns = [{"title": '阅片状态'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'clireadinginfo.html', context)
        
        if Fzp:  # 查询制片状态
            adate = clireading.objects.filter(bonemarrow=Fzp) # 查询制片状态
            zp1 = {0:'不制片', 1:'制片'}
            adateb, sumdata = query_b(adate)
            sumdata = [[zp1.get(int(Fzp)),'总计'] + list(sumdata.values())] # 和值
            sumcolumns = [{"title": '骨髓制片'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'clireadinginfo.html', context)
        
        if Fdaterep:  # 查询时间范围
            fd = [int(x) for x in Fdaterep.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            adate = clireading.objects.filter(reportdate__gte=start_date, reportdate__lte=end_date) # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
            adateb, sumdata = query_b(adate)
            sumdata = [[Fdaterep,'总计'] + list(sumdata.values())] # 和值
            sumcolumns = [{"title": '报告结束时间范围'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
            context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
            return render(request, 'clireadinginfo.html', context)

    if Fstudyid == None:
        return render(request, 'clireadinginfo.html', {'error': True})

    else:  # 没有提交GET请求返回一个错误页面
        return render(request, 'clireadinginfo.html', {'error': True})
        # return render(request, 'assets/Error.html')

def clireadinginfo(request):
    """
    显示7日内阅片信息
    :param request:
    :return:
    """
    column = ['专题负责人','专题编号','动物品系','动物来源','试验开始日期','试验结束日期','动物数量','骨髓制片', '阅片状态','阅片人员','阅片日期','报告日期','归档日期','备注', '更新时间']
    sumcolumn = ['项目','动物数量']
    columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
    sumcolumns = [{"title": x} for x in sumcolumn]  # 拼接为前端需要样式字典
    start_date = datetime.datetime.now() - datetime.timedelta(days=7)  # 当前时间减去7天得到开始时间
    end_date = datetime.datetime.now()
    Fdate = '{} - {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    adate = clireading.objects.filter(studyno__studysprogressstatus__testenddate__gte=start_date, studyno__studysprogressstatus__testenddate__lte=end_date) # 第二种办法__range['2019-09-09',' 2019-09-11'] 注意不包含后者
    sumdata = adate.aggregate(anmailnums=Sum('anmailnum'))  # 对列求和 
    adatea = adate.values_list('studyno__studydirector__username', 
                               'studyno__studyno', 
                               'studyno__testsystem__testsystemname', 
                               'studyno__animalsource',
                               'studyno__studysprogressstatus__teststartdate',
                               'studyno__studysprogressstatus__testenddate',
                               )    # 前半段数据 
    bl = []
    for pk in [x.id for x in adate]:  # 根据ID  PK 查询多对多并组装
        iddate = list(clireading.objects.filter(pk=pk).values_list('observedby__username'))
        ab = [','.join([y for y in [','.join(x) for x in iddate]])]
        bl.append(ab)
    adate = adate.values_list('anmailnum',
                            'bonemarrow',
                            'readingstatus',
                            'readingdate',
                            'reportdate',
                            'inputdate',
                            'remarks',
                            'update_time',
                            )
    adatea = [x[:4]+[x[4].strftime('%Y-%m-%d')]+[x[5].strftime('%Y-%m-%d')] for x in [list(z) for z in list(adatea)]]  # 前半段数据
    adateb = [x[0:3]+[x[3].strftime('%Y-%m-%d') if x[3] else ' ']+[x[4].strftime('%Y-%m-%d') if x[4] else ' ']+[x[5].strftime('%Y-%m-%d') if x[5] else ' ']+x[6:7]+[x[-1].strftime('%y-%m-%d %H:%M:%S')] for x in [list(z) for z in list(adate)]]  # 后半段数据及拼接
    dt1 =  {0:r'<label class="label label-warning">不阅片</label>',
            1:r'<label class="label label-primary">待阅片</label>',
            2:r'<label class="label label-info">阅片中</label>',
            3:r'<label class="label label-success">阅片完成</label>',
            4:r'<label class="label label-default">待定</label>',}
    zp1 = {0:'不制片', 1:'制片'}
    # <label class="label label-success"> 内容字符串 </label>  颜色代码label
    # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色
    for i in range(len(bl)):  # 拼接值班人员和数据表
        adateb[i][3:3] = bl[i]
        adateb[i][0:0] = adatea[i]
        adateb[i][7:8] = [zp1.get(adateb[i][7])]
        adateb[i][8:9] = [dt1.get(adateb[i][8])]
    sumdata = [[Fdate,'总计'] + list(sumdata.values())] # 和值
    sumcolumns = [{"title": '时间范围'}] + [{"title": x} for x in sumcolumn]  # 重写时间列名称拼接为前端需要样式字典
    context = {'clidata':adateb, 'columnstitle': columns, 'sumdata': sumdata, 'sumcolumns':sumcolumns}  # 传入到render变量参数用于被脚本调用
    return render(request, 'clireadinginfo.html', context)

"""
def StudyNumConf(request, studynum):
    ''''''
    根据试验编号进行查询返回配置的信息
    通过多类的条件查询一类的数据：
    一类名.objects.filter(多类名小写__多类属性名__条件名)   # 关联属性没有定义在该类中,所以用多类名小写
    通过一类的条件查询多类的数据：
    多类名.objects.filter(关联属性__一类属性名__条件名)   # 关联属性定义在该类中,所以直接用关联属性名
    ''''''
    assets = models.TSMConfStatus.objects.filter(Study_No__Study_No=studynum)
    return render(request, 'assets/TSMConfStatus.html', locals())


def TSMstudysearch(request):
    '''以试验编号搜索配置信息'''
    
    if request.method == 'GET':
        studynum = request.GET.get('q', '')  #得到搜索关键词'试验编号'
    assets = models.TSMConfStatus.objects.filter(Study_No__Study_No__icontains=studynum)
    return render(request, 'assets/TSMConfStatus.html', locals())
"""


def LB_BW_query(request):
    items = sql_query()
    itemdict = {x:y for x, y in enumerate(items)} # 生成被调用的字典{0:'A2017004-T014-01'}
    itemdata = [{'id':o, 'text':z} for o, z in itemdict.items()]  
    # 字典迭代生成式加列表[{'id': 0, 'text': 'A2017004-T014-01'},] 生成前端用的试验操作itemname
    context = {'itemdata':itemdata}
    if request.method == 'GET':
        Fstudyid = request.GET.get('q', None)  # 得到搜索关键词'studyid'

        if Fstudyid:  # 如果输入了专题编号关键字就以专题编号进行查询
            Fstudyid = itemdict[int(Fstudyid)]  #由字典获取专题编号
            if len(Fstudyid) <= 18:
                file_name = '{}.xlsx'.format(Fstudyid)
                df = df_query(Fstudyid)
                df.drop_duplicates(['CheckCode', 'PatientName', 'SendTime'],keep='last',inplace=True) # 根据ID 列去重 并导出excel
                # 组装代码写这里
                df.to_excel('temp.xlsx')
                # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
                response = StreamingHttpResponse(open('temp.xlsx', 'rb'))
                # 以流的形式下载文件,这样可以实现任意格式的文件下载
                response['Content-Type'] = 'application/octet-stream'
                # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
                response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
                return response

        if Fstudyid == None:  # 当Fstudyid为none 
            return render(request, 'cliLB_BW.html', context)

    else:  # 没有提交GET请求返回一个错误页面
        return render(request, 'cliLB_BW.html', {'error': True}.update(context))


