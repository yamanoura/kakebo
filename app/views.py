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
        class_object = self.get_object()
        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(class_object, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        class_object = self.get_object()
        form.instance.user = self.request.user
        return super(class_object, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(BaseCreateView,self).get_context_data(**kwargs)
        ctx['is_logined'] = True
        ctx['is_addmode'] = True
        return ctx

    def get_form_kwargs(self):
        class_object = self.get_object()
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
class BaseUpdateView(UpdateView):
    success_url = SUCCESS_URL

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(AUTH_FAILURE % request.path)
        else:
            return super(BaseUpdateView, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BaseUpdateView, self).form_valid(form) 
        return render(self.request,self.template_name,
                      self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(BaseUpdateView,self).get_context_data(**kwargs)
        ctx['is_logined'] = True
        ctx['is_addmode'] = False
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

        ctx['search_trade_date']   = self.request.GET.get('search_trade_date','')
        ctx['search_ab_desc']   = self.request.GET.get('search_ab_desc','')

        ctx['is_logined'] = True
        ctx['query_string'] = self.request.GET.urlencode()

        return ctx

    def get_queryset(self):
        request_trade_date = self.request.GET.get('search_trade_date','')
        request_ab_desc = self.request.GET.get('search_ab_desc','')

        if request_ab_desc is not None:
            return AccountBook.objects.filter(user=self.request.user,
                                              ab_desc__contains=request_ab_desc)

