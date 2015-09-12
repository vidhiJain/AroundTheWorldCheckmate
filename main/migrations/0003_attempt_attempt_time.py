# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_player_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='attempt_time',
            field=models.DateTimeField(null=True, default=None),
        ),
    ]
