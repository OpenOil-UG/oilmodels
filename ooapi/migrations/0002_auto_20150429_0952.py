# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concession',
            name='retrieved_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='concession',
            name='source_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
