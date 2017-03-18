# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-18 00:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170318_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbook',
            name='ab_desc',
            field=models.CharField(default='\u672a\u5165\u529b', max_length=100, verbose_name='\u5e33\u7c3f\u6458\u8981'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 18, 0, 19, 53, 242062, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]
