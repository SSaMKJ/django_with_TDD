# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 08:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20171103_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
