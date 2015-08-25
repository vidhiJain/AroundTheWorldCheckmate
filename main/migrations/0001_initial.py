# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('attempts', models.IntegerField(default=0)),
                ('correct', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('distance', models.FloatField(verbose_name='Distance between 2 cities in km')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('score', models.FloatField()),
                ('arrival_time', models.DateTimeField(null=True)),
                ('name1', models.CharField(max_length=200)),
                ('name2', models.CharField(max_length=200)),
                ('phone1', models.BigIntegerField()),
                ('phone2', models.BigIntegerField(null=True)),
                ('email1', models.EmailField(max_length=254)),
                ('email2', models.EmailField(max_length=254, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.TextField()),
                ('loc_name', models.CharField(max_length=64, verbose_name='Location name')),
                ('rent', models.FloatField(verbose_name='Accomodation cost per second')),
                ('answer', models.CharField(max_length=64)),
                ('max_attempts', models.IntegerField(default=0)),
                ('marks', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='curr_loc',
            field=models.ForeignKey(to='main.Question'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distance',
            name='dest',
            field=models.ForeignKey(to='main.Question', related_name='dests'),
        ),
        migrations.AddField(
            model_name='distance',
            name='source',
            field=models.ForeignKey(to='main.Question', related_name='sources'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='question',
            field=models.ForeignKey(to='main.Question'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
