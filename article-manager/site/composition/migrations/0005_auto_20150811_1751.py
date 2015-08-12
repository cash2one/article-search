# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('composition', '0004_auto_20150810_1924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='composition',
            options={'permissions': (('view_composition', 'Can view compositions'), ('changeimage_composition', 'Can change composition image'))},
        ),
    ]
