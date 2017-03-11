#coding=UTF8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from kakebo import settings
from django.utils import timezone
from .constant import *

# Create your models here.
#Project情報
class Project(models.Model):
    user = models.ForeignKey(User)
    project_name = models.CharField(u'Project名',max_length=100)
    project_desc = models.CharField(u'Project説明',max_length=400)
    project_status = models.CharField(u'Project状態',max_length=1, choices=PROJECT_STATUS)

    def __str__(self):
        return self.project_name

    def __unicode__(self):
        return u"{}".format(self.project_name)

#勘定科目
class AccountTitle(models.Model):
    user = models.ForeignKey(User)
    at_name = models.CharField(u'勘定科目名',max_length=50)
    at_type = models.CharField(u'勘定科目種類',max_length=1, choices=ACCOUNT_TITLE_TYPE_DEFINE)
    
    def __str__(self):
        return self.at_name

    def __unicode__(self):
        return u"{}".format(self.at_name)
