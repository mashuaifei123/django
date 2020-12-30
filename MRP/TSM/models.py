from django.db import models
# Create your models here.
from project.models import projectinfo, testarticleinfo
from studys.models import studysinfo


class tsmusersinfo(models.Model):
    """ TSM用户信息 """
    username = models.CharField(max_length=64, unique=True, verbose_name='用户名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username  # 显示记录时，用name来区别

    class Meta:
        verbose_name = 'TSM用户信息'
        verbose_name_plural = 'TSM用户信息'




class tsmconfstatus(models.Model):
    """ 供试品配置状态 """
    TSM_status_type = ((0, '未完成'), (1, '已配待领'), (2, '已领取'), (3, '已返还'))
    studyno = models.ForeignKey('studys.studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    deliverydate = models.DateField(null=False, verbose_name='领药日期')
    status = models.SmallIntegerField(choices=TSM_status_type, default=0, verbose_name='状态')
    operatedby = models.ForeignKey('tsmusersinfo', blank=True, null=True, default=0, verbose_name='操作者', on_delete=(models.DO_NOTHING))
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    
    def __str__(self):
        return '<%s> %s' % (self.studyno, self.get_status_display())

    class Meta:
        verbose_name = 'TSM供试品配置状态'
        verbose_name_plural = 'TSM供试品配置状态表'
        ordering = ['-update_time']



class tsmreceiveinfo(models.Model):
    """ 供试品接收信息 """
    TSM_status_type = ((0, '预试样已接收'), (1, '正式样已接收'), (2, '已剩余处理'), (3, '未知'))
    projectno = models.ForeignKey('project.projectinfo', null=False, verbose_name='项目编号', default=0, on_delete=(models.DO_NOTHING))
    nameorid = models.ForeignKey('project.testarticleinfo', null=False, max_length=64, verbose_name='供试品名称/代号', default=0, on_delete=(models.DO_NOTHING))
    status = models.SmallIntegerField(choices=TSM_status_type, default=0, verbose_name='状态')
    statusdate = models.DateField(null=False, verbose_name='状态变更日期')
    operatedby = models.ForeignKey('tsmusersinfo', blank=True, null=True, verbose_name='操作者', on_delete=(models.DO_NOTHING))
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    

    def __str__(self):
        return '<%s> %s  %s' % (self.projectno, self.nameorid, self.get_status_display())

    class Meta:
        verbose_name = 'TSM供试品接收信息'
        verbose_name_plural = 'TSM供试品接收信息'
        ordering = ['-update_time']