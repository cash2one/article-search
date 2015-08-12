# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('composition', '0002_auto_20150806_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='tags',
            field=jsonfield.fields.JSONField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe7\xad\xbe', null=True, blank=True),
        ),
    ]
