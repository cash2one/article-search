# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import composition.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe9\xa2\x98', max_length=300)),
                ('abstract', models.CharField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\x91\x98\xe8\xa6\x81', max_length=500)),
                ('tags', models.CharField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe7\xad\xbe', max_length=500, blank=True)),
                ('atype', models.IntegerField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe4\xbd\x93\xe8\xa3\x81', blank=True, choices=[(1, b'\xe8\xae\xb0\xe5\x8f\x99\xe6\x96\x87'), (2, b'\xe8\xae\xae\xe8\xae\xba\xe6\x96\x87'), (3, b'\xe8\xaf\xb4\xe6\x98\x8e\xe6\x96\x87'), (4, b'\xe6\x95\xa3\xe6\x96\x87'), (5, b'\xe8\xaf\x97\xe6\xad\x8c'), (6, b'\xe6\x9d\x82\xe6\x96\x87')])),
                ('grade', models.IntegerField(help_text=b'\xe5\xb9\xb4\xe7\xba\xa7', blank=True, choices=[(1, b'\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (2, b'\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'), (3, b'\xe4\xb8\x89\xe5\xb9\xb4\xe7\xba\xa7'), (4, b'\xe5\x9b\x9b\xe5\xb9\xb4\xe7\xba\xa7'), (5, b'\xe4\xba\x94\xe5\xb9\xb4\xe7\xba\xa7'), (6, b'\xe5\x85\xad\xe5\xb9\xb4\xe7\xba\xa7'), (7, b'\xe4\xb8\x83\xe5\xb9\xb4\xe7\xba\xa7'), (8, b'\xe5\x85\xab\xe5\xb9\xb4\xe7\xba\xa7'), (9, b'\xe4\xb9\x9d\xe5\xb9\xb4\xe7\xba\xa7'), (10, b'\xe9\xab\x98\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (11, b'\xe9\xab\x98\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'), (12, b'\xe9\xab\x98\xe4\xb8\x89\xe5\xb9\xb4\xe7\xba\xa7')])),
                ('number', models.IntegerField(help_text=b'\xe5\xad\x97\xe6\x95\xb0')),
                ('created', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xa5\xe6\x9c\x9f', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xa5\xe6\x9c\x9f', auto_now=True)),
                ('content', models.TextField(help_text=b'\xe6\xad\xa3\xe6\x96\x87')),
                ('source', models.CharField(help_text=b'\xe6\x9d\xa5\xe6\xba\x90', max_length=200, blank=True)),
                ('status', models.IntegerField(default=0, help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xbe\x85\xe5\xae\xa1\xe6\xa0\xb8'), (1, b'\xe5\xae\xa1\xe6\xa0\xb8\xe4\xb8\xad'), (2, b'\xe5\xae\xa1\xe6\xa0\xb8\xe5\xae\x8c\xe6\xaf\x95')])),
                ('image', models.ImageField(max_length=300, null=True, upload_to=composition.models.get_image_filepath)),
                ('beginning', models.TextField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe5\xbc\x80\xe5\xa4\xb4', max_length=600, null=True)),
                ('ending', models.TextField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\xbb\x93\xe5\xb0\xbe', max_length=600, null=True)),
                ('approver', models.ForeignKey(related_name='compositions', to=settings.AUTH_USER_MODEL, null=True)),
                ('creator', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_composition', 'Can view compositions'),),
            },
        ),
    ]
