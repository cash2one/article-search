# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qq', models.CharField(help_text=b'QQ\xe5\x8f\xb7\xe7\xa0\x81', max_length=50)),
                ('created_count', models.IntegerField(default=0, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x80\xbb\xe6\x95\xb0')),
                ('approved_count', models.IntegerField(default=0, help_text=b'\xe5\xae\xa1\xe6\xa0\xb8\xe6\x80\xbb\xe6\x95\xb0')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
