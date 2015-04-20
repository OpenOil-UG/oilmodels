# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_date_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0013_auto_20150416_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='year',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, blank=True, null=True, help_text='year statement applies to, if specified, otherwise publication year of the source document'),
        ),
    ]
