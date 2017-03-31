# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 14:45
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170329_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalparameter',
            name='sort_no',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)], verbose_name='\u8868\u793a\u9806'),
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 29, 14, 45, 55, 29092, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='generalparameter',
            name='param1',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf1'),
        ),
        migrations.AlterField(
            model_name='generalparameter',
            name='param2',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf2'),
        ),
        migrations.AlterField(
            model_name='generalparameter',
            name='param3',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf3'),
        ),
    ]