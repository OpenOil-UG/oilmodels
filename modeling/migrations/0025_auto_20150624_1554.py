# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modeling', '0024_extrainformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='extracted_data',
            field=models.ForeignKey(blank=True, to='modeling.ExtractedData', null=True),
        ),
        migrations.AddField(
            model_name='cost',
            name='moderated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='extrainformation',
            name='extracted_data',
            field=models.ForeignKey(blank=True, to='modeling.ExtractedData', null=True),
        ),
        migrations.AddField(
            model_name='extrainformation',
            name='moderated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='production',
            name='extracted_data',
            field=models.ForeignKey(blank=True, to='modeling.ExtractedData', null=True),
        ),
        migrations.AddField(
            model_name='production',
            name='moderated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reserve',
            name='extracted_data',
            field=models.ForeignKey(blank=True, to='modeling.ExtractedData', null=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='moderated',
            field=models.BooleanField(default=False),
        ),
    ]
