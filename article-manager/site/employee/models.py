# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

class Operator(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    qq = models.BigIntegerField(help_text='QQ号码', default=0, blank=True, null=True)
    memo = models.CharField(help_text='备注', max_length=300, default='', blank=True, null=True)
    created_count = models.IntegerField(help_text='创建总数', default=0)
    approved_count = models.IntegerField(help_text='审核总数', default=0)
