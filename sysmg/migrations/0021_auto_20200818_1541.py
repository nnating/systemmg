# Generated by Django 3.1 on 2020-08-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmg', '0020_auto_20200818_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlog',
            name='operationtype',
            field=models.IntegerField(choices=[(1, '新增设备'), (2, '编辑设备'), (3, '删除设备'), (4, '登陆系统'), (5, '新增用户'), (6, '编辑用户'), (7, '删除用户'), (8, '用户注册'), (9, '导入设备')]),
        ),
    ]
