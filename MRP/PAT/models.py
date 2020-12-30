from django.db import models
from studys.models import studysinfo, anatomicalday
# Create your models here.

class patinfo(models.Model):
    """ 病理信息 """
    sli_status_type = ((0, '未开始'), (1, '制片中'), (2, '制片完成'))
    his_status_type = ((0, '未开始'), (1, '阅片中'), (2, '阅片完成'))

    studyno = models.ForeignKey('studys.anatomicalday', null=False, max_length=64, verbose_name='专题编号', default=0, on_delete=(models.DO_NOTHING))
    slidespreparationstatus = models.SmallIntegerField(choices=sli_status_type, default=0, verbose_name='制片状态')
    slidesdate = models.DateField(null=True, blank=True, verbose_name='制片状态变更日期')
    histopathologystatus = models.SmallIntegerField(choices=his_status_type, default=0, verbose_name='阅片状态')
    histodate = models.DateField(null=True, blank=True, verbose_name='阅片状态变更日期')
    observedby = models.ManyToManyField('patusersinfo', blank=True, verbose_name='参与人员', )
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '{}'.format(self.studyno)

    class Meta:
        verbose_name = '病理信息'
        verbose_name_plural = '病理信息'
        ordering = ['-update_time']



class patusersinfo(models.Model):
    """ PAT用户信息 """
    username = models.CharField(max_length=64, unique=True, verbose_name='用户名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username  # 显示记录时，用name来区别

    class Meta:
        verbose_name = 'PAT用户信息'
        verbose_name_plural = 'PAT用户信息'