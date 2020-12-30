from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponseRedirect
import time
import os
from django.shortcuts import render_to_response
from UploadMulti.forms import PhotoForm, tsmForm, spssForm, xzxForm, wordForm
from .models import Photo, tsmcode, spss, xzx, word

from .lib.png_to_csv import png_to_csv1
from .lib.word_zongxiang import word_to_p
from .lib.xueya_to_table import xue_ya

from .lib.xindian_to_table import xin_dian
#新增
from .lib.spss_xlsx import read_excel
from .lib.excel_xianzhux import xianzhuxing1
from .lib.excel_xianzhuxing3 import xianzhuxing3
from .lib.xibao import xibao_xzx
from .lib.Individual_data import excel_froms
from .lib.word_zongxiang1 import  word_to_p

from uploadFiles.settings import MEDIA_ROOT, MEDIA_URL
from shutil import rmtree
from .lib.code128 import read_xlsx_pdf_tsm, read_xlsx_pdf_2612, read_xlsx_pdf_6236, read_xlsx_pdf_3512, read_xlsx_pdf_2515
from django.http import HttpResponse

global MEDIA_ROOT_N
global MEDIA_URL_N
MEDIA_ROOT_N = os.path.join(MEDIA_ROOT)
MEDIA_URL_N = os.path.join(MEDIA_URL)

'''
class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': Tr
            ue, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
'''


class ProgressBarUploadView(View):

    def get(self, request):
        MEDIA_Path_in = MEDIA_URL_N + 'input/'
        MEDIA_Path_out = MEDIA_URL_N + 'output/'
        path0_list = [os.path.join(MEDIA_ROOT_N, 'input'), os.path.join(MEDIA_ROOT_N, 'output')]
        for i in path0_list:
            isExists = os.path.exists(i)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(i)
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass
        photos_list = Photo.objects.all()
        # photos_list1 = map(lambda x: MEDIA_Path_in + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'input')))
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'output')))
        # for photo in photos_list:
            # print(photo.file.url)
        return render(self.request, 'UploadMulti/progress_bar_upload/index.html', {'photos': photos_list, 'photos2': Photos_list2})

    def post(self, request):
        #time.sleep(3)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class TsmUploadView(View):

    def get(self, request):
        MEDIA_Path_in = MEDIA_URL_N + 'tsminput/'
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        path0_list = [os.path.join(MEDIA_ROOT_N, 'tsminput'), os.path.join(MEDIA_ROOT_N, 'tsmoutput')]
        for i in path0_list:
            isExists = os.path.exists(i)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(i)
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass
        photos_list = tsmcode.objects.all()
        # photos_list1 = map(lambda x: MEDIA_Path_in + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'input')))
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        # for photo in photos_list:
            # print(photo.file.url)
        return render(self.request, 'UploadMulti/tsmptscode_upload/index.html', {'photos': photos_list, 'photos2': Photos_list2})

    def post(self, request):
        #time.sleep(3)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = tsmForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class SpssUploadView(View):

    def get(self, request):
        MEDIA_Path_in = MEDIA_URL_N + 'spssinput/'
        MEDIA_Path_out = MEDIA_URL_N + 'spssoutput/'
        path0_list = [os.path.join(MEDIA_ROOT_N, 'spssinput'), os.path.join(MEDIA_ROOT_N, 'spssoutput')]
        for i in path0_list:
            isExists = os.path.exists(i)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(i)
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass
        photos_list = spss.objects.all()
        # photos_list1 = map(lambda x: MEDIA_Path_in + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'input')))
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'spssoutput')))
        # for photo in photos_list:
            # print(photo.file.url)
        return render(self.request, 'UploadMulti/spss/index.html', {'photos': photos_list, 'photos2': Photos_list2})

    def post(self, request):
        #time.sleep(3)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = spssForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class XzxUploadView(View):
    def get(self, request):
        MEDIA_Path_in = MEDIA_URL_N + 'xzxinput/'
        MEDIA_Path_out = MEDIA_URL_N + 'xzxoutput/'
        path0_list = [os.path.join(MEDIA_ROOT_N, 'xzxinput'), os.path.join(MEDIA_ROOT_N, 'xzxoutput')]
        for i in path0_list:
            isExists = os.path.exists(i)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(i)
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass
        photos_list = xzx.objects.all()
        # photos_list1 = map(lambda x: MEDIA_Path_in + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'input')))
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'xzxoutput')))
        # for photo in photos_list:
            # print(photo.file.url)
        return render(self.request, 'UploadMulti/xianzhuxing/index.html', {'photos': photos_list, 'photos2': Photos_list2})

    def post(self, request):
        #time.sleep(3)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = xzxForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class WordUploadView(View):
    def get(self, request):
        MEDIA_Path_in = MEDIA_URL_N + 'wordinput/'
        MEDIA_Path_out = MEDIA_URL_N + 'wordoutput/'
        path0_list = [os.path.join(MEDIA_ROOT_N, 'wordinput'), os.path.join(MEDIA_ROOT_N, 'wordoutput')]
        for i in path0_list:
            isExists = os.path.exists(i)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(i)
            else:
                # 如果目录存在则不创建，并提示目录已存在
                pass
        photos_list = word.objects.all()
        # photos_list1 = map(lambda x: MEDIA_Path_in + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'input')))
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'wordoutput')))
        # for photo in photos_list:
            # print(photo.file.url)
        return render(self.request, 'UploadMulti/word/index.html', {'photos': photos_list, 'photos2': Photos_list2})

    def post(self, request):
        #time.sleep(3)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = wordForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


'''
class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
'''


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    rmtree(os.path.join(MEDIA_ROOT_N, 'input'))
    rmtree(os.path.join(MEDIA_ROOT_N, 'output'))
    path0_list = [os.path.join(MEDIA_ROOT_N, 'input'), os.path.join(MEDIA_ROOT_N, 'output')]
    for i in path0_list:
        isExists = os.path.exists(i)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(i)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    return redirect('/UploadMulti/progress-bar-upload/')


def clear_database_ss(request):
    for photo in spss.objects.all():
        photo.file.delete()
        photo.delete()
    rmtree(os.path.join(MEDIA_ROOT_N, 'spssinput'))
    rmtree(os.path.join(MEDIA_ROOT_N, 'spssoutput'))
    path0_list = [os.path.join(MEDIA_ROOT_N, 'spssinput'), os.path.join(MEDIA_ROOT_N, 'spssoutput')]
    for i in path0_list:
        isExists = os.path.exists(i)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(i)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    return redirect('/UploadMulti/spss-upload/')


def clear_database_tsm(request):
    for photo in tsmcode.objects.all():
        photo.file.delete()
        photo.delete()
    rmtree(os.path.join(MEDIA_ROOT_N, 'tsminput'))
    rmtree(os.path.join(MEDIA_ROOT_N, 'tsmoutput'))
    path0_list = [os.path.join(MEDIA_ROOT_N, 'spssinput'), os.path.join(MEDIA_ROOT_N, 'tsmoutput')]
    for i in path0_list:
        isExists = os.path.exists(i)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(i)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    return redirect('/UploadMulti/tsm-upload/')

def clear_database_xzx(request):
    for photo in xzx.objects.all():
        photo.file.delete()
        photo.delete()
    rmtree(os.path.join(MEDIA_ROOT_N, 'xzxinput'))
    rmtree(os.path.join(MEDIA_ROOT_N, 'xzxoutput'))
    path0_list = [os.path.join(MEDIA_ROOT_N, 'xzxinput'), os.path.join(MEDIA_ROOT_N, 'xzxoutput')]
    for i in path0_list:
        isExists = os.path.exists(i)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(i)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    return redirect('/UploadMulti/xzx-upload/')


def clear_database_word(request):
    for photo in word.objects.all():
        photo.file.delete()
        photo.delete()
    rmtree(os.path.join(MEDIA_ROOT_N, 'wordinput'))
    rmtree(os.path.join(MEDIA_ROOT_N, 'wordoutput'))
    path0_list = [os.path.join(MEDIA_ROOT_N, 'wordinput'), os.path.join(MEDIA_ROOT_N, 'wordoutput')]
    for i in path0_list:
        isExists = os.path.exists(i)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(i)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    return redirect('/UploadMulti/word-upload/')




'''
class Png_to_csv(View):

    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
'''
def Png_to_csv(request):  # 呼吸转csv
    word_path = os.path.join(MEDIA_ROOT_N, 'input')
    output_path = os.path.join(MEDIA_ROOT_N, 'output')

    try:
        png_to_csv1(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'output/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'output')))
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('Png_to_csv文件不存在或者格式错误')
        clear_database(request)
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()

'''
def Word_to_pdf(request):  # word转pdf设定页面
    word_path = os.path.join(MEDIA_ROOT_N, 'input')
    output_path = os.path.join(MEDIA_ROOT_N, 'output')
    # print(word_path, output_path)
    # word_to_p(word_path, output_path)
    try:
        print(word_path,output_path)
        word_to_p(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'output/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'output')))
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('Word_to_pdf文件不存在或者格式错误')
        print(word_path,output_path)
        clear_database(request)
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':True,})
    # photos_list = Photo.objects.all()
'''

def xueya_csv_xlsx(request):  # 血压转excls
    word_path = os.path.join(MEDIA_ROOT_N, 'input')
    output_path = os.path.join(MEDIA_ROOT_N, 'output')

    try:
        xue_ya(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'output/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'output')))
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('xueya_csv_xlsx文件不存在或者格式错误')
        clear_database(request)
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()



def xindian_xlsx_xlsx(request):  # 血压转excls
    word_path = os.path.join(MEDIA_ROOT_N, 'input')
    output_path = os.path.join(MEDIA_ROOT_N, 'output')

    try:
        xin_dian(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'output/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'output')))
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('xindian_xlsx_xlsx文件不存在或者格式错误')
        clear_database(request)
        return render(request, 'UploadMulti/progress_bar_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()


def tsmtocode(request):  # tsm标签转换
    word_path = os.path.join(MEDIA_ROOT_N, 'tsminput')
    output_path = os.path.join(MEDIA_ROOT_N, 'tsmoutput')

    try:
        read_xlsx_pdf_tsm(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('tsmtocode文件不存在或者格式错误')
        clear_database_tsm(request)
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()


def tocode2612(request):  # 2612标签转换
    word_path = os.path.join(MEDIA_ROOT_N, 'tsminput')
    output_path = os.path.join(MEDIA_ROOT_N, 'tsmoutput')

    try:
        read_xlsx_pdf_2612(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('tocode2612文件不存在或者格式错误')
        clear_database_tsm(request)
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()


def tocode6236(request):  # 6236标签转换
    word_path = os.path.join(MEDIA_ROOT_N, 'tsminput')
    output_path = os.path.join(MEDIA_ROOT_N, 'tsmoutput')

    try:
        read_xlsx_pdf_6236(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('tocode6236文件不存在或者格式错误')
        clear_database_tsm(request)
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()

def tocode3512(request):  # 3512标签转换
    word_path = os.path.join(MEDIA_ROOT_N, 'tsminput')
    output_path = os.path.join(MEDIA_ROOT_N, 'tsmoutput')

    try:
        read_xlsx_pdf_3512(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('tocode3512文件不存在或者格式错误')
        clear_database_tsm(request)
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()


def tocode2515(request):  # 2515标签转换
    word_path = os.path.join(MEDIA_ROOT_N, 'tsminput')
    output_path = os.path.join(MEDIA_ROOT_N, 'tsmoutput')

    try:
        read_xlsx_pdf_2515(word_path, output_path)
        MEDIA_Path_out = MEDIA_URL_N + 'tsmoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'tsmoutput')))
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('tocode2515文件不存在或者格式错误')
        clear_database_tsm(request)
        return render(request, 'UploadMulti/tsmptscode_upload/index.html', {'Errordis':True, 'Error':True})
    # photos_list = Photo.objects.all()


def xianzhuxing11(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'xzxinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'xzxoutput')

    try:
        print('开始执行')
        xianzhuxing1(word_path, output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'xzxoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'xzxoutput')))
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':True})

def xianzhuxing12(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'xzxinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'xzxoutput')

    try:
        print('开始执行')
        xianzhuxing3(word_path, output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'xzxoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'xzxoutput')))
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':True})


def xianzhuxing13(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'xzxinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'xzxoutput')

    try:
        print('开始执行')
        xibao_xzx(word_path, output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'xzxoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'xzxoutput')))
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/xianzhuxing/index.html', {'Errordis':True, 'Error':True})

def spss_excel(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'spssinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'spssoutput')

    try:
        print('开始执行')
        read_excel(word_path, output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'spssoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'spssoutput')))
        return render(request, 'UploadMulti/spss/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/spss/index.html', {'Errordis':True, 'Error':True})

def excel_form(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'spssinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'spssoutput')

    try:
        print('开始执行')
        excel_froms(word_path,output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'spssoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'spssoutput')))
        return render(request, 'UploadMulti/spss/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/spss/index.html', {'Errordis':True, 'Error':True})


def search_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "UploadMulti/progress_bar_upload/index.html", ctx)


def get_word(request):
    word_path = os.path.join(MEDIA_ROOT_N, 'wordinput')
    output_path = os.path.join(MEDIA_ROOT_N, 'wordoutput')

    try:
        print('开始执行')
        word_to_p(word_path, output_path)

        MEDIA_Path_out = MEDIA_URL_N + 'wordoutput/'
        Photos_list2 = map(lambda x: MEDIA_Path_out + x, os.listdir(os.path.join(MEDIA_ROOT_N, 'wordoutput')))
        return render(request, 'UploadMulti/word/index.html', {'Errordis':True, 'Error':False, 'photos2': Photos_list2})

    except:
        print('what a fuck 文件不存在或者格式错误')
        clear_database_ss(request)
        return render(request, 'UploadMulti/word/index.html', {'Errordis':True, 'Error':True})