# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0005_auto_20150416_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(null=True, blank=True, to='hulk.Project', related_name='subprojects'),
        ),
    ]
