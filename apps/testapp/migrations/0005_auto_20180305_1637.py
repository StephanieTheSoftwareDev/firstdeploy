# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-05 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_auto_20180305_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]