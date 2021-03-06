# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-12 19:43
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dw_type', models.CharField(choices=[(b'0', '\u5165\u91d1'), (b'1', '\u51fa\u91d1')], default=0, max_length=1, verbose_name='\u5165\u51fa\u91d1\u7a2e\u985e')),
                ('ab_desc', models.CharField(max_length=100, verbose_name='\u6458\u8981')),
                ('ab_money', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999999)], verbose_name='\u5e33\u7c3f\u91d1\u984d')),
            ],
        ),
        migrations.CreateModel(
            name='AccountTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_name', models.CharField(max_length=50, verbose_name='\u52d8\u5b9a\u79d1\u76ee\u540d')),
                ('at_type', models.CharField(choices=[(b'0', '\u5165\u91d1'), (b'1', '\u51fa\u91d1')], max_length=1, verbose_name='\u52d8\u5b9a\u79d1\u76ee\u7a2e\u985e')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ba_name', models.CharField(max_length=100, verbose_name='\u9280\u884c\u53e3\u5ea7\u540d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositWithdrawalMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dwm_name', models.CharField(max_length=50, verbose_name='\u5165\u51fa\u91d1\u65b9\u6cd5\u540d')),
                ('dwm_type', models.CharField(blank=True, choices=[(b'0', '\u73fe\u91d1'), (b'1', '\u30af\u30ec\u30b8\u30c3\u30c8'), (b'2', '\u632f\u8fbc'), (b'3', '\u53e3\u5ea7\u632f\u66ff')], default=0, max_length=1, null=True, verbose_name='\u5165\u51fa\u91d1\u65b9\u6cd5\u7a2e\u985e')),
                ('ba', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.BankAccount', verbose_name='\u9280\u884c\u53e3\u5ea7\u540d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100, verbose_name='Project\u540d')),
                ('project_desc', models.CharField(max_length=400, verbose_name='Project\u8aac\u660e')),
                ('project_status', models.CharField(choices=[(b'0', '\u8a08\u753b\u4e2d'), (b'1', '\u5229\u7528\u4e2d'), (b'2', '\u5b8c\u4e86\u6e08'), (b'9', '\u524a\u9664\u6e08')], max_length=1, verbose_name='Project\u72b6\u614b')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accountbook',
            name='at',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.AccountTitle', verbose_name='\u52d8\u5b9a\u79d1\u76ee'),
        ),
        migrations.AddField(
            model_name='accountbook',
            name='dwm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.DepositWithdrawalMethod', verbose_name='\u5165\u51fa\u91d1\u65b9\u6cd5'),
        ),
        migrations.AddField(
            model_name='accountbook',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Project', verbose_name='Project\u60c5\u5831'),
        ),
        migrations.AddField(
            model_name='accountbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
