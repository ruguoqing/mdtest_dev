# Generated by Django 3.2.8 on 2021-11-02 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='req_ptype',
            field=models.CharField(max_length=100, verbose_name='参数类型'),
        ),
    ]
