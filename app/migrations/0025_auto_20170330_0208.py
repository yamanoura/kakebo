# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 17:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20170330_0206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalparameter',
            name='gp_name',
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 29, 17, 8, 22, 163603, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]
