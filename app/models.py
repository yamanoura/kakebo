#coding=UTF8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from kakebo import settings
from django.utils import timezone
from .constant import *

import datetime

#from .models_master import *

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

#銀行口座
class BankAccount(models.Model):
    user = models.ForeignKey(User)
    ba_name = models.CharField(u'銀行口座名',max_length=100)

    def __str__(self):
        return self.ba_name

    def __unicode__(self):
        return u"{}".format(self.ba_name)

#入出金方法
class DepositWithdrawalMethod(models.Model):
    user = models.ForeignKey(User)
    dwm_name = models.CharField(u'入出金方法名',max_length=50)
    dwm_type = models.CharField(u'入出金方法種類',
                                           max_length=1,
                                           default=0,
                                           blank=True,
                                           null=True,
                                           choices=DEPOSIT_WITHDRAWAL_METHOD_TYPE_DEFINE)

    ba =  models.ForeignKey(BankAccount,
                            models.SET_NULL,
                            blank=True,
                            null=True,
                            verbose_name=u'銀行口座名'
    )

    closing_deadline = models.IntegerField(u'締め日',
                                           blank=True,
                                           null=True,
                                           validators=[MinValueValidator(1), MaxValueValidator(31)]
    )

    pay_deadline_month = models.IntegerField(u'支払期日(締め後月数)',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(0), MaxValueValidator(12)]
    )    

    pay_deadline_day = models.IntegerField(u'支払期日(締め後日数)',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(1), MaxValueValidator(31)]
    )    

    def __str__(self):
        return self.dwm_name
    
    def __unicode__(self):
        return u"{}".format(self.dwm_name)


class BankAccountBalance(models.Model):
    user = models.ForeignKey(User)
    trade_date = models.DateField(u'取引日',
                                    blank=True,
                                    null=True,
                                    default=timezone.now())    

    dw_type = models.CharField(u'入出金種類',
                               max_length=1,
                               default=1,
                               choices=DEPOSIT_WITHDRAWAL_TYPE_DEFINE
    )

    ba =  models.ForeignKey(BankAccount,
                            verbose_name=u'銀行口座名'
    )


    desc = models.CharField(u'説明',
                            max_length=100
    )

    money = models.IntegerField(u'金額',
                                validators=[MinValueValidator(-99999999), MaxValueValidator(99999999)]
    )

    def __str__(self):
        return self.desc

    def __unicode__(self):
        return u"{}".format(self.desc)


#帳簿
class AccountBook(models.Model):
    user = models.ForeignKey(User)
    trade_date = models.DateField(u'取引日',
                                    blank=True,
                                    null=True,
                                    default=timezone.now())    

    dw_type = models.CharField(u'入出金種類',
                               max_length=1,
                               default=1,
                               choices=DEPOSIT_WITHDRAWAL_TYPE_DEFINE)

    at   = models.ForeignKey(AccountTitle,
                             verbose_name=u'勘定科目'
    )

    dwm   = models.ForeignKey(DepositWithdrawalMethod,
                            verbose_name=u'入出金方法'
    )

    project = models.ForeignKey(Project,
                            models.SET_NULL,
                            blank=True,
                            null=True,
                            verbose_name=u'Project情報'
    )

    ab_desc = models.CharField(u'帳簿摘要',
                               max_length=100
    )

    ab_money = models.IntegerField(u'帳簿金額',
                                   validators=[MinValueValidator(1), MaxValueValidator(99999999)]
    )

    bab = models.ForeignKey(BankAccountBalance,
                            models.SET_NULL,
                            blank=True,
                            null=True,
                            verbose_name=u'銀行口座残高'
    )
    
    def __str__(self):
        return self.ab_desc

    def __unicode__(self):
        return u"{}".format(self.ab_desc)
    

#予定帳簿
class AccountBookPlan(models.Model):
    user = models.ForeignKey(User)
    plan_year_month = models.CharField(u'予定年月',
                                  max_length=7,
                                  default=datetime.date.today().strftime('%Y-%m'))

    dw_type = models.CharField(u'入出金種類',
                               max_length=1,
                               default=1,
                               choices=DEPOSIT_WITHDRAWAL_TYPE_DEFINE)

    at   = models.ForeignKey(AccountTitle,
                             verbose_name=u'勘定科目'
    )

    dwm   = models.ForeignKey(DepositWithdrawalMethod,
                            verbose_name=u'入出金方法'
    )

    project = models.ForeignKey(Project,
                            models.SET_NULL,
                            blank=True,
                            null=True,
                            verbose_name=u'Project情報'
    )

    ab_desc = models.CharField(u'帳簿摘要',
                               max_length=100
    )

    ab_money = models.IntegerField(u'帳簿金額',
                                        validators=[MinValueValidator(1), MaxValueValidator(99999999)]
    )


    ab_create_flag = models.CharField(u'帳簿作成フラグ',
                                      max_length=1,
                                      default=0,
                                      choices=ACCOUNT_BOOK_CREATE_FLAG
    )
    
    def __str__(self):
        return self.ab_desc

    def __unicode__(self):
        return u"{}".format(self.ab_desc)
    


#汎用パラメータ
class GeneralParameter(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(u'汎用パラメータ名',
                            default=None,
                            max_length=20)
    desc = models.CharField(u'説明',
                            default=None,
                            max_length=100)
    sort_no = models.IntegerField(u'表示順',
                                  default=1,
                                  validators=[MinValueValidator(1), MaxValueValidator(999)])
    param1 = models.CharField(u'パラメータ1',
                              blank=True,
                              null=True,
                              max_length=10)
    param2 = models.CharField(u'パラメータ2',
                              blank=True,
                              null=True,
                              max_length=10)
    param3 = models.CharField(u'パラメータ3',
                              blank=True,
                              null=True,
                              max_length=10)

    def __str__(self):
        return self.desc

    def __unicode__(self):
        return u"{}".format(self.desc)


#データパターンマスタ
class DataPattern(models.Model):
    user = models.ForeignKey(User)
    at   = models.ForeignKey(AccountTitle,
                             verbose_name=u'勘定科目'
    )

    dp_name = models.CharField(u'データパターン名',
                               default=None,
                               max_length=100)

    sort_no = models.IntegerField(u'表示順',
                                  default=1,
                                  validators=[MinValueValidator(1), MaxValueValidator(999)])

    def __str__(self):
        return self.dp_name

    def __unicode__(self):
        return u"{}".format(self.dp_name)

#データパターン利用テーブル
class DataPatternUse(models.Model):
    user = models.ForeignKey(User)
    trade_date = models.DateField(u'取引日',
                                  default=timezone.now())    

    at   = models.ForeignKey(AccountTitle,
                             verbose_name=u'勘定科目'
    )

    dwm   = models.ForeignKey(DepositWithdrawalMethod,
                              verbose_name=u'入出金方法',
                              default=None,
                              blank=True,
                              null=True
    )

    desc = models.CharField(u'帳簿摘要',
                            max_length=100,
                            default=None
    )

    money = models.IntegerField(u'金額',
                                validators=[MinValueValidator(-99999999), MaxValueValidator(99999999)],
                                default=0
    )


    ab   = models.ForeignKey(AccountBook,
                             verbose_name=u'帳簿情報',
                             default=None,
                             blank=True,
                             null=True
    )



    def __str__(self):
        return self.desc

    def __unicode__(self):
        return u"{}".format(self.desc)

