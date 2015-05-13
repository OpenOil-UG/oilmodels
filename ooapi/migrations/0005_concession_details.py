# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0004_concessionsearchresult_date_original'),
    ]

    operations = [
        migrations.AddField(
            model_name='concession',
            name='details',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True),
        ),
    ]
