# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0011_auto_20150416_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='confidence',
            field=models.CharField(max_length=20),
        ),
    ]
