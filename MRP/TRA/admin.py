from django.contrib import admin
from TRA.models import tarcreates, tarinpope, tarcheckpope, sendwxlog, msggrouptable
from assets.models import usersinfo
from easy_select2 import select2_modelform
from tools.sendwx import WeChat

tarcreatesForm = select2_modelform(tarcreates, attrs={'width': '850px'})
tarinpopeForm = select2_modelform(tarinpope, attrs={'width': '850px'})
tarcheckpopeForm = select2_modelform(tarcheckpope, attrs={'width': '850px'})

class tarcreatesAdmin(admin.ModelAdmin):
    list_display = ['infoname', 'techname', 'infodept', 'addressroom', 'infodata', 'infotime', 'msgtogroup', 'author', 'update_time']
    search_fields = ('infoname', 'techname__username', 'addressroom',)  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 30  # 一个页面里面有多少行内容
    list_filter = ['techname']  # 重复字段过滤器
    # list_editable = ('techname',) # 可以编辑字段
    exclude = ('author',) # 排除编辑对象自动保存
    form = tarcreatesForm

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(tarcreatesAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return tarcreates.objects.all()
        return tarcreates.objects.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        # obj.save()
        super().save_model(request, obj, form, change)
        wx = WeChat() # 保存后修改发送.
        # 查询保存条目的用户ID
        touser_list = []
        for item in request.POST.getlist(key='msgtogroup'): # 通过request结合查询找到通知组ID反向查询到jobid工号
            jobidnum = msggrouptable.objects.filter(id=int(item)).values_list('grouppope__jobid')
            for i in list(jobidnum):
                for a in i:
                    touser_list.append(str(a))   # 加载工号
        touser = '|'.join(touser_list)
        intoname = str(obj.infoname)
        info = '您有新的培训会议需要选择参加人员'
        ds = str(obj.infods)
        techname = str(obj.techname.username)
        address = str(obj.addressroom)
        data_w = str(obj.infodata)
        time_w = str(obj.infotime)
        sendtime = str(obj.update_time)
        wx.send_data(touser, info, intoname, ds, techname, address, data_w, time_w, sendtime)
        # pid = obj.infoname.get(pk=obj.pk)
        sendwxlog.objects.create(infoname=obj, inpope=touser, class_from='新培训|会议通知')


class tarinpopeAdmin(admin.ModelAdmin):
    list_display = ['infoname', 'show_item', 'author', 'update_time']
    search_fields = ('infoname__infoname', )  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 30  # 一个页面里面有多少行内容
    exclude = ('author',) # 排除编辑对象自动保存
    form = tarinpopeForm

    def show_item(self, obj):  # 显示项目
        item_list = []
        for item in obj.inpope.all():  # self = checkingplan obj = checkingplan.object 之后字段名字 下面引用外键" . "的方式
            item_list.append(item.username)
        return ','.join(item_list)
    show_item.short_description = '应训人员'  # 设置表头

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(tarinpopeAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return tarinpope.objects.all()
        return tarinpope.objects.filter(author=request.user)

    def save_model(self, request, obj, form, change):  # 重写保存函数发送通知另存为日志并检查是否为当前用户.
        if not change:
            obj.author = request.user
        # obj.save()
        super().save_model(request, obj, form, change)

        wx = WeChat() # 保存后修改发送.
        # 查询保存条目的用户ID
        touser_list = []
        for item in request.POST.getlist(key='inpope'): # 通过request结合查询找到用户jobid工号
            touser_list.append(str(usersinfo.objects.get(id=int(item)).jobid))
        touser = '|'.join(touser_list)
        intoname = str(obj.infoname.infoname)
        info = '您有新的培训会议邀请'
        ds = str(obj.infoname.infods)
        techname = str(obj.infoname.techname.username)
        address = str(obj.infoname.addressroom)
        data_w = str(obj.infoname.infodata)
        time_w = str(obj.infoname.infotime)
        sendtime = str(obj.update_time)
        wx.send_data(touser, info, intoname, ds, techname, address, data_w, time_w, sendtime)
        # pid = obj.infoname.get(pk=obj.pk)
        sendwxlog.objects.create(infoname=obj.infoname, inpope=touser, class_from='责任人指定人员通知')



    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        复写用于多选过滤https://xieboke.net/article/242/
        """
        # db_field.name 本模型下的字段名称
        if db_field.name == "inpope":
            # 过滤
            kwargs["queryset"] = usersinfo.objects.filter(active=True)
            # filter_horizontal 保持横向展示
            from django.contrib.admin import widgets
            kwargs['widget'] = widgets.FilteredSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )
        return super(tarinpopeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    filter_horizontal = ('inpope',)  # 多对多，横向显示


class tarcheckpopeAdmin(admin.ModelAdmin):
    list_display = ['infoname', 'show_item','trainingduration', 'update_time']
    search_fields = ('infoname__infoname', )  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 30  # 一个页面里面有多少行内容
    form = tarcheckpopeForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        复写用于多选过滤https://xieboke.net/article/242/
        """
        # db_field.name 本模型下的字段名称
        if db_field.name == "checkpope":
            # 过滤
            kwargs["queryset"] = usersinfo.objects.filter(active=True)
            # filter_horizontal 保持横向展示
            from django.contrib.admin import widgets
            kwargs['widget'] = widgets.FilteredSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )
        return super(tarcheckpopeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def show_item(self, obj):  # 显示项目
        item_list = []
        for item in obj.checkpope.all():  # self = checkingplan obj = checkingplan.object 之后字段名字 下面引用外键" . "的方式
            item_list.append(item.username)
        return ','.join(item_list)
    show_item.short_description = '实训人员'  # 设置表头
    filter_horizontal = ('checkpope',)  # 多对多，横向显示


class sendwxlogAdmin(admin.ModelAdmin):
    list_display = ['infoname', 'inpope', 'class_from', 'update_time']
    search_fields = ('infoname__infoname', )  # 以那一列进行搜索
    date_hierarchy = 'update_time'  # 快捷选择历史的时间
    list_per_page = 30  # 一个页面里面有多少行内容

class msggrouptableAdmin(admin.ModelAdmin):
    filter_horizontal = ('grouppope',)  # 多对多，横向显示


admin.site.register(tarcreates, tarcreatesAdmin)
admin.site.register(tarinpope, tarinpopeAdmin)
admin.site.register(tarcheckpope, tarcheckpopeAdmin)
admin.site.register(sendwxlog, sendwxlogAdmin)
admin.site.register(msggrouptable, msggrouptableAdmin)
