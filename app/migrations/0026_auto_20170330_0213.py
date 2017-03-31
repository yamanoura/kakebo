# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 17:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20170330_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalparameter',
            name='name',
            field=models.CharField(default=None, max_length=20, verbose_name='\u6c4e\u7528\u30d1\u30e9\u30e1\u30fc\u30bf\u540d'),
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 29, 17, 13, 5, 163167, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]
