# Generated by Django 3.2.8 on 2021-10-21 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Module',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
