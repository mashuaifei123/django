from django.db import models
from studys.models import studysinfo
 
class checkingplan(models.Model):
    """ 检查计划 """

    checkdate = models.DateField(verbose_name='检查日期')
    studyno = models.ForeignKey('studys.studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    checkitem = models.ManyToManyField('checkingitem', max_length=256, verbose_name='检查项目')
    person = models.ForeignKey('qauusersinfo', verbose_name='责任人', default=0, on_delete=(models.DO_NOTHING))
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '检查计划'
        verbose_name_plural = '检查计划'
        ordering = ['-update_time']


class checkingitem(models.Model):
    '''检查项目'''
    checkname = models.CharField(max_length=256, unique=True, verbose_name='项目名称', default='未设定')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.checkname

    class Meta:
        verbose_name = '检查项目'
        verbose_name_plural = '检查项目'
        ordering = ['-update_time']


class qauusersinfo(models.Model):
    """ QAU用户信息 """
    username = models.CharField(max_length=64, unique=True, verbose_name='用户名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username  # 显示记录时，用name来区别

    class Meta:
        verbose_name = 'QAU用户信息'
        verbose_name_plural = 'QAU用户信息'