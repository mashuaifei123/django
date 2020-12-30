from django.db import models
from django.contrib.auth.models import User
from assets.models import usersinfo, deptinfo

# Create your models here.

class tarcreates(models.Model):
    """ 培训发起 """      
    infoname = models.CharField(max_length=256, verbose_name='培训主题')
    techname = models.ForeignKey('assets.usersinfo', verbose_name='主讲人', on_delete=(models.DO_NOTHING))
    infods = models.CharField(max_length=256, null=True, blank=True, verbose_name='描述')
    addressroom = models.CharField(max_length=256, verbose_name='会议地点', default='1128')
    infodept = models.ForeignKey('assets.deptinfo', verbose_name='组织部门', on_delete=(models.DO_NOTHING))
    infodata = models.DateField(verbose_name='培训日期')
    infotime = models.TimeField(verbose_name='开始时间')
    msgtogroup = models.ForeignKey('msggrouptable', verbose_name='通知组', default=0, on_delete=(models.DO_NOTHING))
    author = models.ForeignKey(User, related_name='entriesceratuser_id', verbose_name='创建人', on_delete=(models.DO_NOTHING))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}-{}-{}-{}'.format(self.infoname, self.techname, self.infodept, self.infodata)

    class Meta:
        verbose_name = '培训发起'
        verbose_name_plural = '培训发起'
        ordering = ['-update_time']


class tarinpope(models.Model):
    """ 应参培训人员 """      
    infoname = models.ForeignKey('tarcreates', max_length=256, verbose_name='培训主题', on_delete=(models.DO_NOTHING))
    inpope = models.ManyToManyField('assets.usersinfo', related_name='inuser_id', blank=False, verbose_name='应训人员', default=0)
    author = models.ForeignKey(User, related_name='entriesinuser_id', verbose_name='创建人', on_delete=(models.DO_NOTHING))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.infoname)

    class Meta:
        verbose_name = '应参培训人员'
        verbose_name_plural = '应参培训人员'
        ordering = ['-update_time']


class tarcheckpope(models.Model):
    """ 实参培训人员 """      
    infoname = models.OneToOneField('tarcreates', max_length=256, verbose_name='培训主题', on_delete=(models.DO_NOTHING))
    checkpope = models.ManyToManyField('assets.usersinfo', related_name='checkuser_id', blank=False, verbose_name='实训人员', default=0)
    trainingduration = models.DecimalField(default=0.5, verbose_name='培训时长(h)', max_digits=3, decimal_places=1)
    remarks = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.infoname)

    class Meta:
        verbose_name = '实参培训人员'
        verbose_name_plural = '实参培训人员'
        ordering = ['-update_time']



class sendwxlog(models.Model):
    """ 企业微信通知日志 """
    infoname = models.ForeignKey('tarcreates', max_length=256, verbose_name='培训主题', on_delete=(models.DO_NOTHING))
    inpope = models.CharField(max_length=10240, null=True, blank=True, verbose_name='信息接受人员')
    class_from = models.CharField(max_length=128, null=True, blank=True, verbose_name='信息发送类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.infoname)

    class Meta:
        verbose_name = '通知日志'
        verbose_name_plural = '通知日志'
        ordering = ['-update_time']


class msggrouptable(models.Model):
    """ 通知组 """
    groupname = models.CharField(max_length=128,verbose_name='组名称')
    grouppope = models.ManyToManyField('assets.usersinfo', related_name='msgusergroup_id', verbose_name='组成员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.groupname)

    class Meta:
        verbose_name = '通知组'
        verbose_name_plural = '通知组'
        ordering = ['-update_time']