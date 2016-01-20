# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0003_auto_20151205_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='korisnik',
            name='aktiviran',
        ),
    ]
