# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0005_auto_20150409_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservelevel',
            name='level',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
