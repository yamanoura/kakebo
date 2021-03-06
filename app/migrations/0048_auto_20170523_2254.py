# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-23 13:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20170523_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 5, 23, 13, 54, 19, 79422, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='bankaccountbalance',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 5, 23, 13, 54, 19, 78040, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='datapatternuse',
            name='trade_date',
            field=models.DateField(default=datetime.datetime(2017, 5, 23, 13, 54, 19, 87667, tzinfo=utc), verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]
