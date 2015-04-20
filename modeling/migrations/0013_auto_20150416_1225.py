# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_date_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0012_auto_20150416_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='confidence',
            field=models.CharField(max_length=20, null=True, blank=True, choices=[('Unknown', 'Unknown'), ('1P', '1P'), ('2P', '2P'), ('3P', '3P'), ('1C', '1C'), ('2C', '2C'), ('3C', '3C')]),
        ),
        migrations.AlterField(
            model_name='production',
            name='date',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, null=True, blank=True),
        ),
    ]
