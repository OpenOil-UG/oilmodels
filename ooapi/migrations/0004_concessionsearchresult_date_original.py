# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ooapi', '0003_concessionsearchresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='concessionsearchresult',
            name='date_original',
            field=models.DateField(null=True, blank=True),
        ),
    ]
