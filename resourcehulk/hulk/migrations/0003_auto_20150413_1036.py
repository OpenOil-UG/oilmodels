# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0002_project_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(max_length=100, choices=[('well', 'Well'), ('field', 'Field'), ('project', 'Project'), ('company-country', 'Company (all operations in one country)')]),
        ),
    ]
