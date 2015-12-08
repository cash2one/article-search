# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def new_user_added(sender, **kwargs):
    user = kwargs.get('instance')
    Operator.objects.create(user=user)


class Operator(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    qq = models.BigIntegerField(help_text='QQ号码', default=0, blank=True, null=True)
    memo = models.CharField(help_text='备注', max_length=300, default='', blank=True, null=True)
    created_count = models.IntegerField(help_text='创建总数', default=0)
    approved_count = models.IntegerField(help_text='审核总数', default=0)
