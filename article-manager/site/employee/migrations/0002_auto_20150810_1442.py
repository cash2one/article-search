# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='qq',
            field=models.CharField(help_text=b'QQ\xe5\x8f\xb7\xe7\xa0\x81', max_length=50, null=True),
        ),
    ]
