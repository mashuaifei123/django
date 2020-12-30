from django.contrib import admin
from TSM.models import tsmusersinfo, tsmconfstatus, tsmreceiveinfo
# Register your models here.
from easy_select2 import select2_modelform

tsmconfstatusForm = select2_modelform(tsmconfstatus, attrs={'width': '250px'})
tsmreceiveinfoForm = select2_modelform(tsmreceiveinfo, attrs={'width': '250px'})


class tsmconfstatusAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'deliverydate', 'status', 'operatedby', 'update_time']
    search_fields = ('studyno__studyno',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['status', 'operatedby']  # 重复字段过滤器
    list_editable = ('status', 'operatedby') # 可以编辑字段
    form = tsmconfstatusForm


class tsmreceiveinfoAdmin(admin.ModelAdmin):
    list_display = ['projectno', 'nameorid', 'status', 'statusdate', 'operatedby', 'update_time']
    search_fields = ('projecton__projectnumber',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['status',  'operatedby']  # 重复字段过滤器
    list_editable = ('status', 'statusdate', 'operatedby') # 可以编辑字段
    form = tsmreceiveinfoForm


admin.site.register(tsmusersinfo)
admin.site.register(tsmconfstatus, tsmconfstatusAdmin)
admin.site.register(tsmreceiveinfo, tsmreceiveinfoAdmin)
