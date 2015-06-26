# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_date_extensions.fields
import django_pg.models.fields.datetime_
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hulk', '0009_auto_20150611_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='host_url',
            new_name='mirror_url',
        ),
        migrations.AddField(
            model_name='document',
            name='import_date',
            field=django_pg.models.fields.datetime_.DateTimeField(default=datetime.datetime(2015, 6, 24, 12, 44, 39, 826676, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='publish_date',
            field=django_date_extensions.fields.ApproximateDateField(help_text=b'When the document was published', max_length=10, null=True, blank=True),
        ),
    ]
