# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import composition.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('composition', '0003_auto_20150810_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='abstract',
            field=models.CharField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\x91\x98\xe8\xa6\x81', max_length=500, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\x91\x98\xe8\xa6\x81'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='approver',
            field=models.ForeignKey(related_name='compositions', verbose_name=b'\xe5\xae\xa1\xe6\xa0\xb8\xe8\x80\x85', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='atype',
            field=models.IntegerField(blank=True, help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe4\xbd\x93\xe8\xa3\x81', null=True, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe4\xbd\x93\xe8\xa3\x81', choices=[(1, b'\xe8\xae\xb0\xe5\x8f\x99\xe6\x96\x87'), (2, b'\xe8\xae\xae\xe8\xae\xba\xe6\x96\x87'), (3, b'\xe8\xaf\xb4\xe6\x98\x8e\xe6\x96\x87'), (4, b'\xe6\x95\xa3\xe6\x96\x87'), (5, b'\xe8\xaf\x97\xe6\xad\x8c'), (6, b'\xe6\x9d\x82\xe6\x96\x87')]),
        ),
        migrations.AlterField(
            model_name='composition',
            name='beginning',
            field=models.TextField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe5\xbc\x80\xe5\xa4\xb4', max_length=600, null=True, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe5\xbc\x80\xe5\xa4\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='content',
            field=models.TextField(help_text=b'\xe6\xad\xa3\xe6\x96\x87', verbose_name=b'\xe6\xad\xa3\xe6\x96\x87'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='created',
            field=models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xa5\xe6\x9c\x9f', verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xa5\xe6\x9c\x9f', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='creator',
            field=models.ForeignKey(related_name='+', verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe8\x80\x85', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='composition',
            name='ending',
            field=models.TextField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\xbb\x93\xe5\xb0\xbe', max_length=600, null=True, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\xbb\x93\xe5\xb0\xbe', blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='grade',
            field=models.IntegerField(blank=True, help_text=b'\xe5\xb9\xb4\xe7\xba\xa7', null=True, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7', choices=[(1, b'\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (2, b'\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'), (3, b'\xe4\xb8\x89\xe5\xb9\xb4\xe7\xba\xa7'), (4, b'\xe5\x9b\x9b\xe5\xb9\xb4\xe7\xba\xa7'), (5, b'\xe4\xba\x94\xe5\xb9\xb4\xe7\xba\xa7'), (6, b'\xe5\x85\xad\xe5\xb9\xb4\xe7\xba\xa7'), (7, b'\xe4\xb8\x83\xe5\xb9\xb4\xe7\xba\xa7'), (8, b'\xe5\x85\xab\xe5\xb9\xb4\xe7\xba\xa7'), (9, b'\xe4\xb9\x9d\xe5\xb9\xb4\xe7\xba\xa7'), (10, b'\xe9\xab\x98\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (11, b'\xe9\xab\x98\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'), (12, b'\xe9\xab\x98\xe4\xb8\x89\xe5\xb9\xb4\xe7\xba\xa7')]),
        ),
        migrations.AlterField(
            model_name='composition',
            name='image',
            field=models.ImageField(max_length=300, upload_to=composition.models.get_image_filepath, null=True, verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87', blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='modified',
            field=models.DateTimeField(help_text=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xa5\xe6\x9c\x9f', verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xa5\xe6\x9c\x9f', auto_now=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='number',
            field=models.IntegerField(help_text=b'\xe5\xad\x97\xe6\x95\xb0', verbose_name=b'\xe5\xad\x97\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='source',
            field=models.CharField(help_text=b'\xe6\x9d\xa5\xe6\xba\x90', max_length=200, null=True, verbose_name=b'\xe6\x9d\xa5\xe6\xba\x90', blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='status',
            field=models.IntegerField(default=0, help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\x8a\xb6\xe6\x80\x81', verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xbe\x85\xe5\xae\xa1\xe6\xa0\xb8'), (1, b'\xe5\xae\xa1\xe6\xa0\xb8\xe4\xb8\xad'), (2, b'\xe5\xae\xa1\xe6\xa0\xb8\xe5\xae\x8c\xe6\xaf\x95')]),
        ),
        migrations.AlterField(
            model_name='composition',
            name='tags',
            field=jsonfield.fields.JSONField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe7\xad\xbe', null=True, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe7\xad\xbe', blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='title',
            field=models.CharField(help_text=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe9\xa2\x98', max_length=300, verbose_name=b'\xe4\xbd\x9c\xe6\x96\x87\xe6\xa0\x87\xe9\xa2\x98'),
        ),
    ]
