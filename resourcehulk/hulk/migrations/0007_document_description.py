# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0006_project_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
