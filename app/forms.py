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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)

class AccountTitleForm(ModelForm):
    class Meta:
        model = AccountTitle
        fields = ("at_name",
                  "at_type",
                  )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountTitleForm, self).__init__(*args, **kwargs)

class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ("ba_name",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BankAccountForm, self).__init__(*args, **kwargs)

class DepositWithdrawalMethodForm(ModelForm):
    class Meta:
        model = DepositWithdrawalMethod
        fields = ("dwm_name",
                  "dwm_type",
                  "ba",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DepositWithdrawalMethodForm, self).__init__(*args, **kwargs)
        self.fields["ba"].queryset = BankAccount.objects.filter(user=self.user)

#入金用
class AccountBookDepositForm(ModelForm):
    user = None
    class Meta:
        model = AccountBook
        fields = (
            "trade_date",
            "dw_type",
            "at",
            "dwm",
            "project",
            "ab_desc",
            "ab_money",
        )

        widgets = {
            'trade_date': DateInput(attrs={"type":"date"}),
            'ab_money': DateInput(attrs={"style":"text-align:right","type":"number"}),
            
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountBookDepositForm, self).__init__(*args, **kwargs)
        self.fields["dw_type"].initial = '0'
        self.fields["dw_type"].widget = forms.HiddenInput()
        self.fields["at"].queryset = AccountTitle.objects.filter(user=self.user,at_type=0)
        self.fields["dwm"].queryset = DepositWithdrawalMethod.objects.filter(user=self.user)
        self.fields["project"].queryset = Project.objects.filter(user=self.user,project_status='0')


#出金用
class AccountBookWithdrawalForm(ModelForm):
    user = None
    class Meta:
        model = AccountBook
        fields = ("trade_date",
                  "dw_type",
                  "at",
                  "dwm",
                  "project",
                  "ab_desc",
                  "ab_money",
        )

        widgets = {
            'trade_date': DateInput(attrs={"type":"date"}),
            'ab_money': DateInput(attrs={"style":"text-align:right","type":"number"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountBookWithdrawalForm, self).__init__(*args, **kwargs)
        self.fields["dw_type"].initial = '1'
        self.fields["dw_type"].widget = forms.HiddenInput()
        self.fields["at"].queryset = AccountTitle.objects.filter(user=self.user,at_type='1')
        self.fields["dwm"].queryset = DepositWithdrawalMethod.objects.filter(user=self.user)
        self.fields["project"].queryset = Project.objects.filter(user=self.user,project_status='0')

#入金用
class AccountBookPlanDepositForm(ModelForm):
    user = None
    class Meta:
        model = AccountBookPlan
        fields = (
            "plan_year_month",
            "dw_type",
            "at",
            "dwm",
            "project",
            "ab_desc",
            "ab_money",
            "ab_create_flag",
        )

        widgets = {
            'plan_year_month': DateInput(attrs={"type":"month"}),
            'ab_money': DateInput(attrs={"style":"text-align:right","type":"number"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountBookPlanDepositForm, self).__init__(*args, **kwargs)
        self.fields["dw_type"].initial = '0'
        self.fields["dw_type"].widget = forms.HiddenInput()
        self.fields["at"].queryset = AccountTitle.objects.filter(user=self.user,at_type=0)
        self.fields["dwm"].queryset = DepositWithdrawalMethod.objects.filter(user=self.user)
        self.fields["project"].queryset = Project.objects.filter(user=self.user,project_status='0')
        self.fields["ab_create_flag"].widget = forms.HiddenInput()


#出金用
class AccountBookPlanWithdrawalForm(ModelForm):
    user = None
    class Meta:
        model = AccountBookPlan
        fields = ("plan_year_month",
                  "dw_type",
                  "at",
                  "dwm",
                  "project",
                  "ab_desc",
                  "ab_money",
                  "ab_create_flag",
        )

        widgets = {
            'plan_year_month': DateInput(attrs={"type":"month"}),
            'ab_money': DateInput(attrs={"style":"text-align:right","type":"number"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountBookPlanWithdrawalForm, self).__init__(*args, **kwargs)
        self.fields["dw_type"].initial = '1'
        self.fields["dw_type"].widget = forms.HiddenInput()
        self.fields["at"].queryset = AccountTitle.objects.filter(user=self.user,at_type='1')
        self.fields["dwm"].queryset = DepositWithdrawalMethod.objects.filter(user=self.user)
        self.fields["project"].queryset = Project.objects.filter(user=self.user,project_status='0')
        self.fields["ab_create_flag"].widget = forms.HiddenInput()


