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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('attempts', models.IntegerField(default=0)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('distance', models.FloatField(verbose_name='Distance between 2 cities in km')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('score', models.FloatField()),
                ('arrival_time', models.DateTimeField()),
                ('name1', models.CharField(max_length=200)),
                ('name2', models.CharField(max_length=200)),
                ('phone1', models.BigIntegerField()),
                ('phone2', models.BigIntegerField(blank=True, null=True)),
                ('email1', models.EmailField(max_length=254)),
                ('email2', models.EmailField(blank=True, max_length=254)),
                ('bitsid1', models.CharField(blank=True, max_length=16)),
                ('bitsid2', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('loc_name', models.CharField(verbose_name='Location name', max_length=64)),
                ('text', models.TextField(blank=True)),
                ('answer', models.CharField(blank=True, max_length=64)),
                ('rent', models.FloatField(default=0.0, verbose_name='Accomodation cost per second')),
                ('stipend', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='curr_loc',
            field=models.ForeignKey(to='main.Question', null=True),
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
