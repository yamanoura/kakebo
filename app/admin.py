from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Project)
admin.site.register(AccountTitle)
admin.site.register(AccountBook)
admin.site.register(AccountBookPlan)
admin.site.register(BankAccount)
admin.site.register(DepositWithdrawalMethod)
admin.site.register(GeneralParameter)
admin.site.register(BankAccountBalance)
