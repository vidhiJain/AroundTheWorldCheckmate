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
            name='ip_address',
            field=models.GenericIPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
    ]
