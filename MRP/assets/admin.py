from django.contrib import admin
from assets.models import usersinfo, deptinfo, testsystem
# Register your models here.
# from assets import asset_handler
from easy_select2 import select2_modelform


usersinfoForm = select2_modelform(usersinfo, attrs={'width': '250px'})
deptinfoForm = select2_modelform(deptinfo, attrs={'width': '250px'})
testsystemForm = select2_modelform(testsystem, attrs={'width': '250px'})


class usersinfoAdmin(admin.ModelAdmin):
    list_display = ['jobid', 'username', 'deptname', 'update_time', 'active']
    search_fields = ('jobid', 'username',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['deptname']  # 重复字段过滤器
    list_editable = ('deptname',) # 可以编辑字段
    form = usersinfoForm


class deptinfoAdmin(admin.ModelAdmin):
    list_display = ['deptname']
    search_fields = ('deptname',)  # 以那一列进行搜索
    date_hierarchy = 'create_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    form = deptinfoForm


class testsystemAdmin(admin.ModelAdmin):
    list_display = ['testsystemname']
    search_fields = ('testsystemname',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['testsystemname']  # 重复字段过滤器
    form = testsystemForm


"""
class TSMReceiveInfoAdmin(admin.ModelAdmin):
    list_display = ['Study_No', 'Name_ID_Group',
                    'TSM_status', 'Status_Date', 'Category', 'Operated_by',
                    'Date_Oper_by',
    ]
    search_fields = ('Study_No__Study_No',)  # 以那一列进行搜索
    date_hierarchy = 'Date_Oper_by'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['Study_No', 'TSM_status', 'Name_ID_Group', 'Operated_by']  # 重复字段过滤器
    list_editable = ('TSM_status', 'Status_Date', 'Operated_by') # 可以编辑字段
    # 由于Django admin默认的多对多关系(ManyToMany)选择器是复选框，非常的不好用。一个更好的方法是使用filter_horizontal或filter_vertical选项
    form = TSMReceiveInfoForm
"""

admin.site.register(usersinfo, usersinfoAdmin)
admin.site.register(deptinfo, deptinfoAdmin)
admin.site.register(testsystem,testsystemAdmin)


