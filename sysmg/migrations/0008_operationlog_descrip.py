# Generated by Django 3.1 on 2020-08-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmg', '0007_auto_20200813_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationlog',
            name='descrip',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
