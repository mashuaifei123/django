from django.db import models
from studys.models import studysinfo
# Create your models here.

class cliitem(models.Model):
    """ 临检项目 """
    date = models.DateField(null=False, verbose_name='日期')
    studyno = models.ForeignKey('studys.studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    dutyofficer = models.ManyToManyField('cliusersinfo', blank=False, verbose_name='值班人员', )
    anmailnum = models.PositiveSmallIntegerField(verbose_name='动物数量', default=0)
    cbaitem = models.PositiveSmallIntegerField(verbose_name='CBA', default=0)
    flowcytometry = models.PositiveSmallIntegerField(verbose_name='流式', default=0)
    hematology = models.PositiveSmallIntegerField(verbose_name='血液学', default=0)
    biochemistry = models.PositiveSmallIntegerField(verbose_name='生化', default=0)
    coagulation = models.PositiveSmallIntegerField(verbose_name='凝血', default=0)
    urinaryroutine = models.PositiveSmallIntegerField(verbose_name='尿常规', default=0)
    urinarysediment = models.PositiveSmallIntegerField(verbose_name='尿沉渣', default=0)
    pagt = models.PositiveSmallIntegerField(verbose_name='PAgT', default=0)
    bonemarrowsmear = models.PositiveSmallIntegerField(verbose_name='骨髓涂片', default=0)
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    remarks1 = models.TextField(null=True, blank=True, verbose_name='注意1')
    remarks2 = models.TextField(null=True, blank=True, verbose_name='注意2')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '临检项目'
        verbose_name_plural = '临检项目'
        ordering = ['-update_time']


class clireading(models.Model):
    """ 临检阅片 """
    obs_status_type = ((0, '不阅片'), (1, '待阅片'), (2, '阅片中'), (3, '阅片完成'), (4, '待定'))
    bone_status_type = ((0, '不制片'), (1, '制片'))
    studyno = models.ForeignKey('studys.studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    anmailnum = models.PositiveSmallIntegerField(verbose_name='动物数量', default=0)
    bonemarrow = models.SmallIntegerField(choices=bone_status_type, default=0, verbose_name='骨髓制片')
    readingstatus = models.SmallIntegerField(choices=obs_status_type, default=0, verbose_name='阅片状态')
    observedby = models.ManyToManyField('cliusersinfo', blank=False, verbose_name='阅片人员', )
    readingdate = models.DateField(null=True, blank=True, verbose_name='阅片日期')
    reportdate = models.DateField(null=True, blank=True, verbose_name='报告日期')
    inputdate = models.DateField(null=True, blank=True, verbose_name='归档日期')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{} {} {}'.format(self.studyno, self.readingstatus, self.observedby)

    class Meta:
        verbose_name = '临检阅片'
        verbose_name_plural = '临检阅片'
        ordering = ['-update_time']



class cliusersinfo(models.Model):
    """ CLI用户信息 """
    username = models.CharField(max_length=64, unique=True, verbose_name='用户名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username  # 显示记录时，用name来区别

    class Meta:
        verbose_name = 'CLI用户信息'
        verbose_name_plural = 'CLI用户信息'