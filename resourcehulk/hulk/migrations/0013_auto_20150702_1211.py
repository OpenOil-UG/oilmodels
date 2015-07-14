# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_date_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0012_auto_20150624_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='filetype',
            field=models.CharField(max_length=10, blank=True, null=True, default=None, choices=[('pdf', 'PDF'), ('html', 'HTML'), ('xls', 'Excel (xls) spreadsheet'), ('other', 'Other')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='publish_date',
            field=django_date_extensions.fields.ApproximateDateField(max_length=10, blank=True, null=True, help_text='When the document was published'),
        ),
    ]
