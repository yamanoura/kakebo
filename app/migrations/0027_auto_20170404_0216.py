# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-03 17:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20170330_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositwithdrawalmethod',
            name='closing_deadline',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='\u7de0\u3081\u65e5'),
        ),
        migrations.AddField(
            model_name='depositwithdrawalmethod',
            name='pay_deadline',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='\u652f\u6255\u671f\u65e5(\u5f15\u843d\u65e5)'),
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 3, 17, 16, 5, 266306, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='accountbookplan',
            name='plan_year_month',
            field=models.CharField(default=b'2017-04', max_length=7, verbose_name='\u4e88\u5b9a\u5e74\u6708'),
        ),
    ]
