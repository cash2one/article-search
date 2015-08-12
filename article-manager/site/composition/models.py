# coding: utf-8
import hashlib
from datetime import datetime
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


def get_image_filepath(instance, filename):
    md5str = hashlib.md5(filename+str(datetime.now())).hexdigest()
    return '{subdir}/{filename}.jpg'.format(subdir=md5str[:3], filename=md5str[3:])

# Composition Model
class Composition(models.Model):
    ATYPE_CHOICES = [
        (1,'记叙文'),
        (2,'议论文'),
        (3,'说明文'),
        (4,'散文'),
        (5,'诗歌'),
        (6,'杂文')
    ]

    GRADE_CHOICES = [
        (1,'一年级'),
        (2,'二年级'),
        (3,'三年级'),
        (4,'四年级'),
        (5,'五年级'),
        (6,'六年级'),
        (7,'七年级'),
        (8,'八年级'),
        (9,'九年级'),
        (10,'高一年级'),
        (11,'高二年级'),
        (12,'高三年级'),
    ]

    WAIT_APPROVAL = 0
    APPROVING = 1
    FINISH_APPROVAL = 2
    STATUS_CHOICES = [
        (WAIT_APPROVAL,'待审核'),
        (APPROVING,'审核中'),
        (FINISH_APPROVAL,'审核完毕'),
    ]

    title = models.CharField(verbose_name='作文标题', help_text='作文标题', max_length=300)
    abstract = models.CharField(verbose_name='作文摘要', help_text='作文摘要', max_length=500)
    tags = JSONField(verbose_name='作文标签', help_text='作文标签', null=True, blank=True)
    atype = models.IntegerField(verbose_name='作文体裁', help_text='作文体裁', 
        choices=ATYPE_CHOICES, null=True, blank=True)
    grade = models.IntegerField(verbose_name='年级', help_text='年级', 
        choices=GRADE_CHOICES, null=True, blank=True)
    number = models.IntegerField(verbose_name='字数', help_text='字数')
    created = models.DateTimeField(verbose_name='创建日期', auto_now_add=True, help_text='创建日期')
    modified = models.DateTimeField(verbose_name='修改日期', auto_now=True, help_text='修改日期')
    content = models.TextField(verbose_name='正文', help_text='正文')
    source = models.CharField(verbose_name='来源', help_text='来源', max_length=200, null=True, blank=True)
    creator = models.ForeignKey(User, related_name='+', verbose_name='创建者')
    approver = models.ForeignKey(User, related_name='compositions', verbose_name='审核者', null=True)
    status = models.IntegerField(verbose_name='作文状态', help_text='作文状态', 
        choices=STATUS_CHOICES, default=WAIT_APPROVAL)
    image = models.ImageField(verbose_name='图片', upload_to=get_image_filepath, max_length=300, null=True, blank=True)
    beginning = models.TextField(verbose_name='作文开头', help_text='作文开头', max_length=600, null=True, blank=True)
    ending = models.TextField(verbose_name='作文结尾', help_text='作文结尾', max_length=600, null=True, blank=True)

    class Meta:
        permissions = (
            ('view_composition', 'Can view compositions'),
            ('changeimage_composition', 'Can change composition image'),
        )

    def __unicode__(self):
        return "id:{id},t:{title},s:{status}".format(id=self.id, title=self.title, status=self.status)

    

