# Generated by Django 3.1 on 2020-08-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmg', '0006_remove_operationlog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlog',
            name='operationtype',
            field=models.SmallIntegerField(choices=[(1, '新增设备'), (2, '编辑设备'), (3, '删除设备'), (4, '登陆系统')], default='4', verbose_name='操作类型'),
        ),
    ]
