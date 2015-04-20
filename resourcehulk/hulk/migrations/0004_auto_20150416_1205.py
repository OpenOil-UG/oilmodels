# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0003_auto_20150413_1036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['company_name']},
        ),
    ]
