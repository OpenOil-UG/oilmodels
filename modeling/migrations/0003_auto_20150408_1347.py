# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0002_country_reserve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
