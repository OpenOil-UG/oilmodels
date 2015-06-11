# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0009_auto_20150611_0717'),
        ('modeling', '0021_auto_20150611_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='extracteddata',
            name='document',
            field=models.ForeignKey(blank=True, to='hulk.Document', null=True),
        ),
    ]
