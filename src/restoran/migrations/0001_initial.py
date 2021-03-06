# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-03 17:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=20)),
                ('opis', models.CharField(max_length=200)),
                ('cena', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Korisnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aktiviran', models.BooleanField(default=False)),
                ('prijatelji', models.ManyToManyField(blank=True, related_name='_korisnik_prijatelji_+', to='restoran.Korisnik')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_auth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poseta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocena', models.IntegerField()),
                ('prosecna_ocena', models.FloatField()),
                ('prosecna_ocena_korisnika', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Pozivnica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stanje', models.CharField(choices=[(b'A', b'Accept'), (b'D', b'Decline'), (b'P', b'Pending')], default=b'P', max_length=1)),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pozvani', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Restoran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=20)),
                ('jelovnik', models.ManyToManyField(to='restoran.Jelo')),
            ],
        ),
        migrations.CreateModel(
            name='Rezervacija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField(verbose_name=b'date published')),
                ('zauzece', models.IntegerField()),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='korisnik', to=settings.AUTH_USER_MODEL)),
                ('restoran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restoran.Restoran')),
                ('zvanice', models.ManyToManyField(related_name='zvanice', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VrstaRestorana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=20)),
                ('opis', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='restoran',
            name='tip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restoran.VrstaRestorana'),
        ),
        migrations.AddField(
            model_name='poseta',
            name='rezervacija',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restoran.Rezervacija'),
        ),
        migrations.AddField(
            model_name='poseta',
            name='zvanice',
            field=models.ManyToManyField(related_name='zvanice', to='restoran.Pozivnica'),
        ),
    ]
