# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0006_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
