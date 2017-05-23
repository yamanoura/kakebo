#coding=UTF8
from django.conf.urls import url

from . import views
from .forms import *
from .models import *

APP_NAME = 'app'

urlpatterns = [
    #BaseCreateView
    url(r'^project/add$', views.BaseCreateView.as_view(template_name='%s/project_form.html' % APP_NAME,
                                                       model=Project,
                                                       form_class=ProjectForm),
    name='project_add'),
    ##帳簿情報
    #入金用
    url(r'^ab_d/add$', views.BaseCreateView.as_view(template_name='%s/ab_d_form.html' % APP_NAME,
                                                  model=AccountBook,
                                                  form_class=AccountBookDepositForm),
    name='ab_d_add'),
    #出金用
    url(r'^ab_w/add$', views.BaseCreateView.as_view(template_name='%s/ab_w_form.html' % APP_NAME,
                                                  model=AccountBook,
                                                  form_class=AccountBookWithdrawalForm),
    name='ab_w_add'),
    ##予定情報
    #入金用
    url(r'^ab_plan_d/add$',views.BaseCreateView.as_view(template_name='%s/ab_plan_d_form.html'%APP_NAME,
                                                  model=AccountBookPlan,
                                                  form_class=AccountBookPlanDepositForm),
    name='ab_plan_d_add'),
    #出金用
    url(r'^ab_plan_w/add$',views.BaseCreateView.as_view(template_name='%s/ab_plan_w_form.html'%APP_NAME,
                                                  model=AccountBookPlan,
                                                  form_class=AccountBookPlanWithdrawalForm),
    name='ab_plan_w_add'),

    url(r'^at/add$', views.BaseCreateView.as_view(template_name='%s/at_form.html' % APP_NAME,
                                                  model=AccountTitle,
                                                  form_class=AccountTitleForm),
    name='at_add'),
    url(r'^ba/add$', views.BaseCreateView.as_view(template_name='%s/ba_form.html' % APP_NAME,
                                                  model=BankAccount,
                                                  form_class=BankAccountForm),
    name='ba_add'),
    url(r'^dwm/add$', views.BaseCreateView.as_view(template_name='%s/dwm_form.html' % APP_NAME,
                                                  model=DepositWithdrawalMethod,
                                                  form_class=DepositWithdrawalMethodForm),
    name='dwm_add'),
    url(r'^gp/add$', views.BaseCreateView.as_view(template_name='%s/gp_form.html' % APP_NAME,
                                                  model=GeneralParameter,
                                                  form_class=GeneralParameterForm),
    name='gp_add'),

    url(r'^dp/add$', views.BaseCreateView.as_view(template_name='%s/dp_form.html' % APP_NAME,
                                                  model=DataPattern,
                                                  form_class=DataPatternForm),
    name='dp_add'),

    #データパターン利用登録
    url(r'^dp_use/add$', views.BaseListCreateView.as_view(
        template_name='%s/dp_use_listform.html' % APP_NAME,
        model=DataPatternUse),
    name='dp_use_add'),


    #BaseUpdateView
    url(r'^project/edit/(?P<pk>\d+)$', 
        views.BaseUpdateView.as_view(template_name='%s/project_form.html' % APP_NAME,
                                     model=Project,
                                     form_class=ProjectForm),
    name='project_edit'),

    ##帳簿情報
    #入金用
    url(r'^ab_d/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/ab_d_form.html' % APP_NAME,
                                     model=AccountBook,
                                     form_class=AccountBookDepositForm),
    name='ab_d_edit'),

    #出金用
    url(r'^ab_w/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/ab_w_form.html' % APP_NAME,
                                     model=AccountBook,
                                     form_class=AccountBookWithdrawalForm),
    name='ab_w_edit'),

    ##帳簿予定
    #入金用
    url(r'^ab_plan_d/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/ab_plan_d_form.html' % APP_NAME,
                                     model=AccountBookPlan,
                                     form_class=AccountBookPlanDepositForm),
    name='ab_plan_d_edit'),

    #出金用
    url(r'^ab_plan_w/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/ab_plan_w_form.html' % APP_NAME,
                                     model=AccountBookPlan,
                                     form_class=AccountBookPlanWithdrawalForm),
    name='ab_plan_w_edit'),

    url(r'^at/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/at_form.html' % APP_NAME,
                                     model=AccountTitle,
                                     form_class=AccountTitleForm),
    name='at_edit'),

    url(r'^ba/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/ba_form.html' % APP_NAME,
                                     model=BankAccount,
                                     form_class=BankAccountForm),
    name='ba_edit'),

    url(r'^dwm/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/dwm_form.html' % APP_NAME,
                                     model=DepositWithdrawalMethod,
                                     form_class=DepositWithdrawalMethodForm),
    name='dwm_edit'),

    url(r'^gp/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/gp_form.html' % APP_NAME,
                                     model=GeneralParameter,
                                     form_class=GeneralParameterForm),
    name='gp_edit'),

    url(r'^dp/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/dp_form.html' % APP_NAME,
                                     model=DataPattern,
                                     form_class=DataPatternForm),
    name='dp_edit'),


    #BaseDeleteView
    url(r'^project/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=Project),
        name='project_delete'),

    #帳簿情報
    url(r'^ab/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=AccountBook,
                                     template_name='%s/ab_confirm_delete.html' % APP_NAME),
        name='ab_delete'),

    ##予定情報
    url(r'^ab_plan/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=AccountBookPlan,
                                     template_name='%s/ab_plan_confirm_delete.html' % APP_NAME),
        name='ab_plan_delete'),

    url(r'^at/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=AccountTitle,
                                     template_name='%s/at_confirm_delete.html' % APP_NAME),
    name='at_delete'),

    url(r'^dwm/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=DepositWithdrawalMethod,
                                     template_name='%s/dwm_confirm_delete.html' % APP_NAME),
    name='dwm_delete'),

    url(r'^ba/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=BankAccount,
                                     template_name='%s/ba_confirm_delete.html' % APP_NAME),
    name='ba_delete'),

    #汎用パラメーター
    url(r'^gp/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=GeneralParameter,
                                     template_name='%s/gp_confirm_delete.html' % APP_NAME),
        name='gp_delete'),

    url(r'^dp/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=DataPattern,
                                     template_name='%s/dp_confirm_delete.html' % APP_NAME),
    name='dp_delete'),



    #BaseListView
    url(r'^project/search$', views.ProjectSearch.as_view(
        template_name='%s/project_list.html' % APP_NAME),
    name='project_search'),

    #帳簿情報
    url(r'^ab/search$', views.AccountBookSearch.as_view(
        template_name='%s/ab_list.html' % APP_NAME),
    name='ab_list'),

    #帳簿予定
    url(r'^ab_plan/search$', views.AccountBookPlanSearch.as_view(
        template_name='%s/ab_plan_list.html'%APP_NAME),
    name='ab_plan_list'),


    url(r'^at/search$', views.AccountTitleSearch.as_view(
        template_name='%s/at_list.html' % APP_NAME),
    name='at_search'),

    url(r'^ba/search$', views.BankAccountSearch.as_view(
        template_name='%s/ba_list.html' % APP_NAME),
    name='ba_search'),

    url(r'^dwm/search$', views.DepositWithdrawalMethodSearch.as_view(
        template_name='%s/dwm_list.html' % APP_NAME),
    name='dwm_search'),

    url(r'^gp/search$', views.GeneralParameterSearch.as_view(
        template_name='%s/gp_list.html' % APP_NAME),
    name='gp_search'),

    #データパターン
    url(r'^dp/search$', views.DataPatternSearch.as_view(
        template_name='%s/dp_list.html' % APP_NAME),
    name='dp_search'),

    #データパターン利用データ
    url(r'^dp_use/search$', views.DataPatternUseSearch.as_view(
        template_name='%s/dp_use_list.html' % APP_NAME),
    name='dp_use_search'),



    #帳簿集計（日別）
    url(r'^ab/sum$', views.AccountBookSum.as_view(
        template_name='%s/ab_sum_list.html' % APP_NAME),
    name='ab_sum'),

    #帳簿集計（月別）
    url(r'^ab/sum_by_month$', views.AccountBookSumByMonth.as_view(
        template_name='%s/ab_sum_by_month_list.html' % APP_NAME),
    name='ab_sum_by_month'),

    #帳簿集計（年度別）
    url(r'^ab/sum_by_year$', views.AccountBookSumByYear.as_view(
        template_name='%s/ab_sum_by_year_list.html' % APP_NAME),
    name='ab_sum_by_year'),

    #帳簿集計（Project別）
    url(r'^ab/sum_by_project$', views.AccountBookSumByProject.as_view(
        template_name='%s/ab_sum_by_project_list.html' % APP_NAME),
    name='ab_sum_by_project'),

    #口座残高照会
    url(r'^bab/inquiry$', views.BankAccountBalanceInquiry.as_view(
        template_name='%s/bab_inquiry.html' % APP_NAME),
    name='bab_inquiry'),



]
