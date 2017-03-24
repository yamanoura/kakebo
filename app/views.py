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

# util
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import logging
from django.db.models import Sum
from django.db.models import Max
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
        info('get_context_date')
        ctx = super(BaseCreateView,self).get_context_data(**kwargs)

        template_file_name = re.sub(r'^'+ APP_NAME + '/', '', self.template_name)
        validator_name = re.sub(r'.html$','',template_file_name) + '.js'

        ctx['validator_name'] = validator_name

        ctx['is_logined'] = True
        ctx['is_addmode'] = True
        ctx['userid']   = self.request.user
        return ctx

    def get_form_kwargs(self):
        info('get_form_kwargs')
        class_object = self.get_object()
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        info('form_valid')
        class_object = self.get_object()
        form.instance.user = self.request.user

        return super(class_object, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))


        
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
        validator_name = re.sub(r'.html$','',template_file_name)

        if (validator_name == 'ab_plan_w_form' or validator_name == 'ab_plan_d_form') and class_object.ab_create_flag=='1':
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

            ab = AccountBook(user=self.request.user,
                        trade_date=get_defaultdate(None),
                        dw_type=class_object.dw_type,
                        at=set_at,
                        dwm=set_dwm,
                        project=set_project,
                        ab_desc=class_object.ab_desc,
                        ab_money=class_object.ab_money
            )

            ab.save()


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

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()
        ctx['userid']   = self.request.user

        return ctx

    def get_queryset(self):
        search_plan_year_month   = self.request.GET.get('search_plan_year_month','')
        search_dw_type_select   = self.request.GET.get('search_dw_type_select','')
        search_at_select   = self.request.GET.get('search_at_select','')
        search_project_select   = self.request.GET.get('search_project_select','')

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
            return ab
        else:
            return ab.filter(project=search_project_select)


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
            ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

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

        return ctx

    def get_queryset(self):
        request_trade_month = self.request.GET.get('search_trade_month','')
        request_ab_desc = self.request.GET.get('search_ab_desc','')

        search_trade_month = self.request.GET.get('search_trade_month','')

        if search_trade_month is None or len(search_trade_month)==0:
            present_month = datetime.date.today().strftime('%Y-%m')
            search_trade_month   = present_month

        first_of_thismonth =  datetime.datetime.strptime(search_trade_month + "-01", '%Y-%m-%d')
        last_of_thismonth  = first_of_thismonth + relativedelta(months=1) - timedelta(days=1)

        ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

        return ab.values('dw_type','at').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')

class PlanReusltSumByMonth(ListView):
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
            ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

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

        return ctx

    def get_queryset(self):
        request_trade_month = self.request.GET.get('search_trade_month','')
        request_ab_desc = self.request.GET.get('search_ab_desc','')

        search_trade_month = self.request.GET.get('search_trade_month','')

        if search_trade_month is None or len(search_trade_month)==0:
            present_month = datetime.date.today().strftime('%Y-%m')
            search_trade_month   = present_month

        first_of_thismonth =  datetime.datetime.strptime(search_trade_month + "-01", '%Y-%m-%d')
        last_of_thismonth  = first_of_thismonth + relativedelta(months=1) - timedelta(days=1)

        ab = AccountBook.objects.filter(user=self.request.user,
                                            trade_date__range=(first_of_thismonth,last_of_thismonth))

        return ab.values('dw_type','at').annotate(at_name=Max('at__at_name'),sum_money=Sum('ab_money')).order_by('dw_type')



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

