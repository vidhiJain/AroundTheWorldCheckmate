# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_edits_to_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='rent',
            field=models.FloatField(verbose_name='Accomodation cost per second', default=0.0),
        ),
        migrations.AlterField(
            model_name='question',
            name='stipend',
            field=models.FloatField(default=0.0),
        ),
    ]
