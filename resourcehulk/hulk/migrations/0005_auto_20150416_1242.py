# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0004_auto_20150416_1205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Commodity',
        ),
        migrations.DeleteModel(
            name='CompanyAlias',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_url',
        ),
        migrations.RemoveField(
            model_name='company',
            name='duns_number',
        ),
        migrations.RemoveField(
            model_name='company',
            name='open_corp_id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='open_lei_id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='tax_id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ticker_symbol',
        ),
        migrations.RemoveField(
            model_name='company',
            name='vat_id',
        ),
    ]
