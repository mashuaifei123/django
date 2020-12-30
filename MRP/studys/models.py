from django.db import models
from django.contrib.auth.models import User
from assets.models import usersinfo, testsystem
from project.models import projectinfo

class studysinfo(models.Model):
    """ 专题信息 """
    studyno = models.CharField(max_length=128, null=False, unique=True, verbose_name='专题编号', default='未设定')
    studyname =  models.CharField(max_length=128, null=False, unique=True, verbose_name='专题名称', default='未设定')
    studydirector = models.ForeignKey('assets.usersinfo', blank=False, null=False, default=0, verbose_name='专题负责人', on_delete=(models.DO_NOTHING))
    projectno = models.ForeignKey('project.projectinfo', null=False, verbose_name='项目编号', default=0, on_delete=(models.DO_NOTHING))
    testsystem = models.ForeignKey('assets.testsystem', null=False, verbose_name='试验系统', default=0, on_delete=(models.DO_NOTHING))
    anmailnum = models.PositiveSmallIntegerField(verbose_name='动物数量', default=0)
    animalsource = models.CharField(max_length=128, null=False, verbose_name='动物来源', default='未设定')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{} {} {}'.format(self.studyno, self.studyname, self.studydirector)

    def __unicode__(self):
        return self.studyno  # 显示记录时，用name来区别

    class Meta:
        verbose_name = '专题信息'
        verbose_name_plural = '专题信息'
        ordering = ['-update_time']


class studysprogressstatus(models.Model):
    """ 专题进展状态 """
    status_type = ((0, '未完成'), (1, '终止'), (2, '进行中'), (3, '未开始'))
    studyno = models.OneToOneField('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    sdappointdate = models.DateField(null=False, verbose_name='SD任命签发日期')
    initiationdate = models.DateField(null=False, verbose_name='专题启动日期')
    teststartdate = models.DateField(null=False, verbose_name='试验开始日期')
    firstexposuredate = models.DateField(null=False, verbose_name='首次给药日期')
    lastexposuredate = models.DateField(null=False, verbose_name='末次给药日期')
    anatomicaldate = models.DateField(null=False, verbose_name='解剖日期')
    testenddate = models.DateField(null=False, verbose_name='试验结束日期')
    studycompletiondate = models.DateField(null=False, verbose_name='专题完成日期')
    studystatus = models.SmallIntegerField(choices=status_type, default=0, verbose_name='专题状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{} {}'.format(self.studyno, self.get_studystatus_display())

    class Meta:
        verbose_name = '专题进展状态'
        verbose_name_plural = '专题进展状态'
        ordering = ['-update_time']


class studyproperty(models.Model):
    """ 专题属性 """

    studyno = models.OneToOneField('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    anmailnum = models.PositiveSmallIntegerField(verbose_name='动物数量', default=1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{} {}'.format(self.studyno, self.anmailnum)

    class Meta:
        verbose_name = '专题属性'
        verbose_name_plural = '专题属性'
        ordering = ['-update_time']


class sdmanager(models.Model):
    """ 毒理部专题管理 """

    studyno = models.OneToOneField('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    biganimald = models.DateField(null=True, blank=True, verbose_name='大动物资料接受日期')
    bmreportd = models.DateField(null=True, blank=True, verbose_name='骨髓报告日期')
    patreportd = models.DateField(null=True, blank=True, verbose_name='病理报告初稿日期')
    tkadareportd = models.DateField(null=True, blank=True, verbose_name='TK/ADA报告日期')
    summaryreportd = models.DateField(null=True, blank=True,  verbose_name='总结报告初稿日期')
    returnd = models.DateField(null=True, blank=True, verbose_name='委托方初稿/返还日期')
    dateqad = models.DateField(null=True, blank=True, verbose_name='资料递交QA日期')
    qareturnd = models.DateField(null=True, blank=True, verbose_name=' QA返还日期')
    Finalsignatured = models.DateField(null=True, blank=True, verbose_name=' 终版报告签字日期')
    archived = models.DateField(null=True, blank=True, verbose_name='归档日期')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '毒理部专题管理'
        verbose_name_plural = '毒理部专题管理'
        ordering = ['-update_time']


class studyplansetting(models.Model):
    """专题计划时间计算设定"""

    studyno = models.OneToOneField('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    ddwzljsd = models.PositiveSmallIntegerField(verbose_name='大动物资料接受天', blank=False, default=7)
    gsbgd = models.PositiveSmallIntegerField(verbose_name='骨髓报告天', blank=False, default=45)
    patd = models.PositiveSmallIntegerField(verbose_name='病理报告初稿天', blank=False, default=45)
    tkadad = models.PositiveSmallIntegerField(verbose_name='TK/ADA报告天', blank=False, default=45)
    sumrepd = models.PositiveSmallIntegerField(verbose_name='总结报告初稿天', blank=False, default=60)
    wtfcfd = models.PositiveSmallIntegerField(verbose_name='委托方初稿/返还天', blank=False, default=65)
    sdwtfcfd = models.PositiveSmallIntegerField(verbose_name='预计-委托方初稿/返还天', blank=False, default=5)
    sendqad = models.PositiveSmallIntegerField(verbose_name='资料递交QA天', blank=False, default=67)
    sdsendqad = models.PositiveSmallIntegerField(verbose_name='预计-资料递交QA天', blank=False, default=2)
    qared = models.PositiveSmallIntegerField(verbose_name='QA返还天', blank=False, default=80)
    sdqareturnd = models.PositiveSmallIntegerField(verbose_name='预计-QA返还天', blank=False, default=14)
    finalrd = models.PositiveSmallIntegerField(verbose_name='终版报告签字天', blank=False, default=90)
    sdfinalrd = models.PositiveSmallIntegerField(verbose_name='预计-终版报告签字天', blank=False, default=9)
    activedd = models.PositiveSmallIntegerField(verbose_name='归档天', blank=False, default=104)
    sdactivedd = models.PositiveSmallIntegerField(verbose_name='预计-归档天', blank=False, default=14)
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '专题计划完成设定'
        verbose_name_plural = '专题计划完成设定'
        ordering = ['-update_time']

class phase(models.Model):
    '''阶段信息'''
    phasename = models.CharField(max_length=64, unique=True, verbose_name='阶段名称', default='未设定')

    def __str__(self):
        return self.phasename

    class Meta:
        verbose_name = '阶段名称'
        verbose_name_plural = '阶段名称'



class anatomicalday(models.Model):
    '''解剖日程'''
    studyno = models.ForeignKey('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    phasename = models.ForeignKey('phase', null=False, max_length=64, verbose_name='阶段', default=0, on_delete=(models.DO_NOTHING))
    dates = models.DateField(null=False, verbose_name='解剖日期')
    anmailnum = models.PositiveSmallIntegerField(verbose_name='动物数量', default=1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}-{}-日期:{}-动物数量:{}'.format(self.studyno, self.phasename, self.dates, self.anmailnum)

    class Meta:
        verbose_name = '解剖日程'
        verbose_name_plural = '解剖日程'
        ordering = ['-update_time']


class studyitem(models.Model):
    """ 试验操作名称 """
    itemname = models.CharField(max_length=64, unique=True, verbose_name='操作名称', default='未设定')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.itemname)

    class Meta:
        verbose_name = '试验操作名称'
        verbose_name_plural = '试验操作名称'

class itemindept(models.Model):
    """ 部门试验操作关系 """
    deptname = models.OneToOneField('assets.deptinfo', unique=True, null=False, max_length=64, verbose_name='部门名称', default=0, on_delete=(models.DO_NOTHING))
    deptitem = models.ManyToManyField('studyitem', blank=True, verbose_name='试验项目')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.deptname)

    class Meta:
        verbose_name = '部门试验操作关系'
        verbose_name_plural = '部门试验操作关系'

class studydays(models.Model):
    '''专题日程信息'''
    
    studyno = models.ForeignKey('studysinfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    ptsdays = models.CharField(max_length=64, verbose_name='Pristima日程')
    datedays = models.DateField(verbose_name='日程日期')
    weekday = models.CharField(max_length=16, verbose_name='星期')
    weekno = models.PositiveSmallIntegerField('周', default=1)
    phasedays = models.CharField(max_length=64, verbose_name='试验阶段')
    sex = models.CharField(max_length=16, verbose_name='性别')
    itemname = models.ForeignKey('studyitem', null=False, max_length=64, default=0, on_delete=(models.DO_NOTHING), verbose_name='试验操作')
    itemactive = models.CharField(max_length=64, verbose_name='操作内容')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '专题日程信息'
        verbose_name_plural = '专题日程信息'
        ordering = ['-update_time']




"""
class Study_stdate(models.Model):
    '''专题时间安排'''
    Study_No = models.OneToOneField('assets.StudyInfo', unique=True, null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    Study_StartDate = models.DateField(null=False, verbose_name='专题开始日期')
    Study_stopDate = models.DateField(null=False, verbose_name='专题结束日期')

    def __str__(self):
        return '{} {} {}'.format(self.Study_No, self.Study_StartDate, self.Study_stopDate)

    class Meta:
        verbose_name = '专题时间安排'
        verbose_name_plural = '专题时间安排'


class PTS_Phase(models.Model):
    '''阶段信息'''
    Study_No = models.ForeignKey('assets.StudyInfo', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    Pristima_phase = models.ForeignKey('Study_Phase_days', null=False, max_length=64, verbose_name='阶段', default=0, on_delete=(models.DO_NOTHING))
    Days_num = models.PositiveSmallIntegerField('days', default=1)

    def __str__(self):
        return '{} {}'.format(self.Pristima_phase, self.Days_num)

    class Meta:
        verbose_name = '阶段时间安排'
        verbose_name_plural = '阶段时间安排'


class Study_Phase_days(models.Model):
    '''阶段信息分段时间'''
    Phase_name = models.CharField(max_length=64, unique=True, verbose_name='阶段名称', default='未设定')

    def __str__(self):
        return self.Phase_name

    class Meta:
        verbose_name = '阶段名称'
        verbose_name_plural = '阶段名称'


class Program_name(models.Model):
    '''程序-操作名称'''
    Pro_name = models.CharField(max_length=64, unique=True, verbose_name='操作名称', default='未设定')
    
    def __str__(self):
        return self.Pro_name

    class Meta:
        verbose_name = '程序-操作名称'
        verbose_name_plural = '程序-操作名称'

"""