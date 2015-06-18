# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0022_extracteddata_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='production',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='cost',
            name='extra_data',
            field=django_pg.models.fields.json.JSONField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='production',
            name='extra_data',
            field=django_pg.models.fields.json.JSONField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='extra_data',
            field=django_pg.models.fields.json.JSONField(default=None, null=True, blank=True),
        ),
    ]
