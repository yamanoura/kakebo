# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-12 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=100)),
                ('menu_desc', models.CharField(max_length=400)),
                ('menu_url', models.CharField(max_length=400)),
                ('menu_status', models.CharField(choices=[('0', 'USE'), ('1', 'DELETE')], max_length=1)),
            ],
        ),
    ]
