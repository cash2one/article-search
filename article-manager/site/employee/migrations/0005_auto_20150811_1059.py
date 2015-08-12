# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20150811_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='memo',
            field=models.CharField(default=b'', max_length=300, null=True, help_text=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='qq',
            field=models.BigIntegerField(default=0, help_text=b'QQ\xe5\x8f\xb7\xe7\xa0\x81', null=True, blank=True),
        ),
    ]
