# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0004_remove_korisnik_aktiviran'),
    ]

    operations = [
        migrations.AddField(
            model_name='restoran',
            name='menadzer',
            field=models.ManyToManyField(to='restoran.Korisnik'),
        ),
    ]
