# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0013_auto_20151229_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='rezervacija',
            name='stolovi',
            field=models.ManyToManyField(blank=True, to='restoran.Sto'),
        ),
    ]