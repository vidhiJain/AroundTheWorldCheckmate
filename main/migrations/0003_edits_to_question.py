# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_changes_to_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='marks',
            new_name='stipend',
        ),
        migrations.RemoveField(
            model_name='question',
            name='max_attempts',
        ),
    ]
