# Generated by Django 3.1 on 2020-08-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmg', '0015_auto_20200814_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admintype',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]