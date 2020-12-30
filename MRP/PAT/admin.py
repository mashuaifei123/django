from django.contrib import admin
from PAT.models import patinfo, patusersinfo
from easy_select2 import select2_modelform

patinfoForm = select2_modelform(patinfo, attrs={'width': '850px'})

class patinfoAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'slidespreparationstatus', 'slidesdate', 'histopathologystatus', 'histodate', 'update_time']
    search_fields = ('studyno__studyno__studyno',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['slidespreparationstatus', 'histopathologystatus']  # 重复字段过滤器
    list_editable = ('slidespreparationstatus', 'slidesdate', 'histopathologystatus','histodate') # 可以编辑字段
    form = patinfoForm


admin.site.register(patinfo, patinfoAdmin)
admin.site.register(patusersinfo)

