# Generated by Django 2.2.2 on 2020-06-03 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20200603_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersinfo',
            name='jobid',
            field=models.IntegerField(blank=True, default=17610, help_text='请输入工号', null=True, verbose_name='工号'),
        ),
    ]