# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 13:41
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_auto_20170325_0509'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param1', models.CharField(max_length=10, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf1')),
                ('param2', models.CharField(max_length=10, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf2')),
                ('param3', models.CharField(max_length=10, verbose_name='\u30d1\u30e9\u30e1\u30fc\u30bf3')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 3, 29, 13, 41, 18, 343478, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]