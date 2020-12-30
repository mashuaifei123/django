
from django.db import models
from django.contrib.auth.models import User

class usersinfo(models.Model):
    """ 用户信息 """

    jobid = models.IntegerField(null=True, blank=True, unique=False, verbose_name='工号', default=17610, help_text='请输入工号')
    username = models.CharField(max_length=64, unique=True, verbose_name='用户名称')
    deptname = models.ForeignKey('deptinfo', null=True, blank=True, verbose_name='部门名称', on_delete=(models.DO_NOTHING))
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='系统用户', on_delete=models.SET_NULL)
    active = models.BooleanField(verbose_name='是否启用', default=True,)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return '{}-{}-{}'.format(self.jobid, self.username, self.deptname)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class deptinfo(models.Model):
    """ 部门信息 """
    deptname = models.CharField(max_length=64, unique=True, verbose_name='部门名称', default='未设定')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.deptname

    class Meta:
        verbose_name = '部门信息'
        verbose_name_plural = '部门信息'


class testsystem(models.Model):
    """ 试验系统 """
    testsystemname = models.CharField(max_length=64, unique=True, verbose_name='试验系统名称', default='未设定')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.testsystemname

    class Meta:
        verbose_name = '试验系统'
        verbose_name_plural = '试验系统'


