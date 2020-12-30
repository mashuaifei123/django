from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
import datetime
from django.contrib.auth.decorators import login_required  # 确认是否已经登入装装饰器
from django.contrib.auth.decorators import permission_required
import pandas as pd
from TRA.models import tarcheckpope, tarcreates, tarinpope
from assets.models import usersinfo
from django.db.models import Count, Sum
import numpy as np
from tools.dateTO import Date_Year_Month_1
# Create your views here.

def statalist(request):
    trano_list = tarcreates.objects.all().order_by("-update_time")[:10] # 排序后返回前10
    TR_column = ['日期','培训内容','主讲人','地点','更新日期']
    TR_columns = [{"title": x} for x in TR_column]  # 拼接为前端需要样式字典
    adate = trano_list.values(  'infodata',
                        'infoname',
                        'techname__username',
                        'addressroom',
                        'update_time',
                        )  #  查询数据

    adate = [[z['infodata'].strftime('%Y-%m-%d')]+
                    [z['infoname']]+
                    [z['techname__username']]+
                    [z['addressroom']]+
                    [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]
    data_year_month = Date_Year_Month_1() # 得到过去12个月列表
    cdate = []
    for item in data_year_month:
        q1 = Q()  # Q查询
        q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
        con = Q()
        q2 = Q()
        q2.connector = 'OR'
        itemspl = item.split('-')
        q1.children.append(('infoname__infodata__year', itemspl[0]))
        q1.children.append(('infoname__infodata__month', itemspl[1]))
        con.add(q1, 'AND')
        con.add(q2, 'AND')  # 合并查询
        bdate = tarcheckpope.objects.filter(con)
        bacinf = bdate.aggregate(counts=Count('infoname__infoname'), sumsh=Sum('trainingduration'))
        baccuser = bdate.aggregate(sumjishu=Count('checkpope__username'))
        cdate.append([bacinf['counts'], baccuser['sumjishu'], float(bacinf['sumsh']) if bacinf['sumsh'] else 0])
    cdate = np.asarray(cdate).T.tolist() # 转换为np array 转置  在转换为列表
    data2 = [{
            'name': '培训场次',
            'data': cdate[0]
        }, {
            'name': '实参计数',
            'data': cdate[1]
        }, {
            'name': '月时长(h)',
            'data': cdate[2]
        }]
    datal = [{
            'name': '培训场次',
            'data': [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 21.4, 19.1, 95.6, 54.4]
        }, {
            'name': '实参计数',
            'data': [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
        }, {
            'name': '月时长(h)',
            'data': [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6, 52.4, 65.2, 59.3, 51.2]
        }]
    context = {'series':datal, 'data':adate, 'title': TR_columns, 'dym': data_year_month}  # 传入到render变量参数用于被脚本调用
    return render(request, 'statalist.html', context)



def traininglist(request):
    ''' 培训清单 查询返回 '''
    # 前段需要的专题列表
    trano_list = tarcreates.objects.all().values("id","infoname")
    trano_josn = [{'id':o['id'], 'text':o['infoname']} for o in trano_list]
    TR_column = ['日期','培训内容','地点','组织部门','主讲人','时长(h)','更新时间','实参加人员','人数', '应参加人员', '人数', '应参未参加人员',]
    TR_columns = [{"title": x} for x in TR_column]  # 拼接为前端需要样式字典

    """ 合并判断查询部分"""
    q1 = Q()  # Q查询
    q1.connector = 'AND'              # 连接方式 默认AND 可以设定为OR
    con = Q()
    q2 = Q()
    q2.connector = 'OR' 
    if request.method == 'GET':
        Ftranoid = request.GET.get('q', None)  # 得到搜索关键词'studyid'
        Fcyr = request.GET.get('cyr', None)  # 得到部分人名称关键字
        Fdate = request.GET.get('date', None)  # 得到搜索日期范围
        
        if Ftranoid:  # 查询培训编号
            q1.children.append(('id', int(Ftranoid)))
        if Fcyr:  # 查询主讲人
            q1.children.append(('checkpope__username__icontains', Fcyr))
        if Fdate:
            fd = [int(x) for x in Fdate.strip().split('-')]  # 拆分日期开始结束
            start_date = datetime.date(fd[0], fd[1], fd[2])
            end_date = datetime.date(fd[3], fd[4], fd[5])  # 返回拼接时间字符串'2019-09-27'
            q1.children.append(('infoname__infodata__gte', start_date))
            q1.children.append(('infoname__infodata__lte', end_date))
        con.add(q1, 'AND')
        con.add(q2, 'AND')  # 合并查询
        # 一类名.objects.filter(多类名小写__多类属性名__条件名) 
        # zz = tarcheckpope.objects.filter(checkpope__username__icontains='老')
        # print(zz)
        if Ftranoid or Fcyr or Fdate: # 任何一个有数据执行
            adate = tarcheckpope.objects.filter(con).order_by('update_time')  # 拼接的Q查询返回Queryset order_by 排序
            bl = []
            for pk, inp in [(x.id, x.infoname) for x in adate]:  # 根据ID  PK 查询多对多并组装 参与人员
                iddate = tarcheckpope.objects.filter(pk=pk).values_list('checkpope__username')
                inpopes = tarinpope.objects.filter(infoname=inp).values_list('inpope__username')
                countname = iddate.aggregate(sumcount=Count('id'))  # 实参人员输出的时候计数
                countnamein = inpopes.aggregate(sumcount=Count('id'))  # 应参人员输出的时候计数
                liddate, linpopes = list(iddate), list(inpopes)
                jiaoji = list(set(linpopes) - set(liddate))  # 差集 应参加未参加人员
                ab = [','.join([y for y in [','.join(x) for x in liddate]])]  # 实际参加
                ac = [','.join([y for y in [','.join(x) for x in linpopes]])]  # 应参加
                ad = [','.join([y for y in [','.join(x) for x in jiaoji]])]  #  应参加未参加
                bl.append(ab + [countname['sumcount']] + ac + [countnamein['sumcount']] + ad)
            adate = adate.values('infoname__infodata',
                                'infoname__infoname',
                                'infoname__addressroom',
                                'infoname__infodept__deptname',
                                'infoname__techname__username',
                                'trainingduration',
                                'update_time',
                                )  #  查询数据
            adate = [[z['infoname__infodata'].strftime('%Y-%m-%d')]+
                    [z['infoname__infoname']]+
                    [z['infoname__addressroom']]+
                    [z['infoname__infodept__deptname']]+
                    [z['infoname__techname__username']]+
                    [str(z['trainingduration'])]+
                    [z['update_time'].strftime('%Y-%m-%d %H:%M:%S')] for z in adate]  # 列表生成数据格式
            for i in range(len(bl)):  # 拼接人员和数计数
                adate[i] = adate[i]+bl[i]
            context = {'trano':trano_josn, 'data':adate, 'title': TR_columns,}  # 传入到render变量参数用于被脚本调用
            return render(request, 'traininglist.html', context)
        else:
            context = {'trano':trano_josn}  # 传入到render变量参数用于被脚本调用
            return render(request, 'traininglist.html', context)