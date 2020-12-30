# Generated by Django 2.2.2 on 2019-12-24 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contractinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractnumber', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='合同编号')),
                ('contractname', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='合同名称')),
                ('datesigning', models.DateField(verbose_name='签订日期')),
                ('contractvalue', models.IntegerField(verbose_name='合同金额')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '合同信息',
                'verbose_name_plural': '合同信息',
                'ordering': ['-update_time'],
            },
        ),
        migrations.CreateModel(
            name='sponsorinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsorname', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='委托方')),
                ('sponsoren', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='委托方英文名称')),
                ('innumber', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='内部编号')),
                ('address', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='地址')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '委托方信息',
                'verbose_name_plural': '委托方信息',
                'ordering': ['-update_time'],
            },
        ),
        migrations.CreateModel(
            name='testarticleinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testtrarticlename', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='供试品名称')),
                ('testtrarticlenumber', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='供试品编号')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '供试品信息',
                'verbose_name_plural': '供试品信息',
                'ordering': ['-update_time'],
            },
        ),
        migrations.CreateModel(
            name='sponsorusers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsorusers', models.CharField(default='未设定', max_length=16, unique=True, verbose_name='联系人')),
                ('phoneno1', models.CharField(default='未设定', max_length=64, unique=True, verbose_name='联系电话1')),
                ('phoneno2', models.CharField(max_length=64, verbose_name='联系电话2')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='电子邮件')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('insponsor', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.sponsorinfo', verbose_name='所属委托方')),
            ],
            options={
                'verbose_name': '委托方联系人',
                'verbose_name_plural': '委托方联系人',
                'ordering': ['-update_time'],
            },
        ),
        migrations.CreateModel(
            name='projectinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectnumber', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='项目编号')),
                ('projectname', models.CharField(default='未设定', max_length=128, unique=True, verbose_name='项目名称')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('businessuser', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsor_userb', to='project.sponsorusers', verbose_name='商务联系人')),
                ('contractnumber', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='project.contractinfo', verbose_name='合同编号')),
                ('projectuser', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsor_userp', to='project.sponsorusers', verbose_name='项目联系人')),
                ('sponsor', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.sponsorinfo', verbose_name='委托方')),
                ('testtrarticlename', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='project.testarticleinfo', verbose_name='供试品编号')),
            ],
            options={
                'verbose_name': '项目信息',
                'verbose_name_plural': '项目信息',
                'ordering': ['-update_time'],
            },
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='sponsor',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.sponsorinfo', verbose_name='甲方名称'),
        ),
    ]
