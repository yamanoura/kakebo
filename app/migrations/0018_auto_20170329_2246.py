# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 13:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20170329_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalparameter',
            name='desc',
            field=models.CharField(default=None, max_length=100, verbose_name='\u8aac\u660e'),
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 29, 13, 46, 42, 482597, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]