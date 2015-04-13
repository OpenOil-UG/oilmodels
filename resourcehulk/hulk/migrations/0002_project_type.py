# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(default=1, max_length=100, choices=[('well', 'Well'), ('field', 'Field'), ('project', 'Project'), ('company-country', 'Company (in one country)'), ('company', 'Company (global)'), ('country', 'Country (all companies')]),
            preserve_default=False,
        ),
    ]
