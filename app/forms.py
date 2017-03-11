#coding=UTF8
from django import forms
from django.forms import ModelForm,DateInput
from app.models import *

from .constant import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("project_name",
                  "project_desc",
                  "project_status")

class AccountTitleForm(ModelForm):
    class Meta:
        model = AccountTitle
        fields = ("at_name",
                  "at_type",
                  )

