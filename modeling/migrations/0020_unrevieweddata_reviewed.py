# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0019_auto_20150608_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='unrevieweddata',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
