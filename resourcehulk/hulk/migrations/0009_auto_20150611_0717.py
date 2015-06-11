# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0008_document_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='metadata',
            field=django_pg.models.fields.json.JSONField(default=None, null=True, blank=True),
        ),
    ]
