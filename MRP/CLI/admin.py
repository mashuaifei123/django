from django.contrib import admin
from CLI.models import cliitem, cliusersinfo, clireading
from easy_select2 import select2_modelform
# Register your models here.

cliitemForm = select2_modelform(cliitem, attrs={'width': '250px'})
clireadingForm = select2_modelform(clireading, attrs={'width': '250px'})

class clireadingAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'anmailnum', 'bonemarrow', 'readingstatus', 'readingdate', 'reportdate', 'inputdate', 'update_time']
    search_fields = ('studyno__studyno', 'studyno__studydirector__username')  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['studyno__studydirector__username', 'studyno__studyno', 'readingstatus',]  # 重复字段过滤器
    list_editable = ('anmailnum', 'bonemarrow', 'readingstatus',)  # 可以编辑字段
    form = clireadingForm


class cliitemAdmin(admin.ModelAdmin):
    list_display = ['date', 'studyno',  'anmailnum', 'cbaitem',  'flowcytometry', 'hematology', 'biochemistry', 'coagulation', 'urinaryroutine', 'urinarysediment', 'pagt', 'bonemarrowsmear', 'update_time']
    search_fields = ('studyno__studyno', 'studyno__studydirector__username')  # 以那一列进行搜索
    date_hierarchy = 'date'  # 快捷选择历史的时间
    list_max_show_all = 200
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['studyno__studydirector__username', 'studyno__studyno',]  # 重复字段过滤器
    list_editable = ('anmailnum', 'cbaitem', 'flowcytometry', 'hematology', 'biochemistry', 'coagulation', 'urinaryroutine', 'urinarysediment', 'pagt', 'bonemarrowsmear',)  # 可以编辑字段
    form = cliitemForm

admin.site.register(cliitem, cliitemAdmin)
admin.site.register(cliusersinfo)
admin.site.register(clireading, clireadingAdmin)