from django.db import models
from django.contrib.auth.models import User



class projectinfo(models.Model):
    """ 项目信息 """
    projectnumber = models.CharField(max_length=128, null=False, unique=True, verbose_name='项目编号', default='未设定')
    projectname = models.CharField(max_length=128, null=False, unique=True, verbose_name='项目名称', default='未设定')
    sponsor = models.ForeignKey('sponsorinfo', blank=True, null=True, verbose_name='委托方', default=0, on_delete=(models.DO_NOTHING))
    contractnumber = models.ForeignKey('contractinfo', null=False, verbose_name='合同编号', default=0, on_delete=(models.DO_NOTHING))
    testtrarticlename =  models.ForeignKey('testarticleinfo', null=False, verbose_name='供试品编号', default=0, on_delete=(models.DO_NOTHING))
    projectuser = models.ForeignKey('sponsorusers', null=False, verbose_name='项目联系人', default=0, on_delete=(models.DO_NOTHING), related_name='sponsor_userp')
    businessuser = models.ForeignKey('sponsorusers', null=False, verbose_name='商务联系人', default=0, on_delete=(models.DO_NOTHING), related_name='sponsor_userb')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.projectnumber

    class Meta:
        verbose_name = '项目信息'
        verbose_name_plural = '项目信息'
        ordering = ['-update_time']


class sponsorusers(models.Model):
    """ 委托方联系人 """
    sponsorusers = models.CharField(max_length=16, null=False, unique=True, verbose_name='联系人', default='未设定')
    phoneno1 = models.CharField(max_length=64, null=False, unique=True, verbose_name='联系电话1', default='未设定')
    phoneno2 = models.CharField(max_length=64, verbose_name='联系电话2')
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False, verbose_name='电子邮件')
    insponsor = models.ForeignKey('sponsorinfo', blank=True, null=True, verbose_name='所属委托方', default=0, on_delete=(models.DO_NOTHING))
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
        
    def __str__(self):
        return self.sponsorusers

    class Meta:
        verbose_name = '委托方联系人'
        verbose_name_plural = '委托方联系人'
        ordering = ['-update_time']


class contractinfo(models.Model):
    """ 合同信息 """
    contractnumber = models.CharField(max_length=128, null=False, unique=True, verbose_name='合同编号', default='未设定')
    contractname = models.CharField(max_length=128, null=False, unique=True, verbose_name='合同名称', default='未设定')
    datesigning = models.DateField(null=False, verbose_name='签订日期')
    contractvalue = models.IntegerField(verbose_name='合同金额')
    sponsor = models.ForeignKey('sponsorinfo', blank=True, null=True, verbose_name='甲方名称', default=0, on_delete=(models.DO_NOTHING))
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.contractnumber

    class Meta:
        verbose_name = '合同信息'
        verbose_name_plural = '合同信息'
        ordering = ['-update_time']


class sponsorinfo(models.Model):
    """ 委托方信息 """
    sponsorname = models.CharField(max_length=128, null=False, unique=True, verbose_name='委托方', default='未设定')
    sponsoren = models.CharField(max_length=128, null=False, unique=True, verbose_name='委托方英文名称', default='未设定')
    innumber = models.CharField(max_length=128, null=False, unique=True, verbose_name='内部编号', default='未设定')
    address = models.CharField(max_length=128, null=False, unique=True, verbose_name='地址', default='未设定')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.sponsorname

    class Meta:
        verbose_name = '委托方信息'
        verbose_name_plural = '委托方信息'
        ordering = ['-update_time']


class testarticleinfo(models.Model):
    """ 供试品信息 """
    testtrarticlename = models.CharField(max_length=128, null=False, unique=True, verbose_name='供试品名称', default='未设定')
    testtrarticlenumber = models.CharField(max_length=128, null=False, unique=True, verbose_name='供试品编号', default='未设定')
    testtrarticleapi = models.FloatField(null=True, blank=True, max_length=128, verbose_name='供试品API-%')
    testtrarticlepcs = models.FloatField(null=True, blank=True, max_length=128, verbose_name='每pcs含量')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间') 

    def __str__(self):
        return '{} {}'.format(self.testtrarticlenumber, self.testtrarticlename)

    class Meta:
        verbose_name = '供试品信息'
        verbose_name_plural = '供试品信息'
        ordering = ['-update_time']