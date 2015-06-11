# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0020_unrevieweddata_reviewed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UnreviewedData',
            new_name='ExtractedData',
        ),
    ]
