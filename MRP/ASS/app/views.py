from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from .datacatch import *
from .doc import *
import markdown
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse


def s():
    Room_pid = [('1132', 23, 15),
                ('1133', 24, 16),
                ('1134', 25, 17),
                ('1135', 26, 18),
                ('1142B', 28, 20),
                ('1142A', 29, 21),
                ('1141A', 30, 22),
                ('1140', 39, 31),
                ('1159', 40, 32),
                ('1158', 41, 33),
                ('1157', 42, 34),
                ('1156', 14, 9),
                ('1153', 43, 35),
                ('1152', 44, 36),
                ('1151', 45, 37),
                ('1248A', 123, 111),
                ('1249A', 124, 112),
                ('1250A', 125, 113),
                ('1251A', 126, 114),
                ('1252A', 162, 141),
                ('1253A', 163, 142),
                ('1254A', 164, 143),
                ('1255A', 165, 144),
                ('1241A', 47, 145),
                ('1242A', 166, 146),
                ('1243A', 167, 147),
                ('1244A', 97, 86),
                ('1245A', 98, 87),
                ('1246A', 109, 100),
                ('1247A', 110, 101),
                ('1262A', 48, 127),
                ('1263A', 138, 128),
                ('1264A', 139, 129),
                ('1265A', 140, 130),
                ('1266A', 192, 168),
                ('1267A', 193, 169),
                ('1268A', 194, 170),
                ('1256A', 195, 171),
                ('1257A', 196, 172),
                ('1258A', 197, 173),
                ('1259A', 198, 174),
                ('1260A', 199, 175),
                ('1261A', 82, 75),
                ('1332', 247, 231),
                ('1333', 248, 232),
                ('1336', 249, 233),
                ('1342', 250, 234),
                ('1341', 251, 235),
                ('1340', 252, 236),
                ('1339', 253, 237),
                ('1338', 254, 238),
                ('1359', 268, 255),
                ('1358', 269, 256),
                ('1357', 270, 257),
                ('1356', 271, 258),
                ('1355', 272, 259),
                ('1352A', 273, 260),
                ('1351A', 274, 261),
                ('1432', 312, 300),
                ('1433', 313, 301),
                ('1434', 314, 302),
                ('1444', 316, 304),
                ('1443', 354, 335),
                ('1442A', 355, 336),
                ('1441', 356, 337),
                ('1440', 357, 338),
                ('1465', 329, 318),
                ('1464', 330, 319),
                ('1463', 331, 320),
                ('1462', 332, 321),
                ('1461', 333, 322),
                ('1460', 334, 323),
                ('1459', 358, 339),
                ('1456A', 359, 340),
                ('1455A', 360, 341),
                ('1454A', 361, 342),
                ('1453', 362, 343)]
    roomid = [{'id': i, 'text': Room_pid[i][0]} for i in range(len(Room_pid))]
    return roomid


def index(request):
    try:
        #studyid= request.GET['studyid']

        roomid = request.GET.getlist('roomid')
        time = request.GET['time']
        stime = time.split(' ')[0].replace('-', '')
        ttime = time.split(' ')[2].replace('-', '')
    except:
        #studyid = 'A2019027-T014-01'
        roomid = ['1']
        stime = '20191120'
        ttime = '20200102'

    print(roomid)
    print(stime)
    print(ttime)
    #uid = request.session.get('uid', None)
    # print({**get_data(studyid, roomid, stime, ttime)})
    return render(request, 'index.html', {**get_data( roomid, stime, ttime)})


def pic(request):
    try:
        roomid = request.GET.getlist('roomid')
        time = request.GET['time']
        stime = time.split(' ')[0].replace('-', '')
        ttime = time.split(' ')[2].replace('-', '')
    except:
        roomid = ['1']
        stime = '20191001'
        ttime = '20191230'
    print(roomid)
    print(stime)
    print(ttime)
    return render(request, 'pic.html',{**get_day_data( roomid, stime, ttime)})


def hold(request):
    roomid_list = s()
    context = {}
    context['roomid'] = roomid_list
    if request.method == 'GET':
        roomid = request.GET.getlist('roomid', None)  # 得到搜索关键词'studyid'
        if roomid:
            print(roomid)
            study_number ='Axxxxxxxxxxx'
            study_name = 'xxxxxxxxxxxx'
            study_anmail = 'xxxxx'
            roomid = request.GET.getlist('roomid')
            time1 = request.GET.get('time1')
            time2 = request.GET.get('time2')
            time3 = request.GET.get('time3')
            time4 = request.GET.get('time4')
            time5 = request.GET.get('time5')
            time_total = [time1, time2,time3, time4, time5]
            time_total = list(filter(None, time_total))
            print(time_total)

            stime = [i.split(' ')[0].replace('-', '') for i in time_total ]
            ttime = [i.split(' ')[2].replace('-', '') for i in time_total]
            print(stime)
            print(ttime)
            word(study_number, study_name, study_anmail, roomid, stime, ttime)
            file = open('{}.docx'.format(study_number), 'rb')
            # 以流的形式下载文件,这样可以实现任意格式的文件下载
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
            response['Content-Disposition'] = 'attachment;filename="{}"'.format('{}.docx'.format(study_number))
            return response
        else:
            return render(request, 'hold.html', {'context': context})


def ask(request):
    return render(request, 'pic1.html')



