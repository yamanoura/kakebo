#coding=UTF8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import *
from django.views.generic.edit import *

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
import sys
from .constant import *
from common.menulist import *

# util
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import logging
from django.db.models import Sum
from django.db.models import Max
from django.db.models import Count
from django.db.models import Case,When,Value
import re

APP_NAME     = 'app'
PACKAGE_NAME = 'app.views'
SUCCESS_URL  = '/common/mypage'
AUTH_FAILURE = '/common/login/?next=%s'

class BaseView():
    def get_object(self):
        class_name = self.__class__.__name__
        __import__(PACKAGE_NAME, globals(), locals(), [], -1)
        class_object = getattr(sys.modules[PACKAGE_NAME],class_name)

        return class_object

class BaseCreateView(BaseView,CreateView):
    success_url= SUCCESS_URL

    def dispatch(self,request, *args, **kwargs):
        info('dispatch')

        class_object = self.get_object()

        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(class_object, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(BaseCreateView,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        ctx['is_logined'] = True
        ctx['is_addmode'] = True
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST
        return ctx

    def get_form_kwargs(self):
        class_object = self.get_object()
        kwargs = super(BaseCreateView, self).get_form_kwargs()

        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        class_object = self.get_object()
        form.instance.user = self.request.user

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        template_name = re.sub(r'.html$','',template_file_name)

        if template_name=='ab_d_form':
            form_trade_date = form.instance.trade_date
            form_dwm_id = form.instance.dwm_id
            form_dw_type = form.instance.dw_type
            form_ab_desc = form.instance.ab_desc
            form_ab_money = form.instance.ab_money

            form_ba_list = DepositWithdrawalMethod.objects.filter(user=self.request.user,
                                                             id=form_dwm_id).values('ba')
            form_ba = None
            form_ba_id = 0

            for item in form_ba_list:
                form_ba_id = item['ba']

            if form_ba_id is not None:
                form_ba = BankAccount.objects.filter(user=self.request.user,
                                                     id=form_ba_id)
                bab = BankAccountBalance(user=self.request.user,
                                         trade_date=form_trade_date,
                                         ba_id=form_ba_id,
                                         dw_type=form_dw_type,
                                         desc=form_ab_desc,
                                         money=form_ab_money
                )

                bab.save()

                form.instance.bab = bab

        return super(class_object, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')


class BaseListCreateView(BaseView,ListView):
    success_url= SUCCESS_URL

    def dispatch(self,request, *args, **kwargs):
        class_object = self.get_object()

        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(class_object, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(BaseListCreateView,self).get_context_data(**kwargs)
        self.set_eachdefault_ctx(ctx)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)

        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name
        ctx['is_logined'] = True
        ctx['is_addmode'] = True

        is_submit_flag = self.get_param('is_submit_flag')

        if is_submit_flag == "":
            ctx['is_detailmode'] = False
        else:
            ctx['is_detailmode'] = True

        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        search_trade_date = self.get_param('search_trade_date')
        search_dw_type_select = self.get_param('search_dw_type_select')
        search_at_select = self.get_param('search_at_select')

        if is_submit_flag=="2":
            modellist =self.get_modeldata()

            for item in modellist:
                item.money = self.get_param(str(item.id) + '_money')
                
                dwm_select = self.get_param(str(item.id) + '_dwm')
                dwm_object = DepositWithdrawalMethod.objects.get(user=self.request.user,
                                                                 id=dwm_select)
                item.dwm = dwm_object

                
                if item.ab==None:
                    if int(item.money) != 0:
                        ab = AccountBook(user=self.request.user,
                                         trade_date=item.trade_date,
                                         dw_type=item.at.at_type,
                                         at=item.at,
                                         dwm=item.dwm,
                                         project=None,
                                         ab_desc='DPU ' + item.desc,
                                         ab_money=item.money)

                        ab.save()
                        item.ab = ab
                else:
                    item_ab = item.ab
                    if int(item.money) == 0:
                        item.ab = None
                        info(item_ab)
                        item_ab.delete()

                    else:
                        info(item_ab.ab_money)
                        item_ab.ab_money = item.money
                        info(item_ab.ab_money)
                        
                        item_ab.save()
                        
                item.save()

        return ctx

    def set_eachdefault_ctx(self,ctx):
        #画面項目セット
        search_trade_date = self.get_param('search_trade_date')
        search_trade_date = get_defaultdate(search_trade_date)
        ctx['search_trade_date'] = search_trade_date

        ctx['search_dw_type_select'] = self.get_param('search_dw_type_select')
        search_at_select = self.request.GET.get('search_at_select','')

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)
        ctx['search_at_select'] = search_at_select

        search_at = DataPattern.objects.filter(user=self.request.user,
                                               at__at_type=ctx['search_dw_type_select'])

        search_at = search_at.values('at__id').annotate(id=Max('at__id'),at_name=Max('at__at_name'))

        ctx['search_at'] = search_at

        search_dwm = DepositWithdrawalMethod.objects.filter(user=self.request.user)

        ctx['search_dwm'] = search_dwm

    def get_queryset(self):
        return self.get_modeldata()

    def get_modeldata(self):
        search_trade_date = self.get_param('search_trade_date')
        search_dw_type_select = self.get_param('search_dw_type_select')
        search_at_select = self.request.GET.get('search_at_select','')

        if search_trade_date == "" or search_dw_type_select == "" or search_at_select == "":
            return None

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)

        dpu =  DataPatternUse.objects.filter(user=self.request.user,
                                             trade_date=search_trade_date,
                                             at=search_at_select
        )

        dp =  DataPattern.objects.filter(user=self.request.user,
                                         at=search_at_select
        )

        dwm_default = DepositWithdrawalMethod.objects.get(user=self.request.user,
                                                          dwm_type="0")

        for dp_item in dp:
            dpu_item_exist_flag = 0
            for dpu_item in dpu:
                if dp_item.dp_name == dpu_item.desc:
                    dpu_item_exist_flag = 1

            if dpu_item_exist_flag == 0:
                dp_new = DataPatternUse(user=self.request.user,
                                        trade_date=search_trade_date,
                                        at=dp_item.at,
                                        dwm=dwm_default,
                                        desc=dp_item.dp_name,
                                        money=0,
                                        ab=None)

                dp_new.save()

        dpu =  DataPatternUse.objects.filter(user=self.request.user,
                                             trade_date=search_trade_date,
                                             at=search_at_select
        )

        

        return dpu

    def get_dp_at(self):
        return None

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')

        
class BaseUpdateView(UpdateView):
    success_url = SUCCESS_URL

    def get_object(self, **kwargs):
        if not hasattr(self, '_object'):
            self._object = super(BaseUpdateView, self).get_object(**kwargs)

        return self._object

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            buv = self.get_object()
            if buv.user.id != request.user.id:
                return HttpResponseRedirect(SUCCESS_URL)

            return super(BaseUpdateView, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user

        class_object = self.get_object()
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        template_name = re.sub(r'.html$','',template_file_name)


        if (template_name == 'ab_plan_w_form' or template_name == 'ab_plan_d_form') and class_object.ab_create_flag=='1':
            set_at = AccountTitle(user=self.request.user,
                              id=class_object.at.id
            )

            set_dwm = DepositWithdrawalMethod(user=self.request.user,
                                              id=class_object.dwm.id
            )

            set_project=None
            if class_object.project==None:
                set_project = None
            else:
                set_project = Project(user=self.request.user,
                                  id=class_object.project.id
                )

            set_bab = None
            if template_name == 'ab_plan_d_form':
                form_ba_list = DepositWithdrawalMethod.objects.filter(user=self.request.user,
                                                                      id=class_object.dwm.id).values('ba')

                form_ba = None
                form_ba_id = None
                for item in form_ba_list:
                    form_ba_id = item['ba']
                    
                if form_ba_id is not None:
                    form_ba = BankAccount.objects.filter(user=self.request.user,
                                                         id=form_ba_id)

                    set_bab = BankAccountBalance(user=self.request.user,
                                                 trade_date=get_defaultdate(None),
                                                 dw_type=class_object.dw_type,
                                                 ba_id=form_ba_id,
                                                 desc=class_object.ab_desc,
                                                 money=class_object.ab_money
                    )
                    set_bab.save()


            ab = AccountBook(user=self.request.user,
                        trade_date=get_defaultdate(None),
                        dw_type=class_object.dw_type,
                        at=set_at,
                        dwm=set_dwm,
                        project=set_project,
                        ab_desc=class_object.ab_desc,
                        ab_money=class_object.ab_money,
                        bab=set_bab
            )

            ab.save()


        if template_name=='ab_d_form':
            form_trade_date = form.instance.trade_date
            form_dwm_id = form.instance.dwm_id
            form_dw_type = form.instance.dw_type
            form_ab_desc = form.instance.ab_desc
            form_ab_money = form.instance.ab_money
            form_bab_id = form.instance.bab_id

            form_ba_list = DepositWithdrawalMethod.objects.filter(user=self.request.user,
                                                                  id=form_dwm_id).values('ba')
            form_ba = None
            for item in form_ba_list:
                form_ba_id = item['ba']

            if form_ba_id is not None:
                form_ba = BankAccount.objects.filter(user=self.request.user,
                                                     id=form_ba_id)

                if form_bab_id is not None:
                    form_bab = BankAccountBalance.objects.get(pk=form_bab_id)
                    form_bab.trade_date = form_trade_date
                    form_bab.dw_type = form_dw_type
                    form_bab.ba_id = form_ba_id
                    form_bab.desc = form_ab_desc
                    form_bab.money = form_ab_money
                    form_bab.save()
                else:
                    bab = BankAccountBalance(user=self.request.user,
                                             trade_date=form_trade_date,
                                             ba_id=form_ba_id,
                                             dw_type=form_dw_type,
                                             desc=form_ab_desc,
                                             money=form_ab_money
                    )

                    bab.save()
                    form.instance.bab = bab
            else:
                form.instance.bab = None

                if form_bab_id is not None:
                    form_bab = BankAccountBalance.objects.get(pk=form_bab_id)
                    form_bab.delete()

        return super(BaseUpdateView, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(BaseUpdateView,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        ctx['is_logined'] = True
        ctx['is_addmode'] = False
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST
        return ctx



    def get_form_kwargs(self):
        class_object = self.get_object()
        kwargs = super(BaseUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class BaseDeleteView(DeleteView):
    success_url = SUCCESS_URL

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(BaseDeleteView, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BaseDeleteView, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(BaseDeleteView,self).get_context_data(**kwargs)
        ctx['is_logined'] = True
        ctx['is_addmode'] = False
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST
        return ctx

class ProjectSearch(ListView):
    model = Project
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(ProjectSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ProjectSearch,self).get_context_data(**kwargs)

        ctx['search_project_name'] = self.request.GET.get('search_project_name','')
        ctx['search_project_desc'] = self.request.GET.get('search_project_desc','')
        ctx['search_project_status'] = self.request.GET.get('search_project_status','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        request_project_name   = self.request.GET.get('search_project_name','')
        request_project_desc   = self.request.GET.get('search_project_desc','')
        request_project_status = self.request.GET.get('search_project_status','')

        if request_project_name is not None and \
           request_project_desc is not None and \
           request_project_status is not None:
            project =  Project.objects.filter(user=self.request.user,
                                              project_name__contains=request_project_name,
                                              project_desc__contains=request_project_desc,
                                              project_status__contains=request_project_status
	    )

            return project

class AccountTitleSearch(ListView):
    model = AccountTitle
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountTitleSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountTitleSearch,self).get_context_data(**kwargs)

        ctx['search_at_name']   = self.request.GET.get('search_at_name','')
        ctx['search_at_type']   = self.request.GET.get('search_at_type','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        request_at_name = self.request.GET.get('search_at_name','')
        request_at_type   = self.request.GET.get('search_at_type','')

        if request_at_name is not None and \
           request_at_type is not None:
            if request_at_type == "":
                return AccountTitle.objects.filter(user=self.request.user,
                                                   at_name__contains=request_at_name)
            else:
                return AccountTitle.objects.filter(user=self.request.user,
                                                   at_name__contains=request_at_name,
                                                   at_type=request_at_type)

class BankAccountSearch(ListView):
    model = BankAccount
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(BankAccountSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(BankAccountSearch,self).get_context_data(**kwargs)

        ctx['search_ba_name']   = self.request.GET.get('search_ba_name','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        request_ba_name = self.request.GET.get('search_ba_name','')

        if request_ba_name is not None:
            return BankAccount.objects.filter(user=self.request.user,
                                              ba_name__contains=request_ba_name)


class DepositWithdrawalMethodSearch(ListView):
    model = DepositWithdrawalMethod
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(DepositWithdrawalMethodSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DepositWithdrawalMethodSearch,self).get_context_data(**kwargs)

        ctx['search_dwm_name']   = self.request.GET.get('search_dwm_name','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        request_dwm_name = self.request.GET.get('search_dwm_name','')

        if request_dwm_name is not None:
            return DepositWithdrawalMethod.objects.filter(user=self.request.user,
                                                          dwm_name__contains=request_dwm_name)


class AccountBookSearch(ListView):
    model = AccountBook
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookSearch,self).get_context_data(**kwargs)

        search_trade_date_from = self.request.GET.get('search_trade_date_from','')
        search_trade_date_to   = self.request.GET.get('search_trade_date_to','')

        search_trade_date_from = get_defaultdate(search_trade_date_from)
        search_trade_date_to   = get_defaultdate(search_trade_date_to)

        ctx['search_trade_date_from'] = search_trade_date_from
        ctx['search_trade_date_to']   = search_trade_date_to

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name
        
        search_dw_type_select = self.request.GET.get('search_dw_type_select','')

        ctx['search_project'] = Project.objects.filter(user=self.request.user,
                                                       project_status=0)

        if search_dw_type_select == '':
            ctx['search_at'] = None
            ctx['search_dw_type_select'] = ''
        else:
            ctx['search_at'] = AccountTitle.objects.filter(user=self.request.user,
                                                           at_type=search_dw_type_select)
            ctx['search_dw_type_select'] = search_dw_type_select

        search_at_select = self.request.GET.get('search_at_select','')

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)

        ctx['search_at_select'] = search_at_select

        search_project_select   = self.request.GET.get('search_project_select','')

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_project_select!=""):
            search_project_select = int(search_project_select)

        ctx['search_project_select'] = search_project_select

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        info(datetime.date.today().strftime('%Y-%m')+'-01')

        return ctx

    def get_queryset(self):
        search_trade_date_from = self.request.GET.get('search_trade_date_from','')
        search_trade_date_to   = self.request.GET.get('search_trade_date_to','')
        search_dw_type_select   = self.request.GET.get('search_dw_type_select','')
        search_at_select   = self.request.GET.get('search_at_select','')
        search_project_select   = self.request.GET.get('search_project_select','')

        search_trade_date_from = get_defaultdate(search_trade_date_from)
        search_trade_date_to   = get_defaultdate(search_trade_date_to)

        ab = ''
        if search_at_select == '':
            ab = AccountBook.objects.filter(user=self.request.user,
                                              dw_type__contains=search_dw_type_select,
                                            trade_date__range=(search_trade_date_from,
                                                               search_trade_date_to)
            ).order_by('trade_date')
        else:
            ab =  AccountBook.objects.filter(user=self.request.user,
                                              dw_type__contains=search_dw_type_select,
                                            trade_date__range=(search_trade_date_from,
                                                               search_trade_date_to),
                                              at = search_at_select
            )

        if search_project_select=="":
            return ab
        else:
            return ab.filter(project=search_project_select)

##帳簿予定検索
class AccountBookPlanSearch(ListView):
    model = AccountBookPlan
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookPlanSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookPlanSearch,self).get_context_data(**kwargs)

        search_plan_year_month = self.request.GET.get('search_plan_year_month','')

        search_plan_year_month = get_defaultyearmonth(search_plan_year_month)

        ctx['search_plan_year_month'] = search_plan_year_month

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name
        
        search_dw_type_select = self.request.GET.get('search_dw_type_select','')

        ctx['search_project'] = Project.objects.filter(user=self.request.user,
                                                       project_status=0)
        
        if search_dw_type_select == '':
            ctx['search_at'] = None
            ctx['search_dw_type_select'] = ''
        else:
            ctx['search_at'] = AccountTitle.objects.filter(user=self.request.user,
                                                           at_type=search_dw_type_select)
            ctx['search_dw_type_select'] = search_dw_type_select

        search_at_select = self.request.GET.get('search_at_select','')

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)

        ctx['search_at_select'] = search_at_select

        search_project_select   = self.request.GET.get('search_project_select','')

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_project_select!=""):
            search_project_select = int(search_project_select)

        ctx['search_project_select'] = search_project_select

        ctx['search_ab_create_flag_check'] = self.request.GET.get('search_ab_create_flag_check','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        search_plan_year_month   = self.request.GET.get('search_plan_year_month','')
        search_dw_type_select   = self.request.GET.get('search_dw_type_select','')
        search_at_select   = self.request.GET.get('search_at_select','')
        search_project_select   = self.request.GET.get('search_project_select','')
        search_ab_create_flag_check = self.request.GET.get('search_ab_create_flag_check','')

        search_plan_year_month = get_defaultyearmonth(search_plan_year_month)

        ab = ''
        if search_at_select == '':
            ab = AccountBookPlan.objects.filter(user=self.request.user,
                                                dw_type__contains=search_dw_type_select,
                                                plan_year_month=search_plan_year_month
            ).order_by('plan_year_month')
        else:
            ab =  AccountBookPlan.objects.filter(user=self.request.user,
                                                 dw_type__contains=search_dw_type_select,
                                                 plan_year_month=search_plan_year_month,
                                                 at = search_at_select
            ).order_by('plan_year_month')

        if search_project_select=="":
            ab = ab
        else:
            ab = ab.filter(project=search_project_select)

        if search_ab_create_flag_check=="on":
            ab = ab.filter(ab_create_flag="0")

        return ab


##汎用パラメーター検索
class GeneralParameterSearch(ListView):
    model = GeneralParameter
    paginate_by = 5

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(GeneralParameterSearch, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(GeneralParameterSearch,self).get_context_data(**kwargs)
        ctx['search_desc'] = self.get_param('search_desc')
        ctx['validator_name'] = self.get_template_name() + '.js'

        #共通設定
        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        search_desc = self.get_param('search_desc')

        return GeneralParameter.objects.filter(desc__contains=search_desc).order_by('sort_no')

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')

class AccountBookSum(ListView):
    model = AccountBook

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookSum, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookSum,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        search_trade_date = self.request.GET.get('search_trade_date','')

        search_trade_date = get_defaultdate(search_trade_date)

        ctx['search_trade_date'] = search_trade_date

        ctx['dw_0_total'] = 0
        ctx['dw_1_total'] = 0

        ab = AccountBook.objects.filter(user=self.request.user,
                                        trade_date=ctx['search_trade_date']
        )

        ab_list = ab.values('dw_type').annotate(total_money=Sum('ab_money'))

        for ab_dict in ab_list:
            #入金
            if ab_dict['dw_type']=='0':
                ctx['dw_0_total']   = ab_dict['total_money']
            else:
                ctx['dw_1_total']   = ab_dict['total_money']

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        search_trade_date = self.request.GET.get('search_trade_date','')

        search_trade_date = get_defaultdate(search_trade_date)

        ab = AccountBook.objects.filter(user=self.request.user,trade_date=search_trade_date)
        return ab.values('dw_type','at').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')


class AccountBookSumByMonth(ListView):
    model = AccountBook

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookSumByMonth, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookSumByMonth,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        search_trade_month = self.request.GET.get('search_trade_month','')
        search_ab_create_flag_check = self.request.GET.get('search_ab_create_flag_check','')

        if search_trade_month is None or len(search_trade_month)==0:
            present_month = datetime.date.today().strftime('%Y-%m')
            ctx['search_trade_month']   = present_month
        else:
            ctx['search_trade_month']   = search_trade_month

        ctx['search_ab_desc']   = self.request.GET.get('search_ab_desc','')

        ctx['dw_0_total'] = 0
        ctx['dw_1_total'] = 0

        if ctx['search_trade_month'] is not None and len(ctx['search_trade_month']) <> 0:
            first_of_thismonth =  datetime.datetime.strptime(ctx['search_trade_month'] + "-01", '%Y-%m-%d')
            last_of_thismonth  = first_of_thismonth + relativedelta(months=1) - timedelta(days=1)

            #AccountBook
            ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

            ab_list = ab.values('dw_type').annotate(total_money=Sum('ab_money'))

            #Set AccountBook Money
            for ab_dict in ab_list:
                #入金
                if ab_dict['dw_type']=='0':
                    ctx['dw_0_total']   = ab_dict['total_money']
                #出金
                else:
                    ctx['dw_1_total']   = ab_dict['total_money']

            if search_ab_create_flag_check=="on":
                #AccountBookPlan
                abp = AccountBookPlan.objects.filter(user=self.request.user,
                                                     plan_year_month=search_trade_month,
                                                     ab_create_flag="0")

                abp_list = abp.values('dw_type').annotate(total_money=Sum('ab_money'))

                for abp_dict in abp_list:
                    #入金
                    if abp_dict['dw_type']=='0':
                        ctx['dw_0_total']   = ctx['dw_0_total'] + abp_dict['total_money']
                    #出金
                    else:
                        ctx['dw_1_total']   = ctx['dw_1_total'] + abp_dict['total_money']

        ctx['search_ab_create_flag_check'] = self.request.GET.get('search_ab_create_flag_check','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        request_trade_month = self.request.GET.get('search_trade_month','')
        request_ab_desc = self.request.GET.get('search_ab_desc','')

        search_trade_month = self.request.GET.get('search_trade_month','')
        search_ab_create_flag_check = self.request.GET.get('search_ab_create_flag_check','')

        if search_trade_month is None or len(search_trade_month)==0:
            present_month = datetime.date.today().strftime('%Y-%m')
            search_trade_month   = present_month

        first_of_thismonth =  datetime.datetime.strptime(search_trade_month + "-01", '%Y-%m-%d')
        last_of_thismonth  = first_of_thismonth + relativedelta(months=1) - timedelta(days=1)

        ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

        ab = ab.values('dw_type','at').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')

        list_ab = list(ab)

        if search_ab_create_flag_check=="on":
            abp = AccountBookPlan.objects.filter(user=self.request.user,
                                                 plan_year_month=search_trade_month,
                                                 ab_create_flag="0"
            )

            abp = abp.values('dw_type','at').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')

            list_abp = list(abp)

            for item in list_abp:
                item['at_name'] = u'(予定)'+item['at_name']

            list_ab.extend(list_abp)

        return list_ab

#帳簿集計(Project別)
class AccountBookSumByProject(ListView):
    model = AccountBook

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookSumByProject, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookSumByProject,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        search_project_select = self.request.GET.get('search_project_select','')
        search_ab_create_flag_check = self.request.GET.get('search_ab_create_flag_check','')
        
        search_project = Project.objects.filter(user=self.request.user)

        ctx['search_project'] = search_project

        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_project_select!=""):
            search_project_select = int(search_project_select)

        ctx['search_project_select'] = search_project_select

        ctx['dw_0_total'] = 0
        ctx['dw_1_total'] = 0
        ctx['month_list'] = None

        project_select = None
        if search_project_select<>'':
            project_select = Project(user=self.request.user,
                                     id=search_project_select)

        #AccountBook
        if project_select<>None:
            ab = AccountBook.objects.filter(user=self.request.user,
                                            project=project_select)

            ab_list = ab.values('dw_type').annotate(total_money=Sum('ab_money'))

            #Set AccountBook Money
            for ab_dict in ab_list:
                #入金
                if ab_dict['dw_type']=='0':
                    ctx['dw_0_total']   = ab_dict['total_money']
                #出金
                else:
                    ctx['dw_1_total']   = ab_dict['total_money']

            if search_ab_create_flag_check=="on":
                #AccountBookPlan
                abp = AccountBookPlan.objects.filter(user=self.request.user,
                                                     project=project_select,
                                                     ab_create_flag="0")

                abp_list = abp.values('dw_type').annotate(total_money=Sum('ab_money'))

                abp_dw_0_total = 0
                abp_dw_1_total = 0

                for abp_dict in abp_list:
                    if abp_dict['dw_type'] == '0':
                        abp_dw_0_total = abp_dict['total_money']
                    else:
                        abp_dw_1_total = abp_dict['total_money']

                ctx['dw_0_total'] += abp_dw_0_total
                ctx['dw_1_total'] += abp_dw_1_total

            #AccountBook 登録されている月がわかる
            ab_month_list = AccountBook.objects.filter(user=self.request.user,
                                                       project=project_select)

            ab_month_list = ab_month_list.extra({'month': "to_char(trade_date,'YYYY') || '-' || to_char(trade_date,'MM')"})

            ab_month_list = ab_month_list.values('month').annotate(cnt=Count('*'))

            ab_month_list_list = list(ab_month_list)

            abp_month_list = None
            abp_month_list_list = None

            if search_ab_create_flag_check=="on":
                #AccountBookPlan 登録されている月がわかる
                abp_month_list = AccountBookPlan.objects.filter(user=self.request.user,
                                                                project=project_select,
                                                                ab_create_flag="0")

                abp_month_list = abp_month_list.extra({'month': 'plan_year_month'})

                abp_month_list = abp_month_list.values('month').annotate(cnt=Count('*'))

                abp_month_list_list = list(abp_month_list)

                ab_month_list_list.extend(abp_month_list_list)

            month_list = []
            for item in ab_month_list_list:
                if item['month'] not in month_list:
                    month_list.append(item['month'])

            ctx['month_list'] = month_list
        
        ctx['search_ab_create_flag_check'] = self.request.GET.get('search_ab_create_flag_check','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset(self):
        search_project_select = self.request.GET.get('search_project_select','')
        search_ab_create_flag_check = self.request.GET.get('search_ab_create_flag_check','')

        project_select=None
        if(search_project_select!=""):
            search_project_select = int(search_project_select)
            project_select = Project.objects.filter(user=self.request.user,
                                    id=search_project_select)

        list_ab = None
        if project_select<>None:
            ab = AccountBook.objects.filter(user=self.request.user,
                                            project=project_select)
            
            ab = ab.extra({'month': "to_char(trade_date,'YYYY') || '-' || to_char(trade_date,'MM')"})

            ab = ab.values('dw_type','at','month').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')

            list_ab = list(ab)
            
            if search_ab_create_flag_check=="on":
                abp = AccountBookPlan.objects.filter(user=self.request.user,
                                                     project=project_select,
                                                     ab_create_flag="0")

                abp = abp.extra({'month': 'plan_year_month'})                
                
                abp = abp.values('dw_type','at','month').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')

                list_abp = list(abp)

                for item in list_abp:
                    item['at_name'] = u'(予定)'+item['at_name']

                list_ab.extend(list_abp)

        return list_ab


#帳簿集計(年度別)
class AccountBookSumByYear(ListView):
    model = AccountBook

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(AccountBookSumByYear, self).dispatch(request,*args, **kwargs)

    def set_common_ctx(self,ctx):
        template_file_name = self.get_template_name()
        ctx['validator_name'] = template_file_name + '.js'
        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user

    def set_eachdefault_ctx(self,ctx):
        ##
        ctx['search_ab_create_flag_check'] = self.get_param('search_ab_create_flag_check')
        search_project_select = self.get_param('search_project_select')
        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_project_select!=""):
            search_project_select = int(search_project_select)

        ctx['search_project_select'] = search_project_select
        
        ##
        search_project = Project.objects.filter(user=self.request.user)
        ctx['search_project'] = search_project

        ##
        ctx['search_trade_year'] = self.get_param('search_trade_year')
        if ctx['search_trade_year'] == '':
            bom = get_bom(ctx['userid'])
            this_fiscal_year = get_this_fiscal_year(None,bom)
            ctx['search_trade_year'] = this_fiscal_year

        ##
        ctx['dw_0_total'] = 0
        ctx['dw_1_total'] = 0

    def get_context_data(self, **kwargs):
        ctx = super(AccountBookSumByYear,self).get_context_data(**kwargs)
        self.set_common_ctx(ctx)
        self.set_eachdefault_ctx(ctx)

        search_trade_year = ctx['search_trade_year']
        search_ab_create_flag_check = ctx['search_ab_create_flag_check']

        #AccountBook
        ab = self.get_queryset_ab(self.request.user,search_trade_year)
        if ab is not None:
            ab = ab.values('dw_type').annotate(sum_money=Sum('ab_money')).order_by('dw_type')

        #AccountBookPlan
        abp = None
        if search_ab_create_flag_check=="on":
            abp = self.get_queryset_abp(self.request.user,search_trade_year)
            if abp is not None:
                abp = abp.values('dw_type').annotate(sum_money=Sum('ab_money')).order_by('dw_type')

        ab_dw0 = 0
        ab_dw1 = 0
        for item in ab:
            if item['dw_type']=='0':
                ab_dw0 = item['sum_money']
            else:
                ab_dw1 = item['sum_money']

        abp_dw0 = 0
        abp_dw1 = 0

        if abp is not None:
            for item in abp:
                if item['dw_type']=='0':
                    abp_dw0 = item['sum_money']
                else:
                    abp_dw1 = item['sum_money']

        ctx['dw_0_total'] = ab_dw0 + abp_dw0
        ctx['dw_1_total'] = ab_dw1 + abp_dw1

        ctx['is_logined'] = True
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset_ab(self,userid,search_trade_year):
        bom = get_bom(userid)
        first_date_s = search_trade_year + '-' + bom + '-01'
        first_date_d = datetime.datetime.strptime(first_date_s,'%Y-%m-%d')
        last_date_d  = first_date_d + relativedelta(years=1) - timedelta(days=1)
        return AccountBook.objects.filter(user=self.request.user,
                                          trade_date__range=(first_date_d,last_date_d))

    def get_queryset_abp(self,userid,search_trade_year):
        bom = get_bom(userid)
        first_date_s = search_trade_year + '-' + bom + '-01'
        first_date_d = datetime.datetime.strptime(first_date_s,'%Y-%m-%d')
        last_date_d  = first_date_d + relativedelta(years=1) - timedelta(days=1)
        last_year_month = last_date_d.strftime('%Y-%m')
        first_year_month = search_trade_year + '-' + bom

        return AccountBookPlan.objects.filter(user=self.request.user,
                                              ab_create_flag='0',
                                              plan_year_month__range=(first_year_month,last_year_month))

    def get_queryset(self):
        search_project_select = self.get_param('search_project_select')
        search_ab_create_flag_check = self.get_param('search_ab_create_flag_check')
        search_trade_year = self.get_param('search_trade_year')

        if search_trade_year == '':
            bom = get_bom(self.request.user)
            search_trade_year = get_this_fiscal_year(None,bom)

        rtn_list = []
        #AccountBook
        ab_list = None
        ab = self.get_queryset_ab(self.request.user,search_trade_year)
        if ab is not None:
            ab = ab.values('dw_type','at').annotate(
                at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')
            ab_list = list(ab)

        #AccountBookPlan
        abp_list = None
        abp = None
        if search_ab_create_flag_check=="on":
            abp = self.get_queryset_abp(self.request.user,search_trade_year)
            if abp is not None:
                abp = abp.values('dw_type','at').annotate(
                    at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')
                abp_list = list(abp)

        if ab_list is not None:
            rtn_list.extend(ab_list)

        if abp_list is not None:
            for item in abp_list:
                item['at_name'] = u'(予定)'+item['at_name']

            rtn_list.extend(abp_list)

        return rtn_list

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')

#口座残高照会
class BankAccountBalanceInquiry(ListView):
    model = BankAccountBalance

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(BankAccountBalanceInquiry, self).dispatch(request,*args, **kwargs)

    def set_common_ctx(self,ctx):
        template_file_name = self.get_template_name()
        ctx['validator_name'] = template_file_name + '.js'
        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user

    def set_eachdefault_ctx(self,ctx):
        ##
        ctx['dw_0_total'] = 0
        ctx['dw_1_total'] = 0

    def get_context_data(self, **kwargs):
        ctx = super(BankAccountBalanceInquiry,self).get_context_data(**kwargs)
        self.set_common_ctx(ctx)
        self.set_eachdefault_ctx(ctx)

        BankAccountBalance.objects.filter(user=self.request.user,
                           dw_type=1).delete()

        bab = self.get_queryset_bab(self.request.user)
        if bab is not None:
            bab = bab.values('ba').annotate(sum_money=Sum('money')).order_by('ba')

        ab = AccountBook.objects.filter(user=self.request.user,dw_type='1').exclude(dwm__ba=None)
        ab = ab.values('dwm__ba').annotate(ba_name=Max('dwm__ba__ba_name'),sum_money=Sum('ab_money'))

        for item in ab:
            set_bab = BankAccountBalance(user=self.request.user,
                                         trade_date=get_defaultdate(None),
                                         dw_type='1',
                                         ba_id=item['dwm__ba'],
                                         desc=u'引き落し',
                                         money=int(item['sum_money'])*-1)

            set_bab.save()

        ctx['is_logined'] = True
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

        return ctx

    def get_queryset_bab(self,userid):
        bab = BankAccountBalance.objects.filter(user=self.request.user)
        return bab

    def get_queryset(self):
        bab = self.get_queryset_bab(self.request.user)
        bab = bab.values('ba').annotate(ba_name=Max('ba__ba_name'),sum_money=Sum('money'))

        return bab

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')


#データパターン検索
class DataPatternSearch(ListView):
    model = DataPattern

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(DataPatternSearch, self).dispatch(request,*args, **kwargs)

    def set_common_ctx(self,ctx):
        template_file_name = self.get_template_name()
        ctx['validator_name'] = template_file_name + '.js'
        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

    def set_eachdefault_ctx(self,ctx):
        #画面項目セット
        ctx['search_dw_type_select'] = self.get_param('search_dw_type_select')
        search_at_select = self.request.GET.get('search_at_select','')
        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)
        ctx['search_at_select'] = search_at_select

        search_at = AccountTitle.objects.filter(user=self.request.user,
                                                at_type=ctx['search_dw_type_select'])
        ctx['search_at'] = search_at

    def get_context_data(self, **kwargs):
        ctx = super(DataPatternSearch,self).get_context_data(**kwargs)
        self.set_common_ctx(ctx)
        self.set_eachdefault_ctx(ctx)
        return ctx

    def get_queryset(self):
        search_dw_type_select = self.get_param('search_dw_type_select')
        search_at_select = self.get_param('search_at_select')

        dp = DataPattern.objects.filter(user=self.request.user)
        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)
            dp = dp.filter(at=search_at_select)

        rtn_list = dp
        return rtn_list

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')


#データパターン検索
class DataPatternUseSearch(ListView):
    model = DataPatternUse

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/common/login/?next=%s' % request.path)
        else:
            return super(DataPatternUseSearch, self).dispatch(request,*args, **kwargs)

    def set_common_ctx(self,ctx):
        template_file_name = self.get_template_name()
        ctx['validator_name'] = template_file_name + '.js'
        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user
        ctx['menu_category_list'] = MENU_CATEGORY_LIST

    def set_eachdefault_ctx(self,ctx):
        #画面項目セット
        ctx['search_dw_type_select'] = self.get_param('search_dw_type_select')
        search_at_select = self.request.GET.get('search_at_select','')
        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)
        ctx['search_at_select'] = search_at_select

        search_at = DataPattern.objects.filter(user=self.request.user,
                                               at__at_type=ctx['search_dw_type_select'])

        search_at = search_at.values('at__id').annotate(id=Max('at__id'),at_name=Max('at__at_name'))

        ctx['search_at'] = search_at

    def get_context_data(self, **kwargs):
        ctx = super(DataPatternUseSearch,self).get_context_data(**kwargs)
        self.set_common_ctx(ctx)
        self.set_eachdefault_ctx(ctx)
        return ctx

    def get_queryset(self):
        search_dw_type_select = self.get_param('search_dw_type_select')
        search_at_select = self.get_param('search_at_select')

        dpu = DataPatternUse.objects.filter(user=self.request.user)
        # templateの組み込みタグでの比較を行うために数値変換を行う
        if(search_at_select!=""):
            search_at_select = int(search_at_select)
            dpu = dpu.filter(at=search_at_select)

        dpu = dpu.values('trade_date','at__at_type','at').annotate(at_name=Max('at__at_name'))

        rtn_list = dpu
        return rtn_list

    def get_template_name(self):
        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name)
        return validator_name

    def get_param(self,param_name):
        return self.request.GET.get(param_name,'')


def info(msg):
    logger = logging.getLogger('command')
    logger.info(msg)


def get_defaultdate(v_date):
    today = datetime.date.today().strftime('%Y-%m-%d')

    if v_date is None or len(v_date)==0:
        return today
    else:
        return v_date


def get_defaultyearmonth(v_year_month):
    this_year_month = datetime.date.today().strftime('%Y-%m')

    if v_year_month is None or len(v_year_month)==0:
        return this_year_month
    else:
        return v_year_month

#今年度の取得
def get_this_fiscal_year(v_date,v_bom):
    v_year_month = None
    if v_date is not None:
        v_year_month = v_date[0:7]

    year_month = get_defaultyearmonth(v_year_month)

    adjust_num = -1 * (int(v_bom) - 1)

    base_date_s = year_month + '-01'
    base_date_d = datetime.datetime.strptime(base_date_s,'%Y-%m-%d')
    adjust_result_date = base_date_d + relativedelta(months=adjust_num)
    this_fiscal_year = adjust_result_date.strftime('%Y')

    return this_fiscal_year

def get_bom(userid):
    gp_bom = GeneralParameter.objects.filter(user=userid,
                                             name='bom')
    bom = None
    for item in gp_bom:
        bom = item.param1
        
    return bom
    
