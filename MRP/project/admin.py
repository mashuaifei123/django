from django.contrib import admin
from easy_select2 import select2_modelform
from project.models import projectinfo, sponsorinfo, sponsorusers, contractinfo, testarticleinfo
# Register your models here.

projectinfoForm = select2_modelform(projectinfo, attrs={'width': '250px'})
sponsorinfoForm = select2_modelform(sponsorinfo, attrs={'width': '250px'})
sponsorusersForm = select2_modelform(sponsorusers, attrs={'width': '250px'})
contractinfoForm = select2_modelform(contractinfo, attrs={'width': '250px'})


class projectinfoAdmin(admin.ModelAdmin):
    list_display = ['projectnumber', 'projectname', 'sponsor', 'contractnumber', 'testtrarticlename', 'projectuser', 'businessuser']
    search_fields = ('projectnumber', 'projectname', 'sponsor', 'contractnumber', 'testtrarticlename', 'projectuser', 'businessuser')  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['sponsor',]  # 重复字段过滤器
    list_editable = ('sponsor', 'testtrarticlename', 'projectuser', 'businessuser') # 可以编辑字段
    form = projectinfoForm

class sponsorinfoAdmin(admin.ModelAdmin):
    list_display = ['sponsorname', 'sponsoren', 'innumber', 'address', 'update_time', ]
    search_fields = ('sponsorname', 'sponsoren', 'innumber',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['remarks',]  # 重复字段过滤器
    list_editable = ('sponsoren', 'innumber', 'address',) # 可以编辑字段
    form = sponsorinfoForm

class sponsorusersAdmin(admin.ModelAdmin):
    list_display = ['sponsorusers', 'phoneno1', 'phoneno2', 'email', 'insponsor', 'update_time']
    search_fields = ('sponsorusers', 'phoneno1', 'phoneno2', 'email', 'insponsor', )  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['insponsor',]  # 重复字段过滤器
    list_editable = ('insponsor',) # 可以编辑字段
    form = sponsorusersForm

class contractinfoAdmin(admin.ModelAdmin):
    list_display = ['contractname', 'contractnumber', 'datesigning', 'contractvalue', 'sponsor', 'update_time']
    search_fields = ('contractname', 'contractnumber','sponsor' )  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['sponsor']  # 重复字段过滤器
    list_editable = ('sponsor',) # 可以编辑字段
    form = contractinfoForm


admin.site.register(projectinfo, projectinfoAdmin)
admin.site.register(sponsorinfo, sponsorinfoAdmin)
admin.site.register(sponsorusers, sponsorusersAdmin)
admin.site.register(contractinfo, contractinfoAdmin)
admin.site.register(testarticleinfo)