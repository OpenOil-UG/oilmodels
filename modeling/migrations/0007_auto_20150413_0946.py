# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0001_initial'),
        ('modeling', '0006_reservelevel_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserve',
            name='field_name',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='project_name',
        ),
        migrations.AddField(
            model_name='reserve',
            name='company',
            field=models.ForeignKey(to='hulk.Company', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='project',
            field=models.ForeignKey(to='hulk.Project', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='source_document',
            field=models.ForeignKey(to='hulk.Document', blank=True, null=True),
        ),
    ]
