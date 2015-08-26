# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bitsid1',
            field=models.CharField(max_length=16, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='bitsid2',
            field=models.CharField(max_length=16, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='arrival_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='curr_loc',
            field=models.ForeignKey(to='main.Question', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone2',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
