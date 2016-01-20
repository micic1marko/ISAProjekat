# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoran', '0010_pozivnica_ocena'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stanje', models.CharField(choices=[(b'R', b'Reserved'), (b'F', b'Free')], default=b'F', max_length=1)),
                ('broj_stolica', models.IntegerField(default=0)),
                ('red', models.IntegerField(default=0)),
                ('kolona', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='restoran',
            name='stolovi',
            field=models.ManyToManyField(blank=True, to='restoran.Sto'),
        ),
    ]