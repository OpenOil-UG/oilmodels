# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0007_document_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='metadata',
            field=django_pg.models.fields.json.JSONField(default=b'{}', null=True, blank=True),
        ),
    ]
