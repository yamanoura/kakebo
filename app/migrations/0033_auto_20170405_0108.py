# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-04 16:08
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0032_auto_20170405_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_date', models.DateField(blank=True, default=datetime.datetime(2017, 4, 4, 16, 8, 54, 228251, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5')),
                ('dw_type', models.CharField(choices=[(b'0', '\u5165\u91d1'), (b'1', '\u51fa\u91d1')], default=1, max_length=1, verbose_name='\u5165\u51fa\u91d1\u7a2e\u985e')),
                ('desc', models.CharField(max_length=100, verbose_name='\u8aac\u660e')),
                ('money', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999999)], verbose_name='\u91d1\u984d')),
                ('ba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BankAccount', verbose_name='\u9280\u884c\u53e3\u5ea7\u540d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='trade_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 4, 16, 8, 54, 223289, tzinfo=utc), null=True, verbose_name='\u53d6\u5f15\u65e5'),
        ),
    ]