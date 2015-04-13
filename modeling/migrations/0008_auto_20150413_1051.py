# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0007_auto_20150413_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserve',
            name='company_name',
        ),
        migrations.AddField(
            model_name='reserve',
            name='commodity',
            field=models.CharField(max_length=100, choices=[('gas', 'Gas'), ('oil', 'Oil, grade unspecified'), ('oil', 'Oil, heavy'), ('oil', 'Oil, light and medium')], default='oil'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reporting_level',
            field=models.CharField(max_length=100, choices=[('well', 'Well'), ('field', 'Field'), ('project', 'Project'), ('company-country', 'Company (in one country)'), ('company', 'Company (global)'), ('country', 'Country (all companies')]),
        ),
    ]
