# coding: utf-8

from django.db import models

# define mofangge composition model
class Composition(models.Model):
    """
        +------------+---------------------+------+-----+---------+----------------+
        | Field      | Type                | Null | Key | Default | Extra          |
        +------------+---------------------+------+-----+---------+----------------+
        | DOCID      | bigint(20)          | NO   | PRI | NULL    | auto_increment |
        | ID         | varchar(64)         | NO   | MUL | NULL    |                |
        | OriginalID | varchar(64)         | YES  |     | NULL    |                |
        | Title      | varchar(128)        | YES  |     | NULL    |                |
        | Num        | int(11)             | YES  |     | 0       |                |
        | KeyList    | varchar(256)        | YES  |     |         |                |
        | Abstract   | longtext            | YES  |     | NULL    |                |
        | Url        | varchar(128)        | YES  | UNI | NULL    |                |
        | LabelList  | varchar(256)        | YES  |     |         |                |
        | Style      | tinyint(4)          | YES  |     | NULL    |                |
        | Grade      | tinyint(4)          | YES  |     | NULL    |                |
        | Score      | int(11)             | YES  |     | NULL    |                |
        | Subject    | int(10) unsigned    | YES  |     | NULL    |                |
        | Content    | longtext            | YES  |     | NULL    |                |
        | Site       | tinyint(3) unsigned | YES  |     | NULL    |                |
    """
    doc_id = models.AutoField(db_column='DOCID', primary_key=True)
    md5_id = models.CharField(db_column='ID', max_length=64, default=None)
    original_id = models.CharField(db_column='OriginalID', max_length=64, null=True, default=None)
    title = models.CharField(db_column='Title', max_length=128, null=True, default=None)
    number = models.IntegerField(db_column='Num', null=True, default=0)
    keywords = models.CharField(db_column='KeyList', max_length=256, null=True, blank=None)
    abstract = models.TextField(db_column='Abstract', null=True, blank=None)
    url = models.URLField(db_column='Url', max_length=128, unique=True, null=True, default=None)
    labels = models.CharField(db_column='LabelList', max_length=256, null=True, blank=None)
    style = models.SmallIntegerField(db_column='Style', null=True)
    grade = models.SmallIntegerField(db_column='Grade', null=True)
    score = models.IntegerField(db_column='Score', null=True, default=None)
    subject = models.IntegerField(db_column='Subject', null=True, default=None)
    content = models.TextField(db_column='Content', null=True, blank=None)
    source = models.SmallIntegerField(db_column='Site', null=True)

    class Meta:
        db_table = 'mofangge_composition_content'