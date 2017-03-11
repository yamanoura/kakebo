from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Menu(models.Model):
    menu_name = models.CharField(max_length=100)
    menu_desc = models.CharField(max_length=400)
    menu_url  = models.CharField(max_length=400)

    MENU_STATUS = (
        ('0','USE'),
        ('1','DELETE'),
    )

    menu_status = models.CharField(max_length=1, choices=MENU_STATUS)

    def __str__(self):
        return self.menu_name

    def __unicode__(self):
        return u"{}".format(self.menu_name)
