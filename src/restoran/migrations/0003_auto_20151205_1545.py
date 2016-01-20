# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0002_auto_20151203_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='restoran',
            name='adresa',
            field=models.CharField(default=b'', max_length=70),
        ),
        migrations.AddField(
            model_name='restoran',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='restoran',
            name='lon',
            field=models.FloatField(default=0),
        ),
    ]
