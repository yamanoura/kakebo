# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-22 15:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20170523_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 5, 22, 15, 15, 18, 943830, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='bankaccountbalance',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 5, 22, 15, 15, 18, 942471, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='datapatternuse',
            name='ab',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.AccountBook', verbose_name='\u5e33\u7c3f\u60c5\u5831'),
        ),
        migrations.AlterField(
            model_name='datapatternuse',
            name='trade_date',
            field=models.DateField(default=datetime.datetime(2017, 5, 22, 15, 15, 18, 952203, tzinfo=utc), verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]
