# coding: utf-8

from django.db import models

# define mofangge composition model
class MofanggeComposition(models.Model):
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
        +------------+---------------------+------+-----+---------+----------------+
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
        managed = False
        db_table = 'mofangge_composition_content'

# define backend db compostion model
class BackendComposition(models.Model):
    """
        +-------------+--------------+------+-----+---------+----------------+
        | Field       | Type         | Null | Key | Default | Extra          |
        +-------------+--------------+------+-----+---------+----------------+
        | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
        | title       | varchar(300) | NO   |     | NULL    |                |
        | abstract    | varchar(500) | NO   |     | NULL    |                |
        | tags        | longtext     | YES  |     | NULL    |                |
        | atype       | int(11)      | YES  |     | NULL    |                |
        | grade       | int(11)      | YES  |     | NULL    |                |
        | number      | int(11)      | NO   |     | NULL    |                |
        | created     | datetime(6)  | NO   |     | NULL    |                |
        | modified    | datetime(6)  | NO   |     | NULL    |                |
        | content     | longtext     | NO   |     | NULL    |                |
        | source      | varchar(200) | YES  |     | NULL    |                |
        | status      | int(11)      | NO   |     | NULL    |                |
        | image       | varchar(300) | YES  |     | NULL    |                |
        | beginning   | longtext     | YES  |     | NULL    |                |
        | ending      | longtext     | YES  |     | NULL    |                |
        | approver_id | int(11)      | YES  | MUL | NULL    |                |
        | creator_id  | int(11)      | NO   | MUL | NULL    |                |
        +-------------+--------------+------+-----+---------+----------------+
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    abstract = models.CharField(max_length=500)
    tags = models.TextField(blank=True, null=True)
    atype = models.IntegerField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    number = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()
    image = models.CharField(max_length=300, blank=True, null=True)
    beginning = models.TextField(blank=True, null=True)
    ending = models.TextField(blank=True, null=True)
    approver = models.IntegerField(blank=True, null=True)
    creator = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'composition_composition'
