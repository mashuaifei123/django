from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from studys.models import studysinfo, studydays, studyitem
from tools.colo import color
import pandas as pd

def index(request):
    """
    资产总表视图
    :param request:
    :return:
    """
    assets = models.TSMConfStatus.objects.all()
    # assets = get_object_or_404(models.StudyInfo)
    return render(request, 'assets/index.html', locals())


def TSMConfStatus(request):
    """
    配置状态
    :param request:
    :return:
    """
    assets = models.TSMConfStatus.objects.select_related()[0:300]
    # assets = get_object_or_404(models.StudyInfo)
    return render(request, 'assets/TSMConfStatus.html', locals())


def TSMReceive(request):
    """
    接收信息
    :param request:
    :return:
    """
    assets = models.TSMReceiveInfo.objects.select_related()
    #prefetch_related() 多对多join  用于提升效率
    # assets = get_object_or_404(models.StudyInfo)
    return render(request, 'assets/TSMReceive.html', locals())


def StudyNumConf(request, studynum):
    """
    根据试验编号进行查询返回配置的信息
    通过多类的条件查询一类的数据：
    一类名.objects.filter(多类名小写__多类属性名__条件名)   # 关联属性没有定义在该类中,所以用多类名小写
    通过一类的条件查询多类的数据：
    多类名.objects.filter(关联属性__一类属性名__条件名)   # 关联属性定义在该类中,所以直接用关联属性名
    """
    assets = models.TSMConfStatus.objects.filter(Study_No__Study_No=studynum)
    return render(request, 'assets/TSMConfStatus.html', locals())


def TSMstudysearch(request):
    '''以试验编号搜索配置信息'''
    
    if request.method == 'GET':
        studynum = request.GET.get('q', '')  #得到搜索关键词'试验编号'
    assets = models.TSMConfStatus.objects.filter(Study_No__Study_No__icontains=studynum)
    return render(request, 'assets/TSMConfStatus.html', locals())


def IndextoActive(request):  
    #直接跳转到一个页面的快捷方式
    return HttpResponseRedirect('/studys/studyplan')  #跳转到主界面  

'''
def StudyNumReceive(request, studynum):
    """
    根据试验编号进行查询返回接收的信息
    :param request:
    :param asset_id:
    :return:
    """
    assets = models.TSMConfStatus.objects.filter(Study_No__Study_No=studynum)
    return render(request, 'assets/TSMConfStatus.html', locals())
'''
'''
def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()

    up_rate = round(upline/total*100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())
'''


def studyinfofull(request):
    """
    根据study唯一id搜索并返回详细信息
    :param request:
    :param asset_id:
    :return:
    """
    if request.method == 'GET':
        study_id = request.GET.get('q', None)  # 得到搜索关键词'studyid'
    if study_id == None:
        return render(request, 'assets/Error.html')
    else:
        assets = studysinfo.objects.filter(pk=int(study_id))
        '''专题日程查询'''
        itemqs = studyitem.objects.all()
        itemdata = [{'id':o.id, 'text':o.itemname} for o in itemqs]  # 字典生成式加列表 生成前端用的试验操作itemname
        colordict = dict(zip(set(x.itemname for x in itemqs), set(color)))  # 生成字典和颜色配合用于生成前端带颜色的日历
        
        """ 查询部分"""
        q1 = Q()  # Q查询
        q1.children.append(('studyno', study_id))
        adate = studydays.objects.filter(q1)  # 拼接的Q查询返回Queryset 

        """开始执行查询"""
        adate = adate.values('studyno__studyno', 'studyno__studydirector__username', 'ptsdays', 'datedays', 'weekday', 'weekno', 'phasedays', 'sex','itemname__itemname', 'itemactive', 'remarks', 'update_time',)
        evedata =  [{'title'         : x['itemname__itemname'],
                    'start'          : x['datedays'].strftime('%Y-%m-%d'),
                    'url'            : '/studys/studyplan/search?q={}&sd=&date=&item={}'.format(x['studyno__studyno'], studyitem.objects.filter(itemname=x['itemname__itemname'])[0].id),
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
        if adate:

            """pandas 转置并生成相关记录"""
            sno = '备注:{}'.format(adate[0][10])  # 获取位置为0 10 的备注
            adate = [x[:-2] for x in adate]  # 选取只需要的数据.
            df = pd.DataFrame(data=adate, columns=['studyno', 'sd', 'ptsdays', 'datedays', 'weekday', 'weekno', 'phasedays', 'sex','itemname', 'itemactive'])  # 生成 DF
            df.set_index(['studyno', 'sd', 'ptsdays', 'datedays', 'weekday', 'weekno', 'phasedays', 'sex', 'itemname',], inplace=True)  # 设定索引准备unstack
            df = df.unstack()  # 长转宽
            column = ['专题编号', 'SD', '日程', '日期', '星期', '周', '试验阶段', '性别',] + list(df.columns.levels[1])  # 获取拼接后的列名称
            df = df.reset_index() # 重排索引
            df = df.fillna(' ') # 替换nan为空格
            df.sort_values(by='datedays', ascending=True, inplace=True)  # 排序日期按照降序
            adate = df.values.tolist()  # 转换为列表
            columns = [{"title": x} for x in column]  # 拼接为前端需要样式字典
        else:
            columns, sno = [], []  # 设定空的无用变量

        context = {'studydata':adate, 'columnstitle': columns, 'eventd':evedata, 'itemdata':itemdata, 'sno':sno, 'assets':assets}  # 传入到render变量参数用于被脚本调用
        return render(request, 'assets/studyinfofull.html', context)


def ajax_get_study_list(request):
    """
    AJAX数据源视图-系统模块
    """
    start = int(request.GET.get('iDisplayStart', '0'))
    length = int(request.GET.get('iDisplayLength', '30'))
    search = request.GET.get('search', '')
    current_office = request.session.get('officename')
    # 取得前台控件输入的关键字
    if search:
    # 截取查询结果对象，以start开始截取start+length位
        orgs = studysinfo.objects.filter(studyno__icontains=search).values_list('id', 'studyno')
    else:
        orgs = studysinfo.objects.all()
    val_list = []
    for org in orgs:
        val_list.append({'id':org[0], 'text':org[1]})
    # 根据关键字查询得到结果后开始拼装返回到前台的数据。先生成字典型数组，一般SELECT2组件使用的话生成id、text两个字段即可
    result = json.dumps(val_list)
    return HttpResponse(result, 'application/json')


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！')
        # 你的检测代码

        sn = data.get('sn', None)

        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)  # [obj]
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已经更新。')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn，请检查数据内容！')

    return HttpResponse('200 ok')
