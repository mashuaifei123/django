from django.contrib import admin
from QAU.models import checkingitem, checkingplan, qauusersinfo
from easy_select2 import select2_modelform

checkingplanForm = select2_modelform(checkingplan, attrs={'width': '850px'})

class checkingplanAdmin(admin.ModelAdmin):
    list_display = ['checkdate', 'studyno', 'show_item', 'person', 'update_time']
    search_fields = ('studyno__studyno', 'checkitem__checkname', 'person__username')  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 100  # 一个页面里面有多少行内容
    list_filter = ['person', 'checkitem']  # 重复字段过滤器
    # list_editable = ('person',) # 可以编辑字段
    form = checkingplanForm
    def show_item(self, obj):  # 显示项目
        item_list = []
        for item in obj.checkitem.all():  # self = checkingplan obj = checkingplan.object 之后字段名字 下面引用外键" . "的方式
            item_list.append(item.checkname)
        return ','.join(item_list)
    show_item.short_description = '检查项目'  # 设置表头
    filter_horizontal = ('checkitem',)  # 多对多，横向显示



admin.site.register(checkingplan, checkingplanAdmin)
admin.site.register(checkingitem)
admin.site.register(qauusersinfo)

