# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 14:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0008_auto_20151222_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poseta',
            name='ocenjen',
        ),
    ]
