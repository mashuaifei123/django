from django.contrib import admin
from studys.models import studysinfo, studysprogressstatus, studyproperty, sdmanager, phase, anatomicalday, studydays, studyitem, itemindept, studyplansetting
from easy_select2 import select2_modelform

studysinfoForm = select2_modelform(studysinfo, attrs={'width': '450px'})
studysprogressstatusForm = select2_modelform(studysprogressstatus, attrs={'width': '450px'})
sdmanagerForm = select2_modelform(sdmanager, attrs={'width': '450px'})
anatomicaldayForm = select2_modelform(anatomicalday, attrs={'width': '450px'})
studydaysForm = select2_modelform(studydays, attrs={'width': '450px'})
itemindeptForm = select2_modelform(itemindept, attrs={'width': '450px'})
studyplansettingForm = select2_modelform(studyplansetting, attrs={'width': '450px'})

class studydaysAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'ptsdays', 'datedays', 'weekday', 'weekno', 'phasedays', 'itemname', 'itemactive', 'remarks']
    search_fields = ('studyno__studyno', 'studyno__studydirector__username', 'datedays', 'itemname__itemname')  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['itemname',]  # 重复字段过滤器
    # list_editable = ('phasename','dates', 'anmailnum') # 可以编辑字段
    form = studydaysForm


class anatomicaldayAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'phasename', 'dates', 'anmailnum', 'update_time']
    search_fields = ('studyno__studyno',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['phasename',]  # 重复字段过滤器
    list_editable = ('phasename','dates', 'anmailnum') # 可以编辑字段
    form = anatomicaldayForm


class studysinfoAdmin(admin.ModelAdmin):
    list_display = ['studyno', 'studyname', 'studydirector', 'projectno', 'update_time']
    search_fields = ('studyno', 'studyno', 'studydirector__username',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['studydirector', 'projectno',]  # 重复字段过滤器
    list_editable = ('studydirector',) # 可以编辑字段
    form = studysinfoForm

class studysprogressstatusAdmin(admin.ModelAdmin):
    list_display = ['studyno',
                    'sdappointdate',
                    'initiationdate',
                    'teststartdate',
                    'firstexposuredate',
                    'lastexposuredate',
                    'anatomicaldate',
                    'testenddate',
                    'studycompletiondate',
                    'studystatus',
                    'update_time',]
    search_fields = ('studyno__studyno',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['studystatus']  # 重复字段过滤器
    form = studysprogressstatusForm


class sdmanagerAdmin(admin.ModelAdmin):
    list_display = ['studyno',
                    'biganimald',
                    'bmreportd',
                    'patreportd',
                    'tkadareportd',
                    'summaryreportd',
                    'returnd',
                    'dateqad',
                    'qareturnd',
                    'Finalsignatured',
                    'archived',
                    'update_time',]
    search_fields = ('studyno__studyno','studyno__studydirector__username')  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['studyno__studydirector__username']  # 重复字段过滤器
    form = sdmanagerForm

class studyplansettingAdmin(admin.ModelAdmin):
    list_display = ['studyno',
                    'ddwzljsd',
                    'gsbgd',
                    'patd',
                    'tkadad',
                    'sumrepd',
                    'wtfcfd',
                    'sdwtfcfd',
                    'sendqad',
                    'sdsendqad',
                    'qared',
                    'sdqareturnd',
                    'finalrd',
                    'sdfinalrd',
                    'activedd',
                    'sdactivedd',
                    'update_time']
    search_fields = ('studyno__studyno',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 15  # 一个页面里面有多少行内容
    list_filter = ['studyno__studydirector__username']  # 重复字段过滤器
    list_editable = ('ddwzljsd',
                    'gsbgd',
                    'patd',
                    'tkadad',
                    'sumrepd',
                    'wtfcfd',
                    'sdwtfcfd',
                    'sendqad',
                    'sdsendqad',
                    'qared',
                    'sdqareturnd',
                    'finalrd',
                    'sdfinalrd',
                    'activedd',
                    'sdactivedd',) # 可以编辑字段
    form = studyplansettingForm



class itemindeptAdmin(admin.ModelAdmin):
    form = itemindeptForm

admin.site.register(studysinfo, studysinfoAdmin)
admin.site.register(studysprogressstatus, studysprogressstatusAdmin)
admin.site.register(studyproperty)
admin.site.register(sdmanager, sdmanagerAdmin)
admin.site.register(anatomicalday, anatomicaldayAdmin)
admin.site.register(studydays, studydaysAdmin)
admin.site.register(phase)
admin.site.register(studyitem)
admin.site.register(itemindept, itemindeptAdmin)
admin.site.register(studyplansetting, studyplansettingAdmin)


