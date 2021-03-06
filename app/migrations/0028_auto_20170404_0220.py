# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-03 17:20
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20170404_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 3, 17, 20, 57, 570721, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
        migrations.AlterField(
            model_name='depositwithdrawalmethod',
            name='closing_deadline',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='\u7de0\u3081\u65e5'),
        ),
        migrations.AlterField(
            model_name='depositwithdrawalmethod',
            name='pay_deadline',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='\u652f\u6255\u671f\u65e5(\u5f15\u843d\u65e5)'),
        ),
    ]
