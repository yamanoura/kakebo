from django.conf.urls import url

from . import views
from .forms import *
from .models import *

APP_NAME = 'app'

urlpatterns = [
    #BaseCreateView
    url(r'^project/add$', views.BaseCreateView.as_view(model=Project,form_class=ProjectForm),
        name='project_add'),
    url(r'^at/add$', views.BaseCreateView.as_view(template_name='%s/at_form.html' % APP_NAME,
                                                  model=AccountTitle,
                                                  form_class=AccountTitleForm),
        name='at_add'),

    #BaseUpdateView
    url(r'^project/edit/(?P<pk>\d+)$', 
        views.BaseUpdateView.as_view(model=Project,form_class=ProjectForm),
        name='project_edit'),
    url(r'^at/edit/(?P<pk>\d+)$',
        views.BaseUpdateView.as_view(template_name='%s/at_form.html' % APP_NAME,
                                     model=AccountTitle,
                                     form_class=AccountTitleForm),
        name='at_edit'),

    #BaseDeleteView
    url(r'^project/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=Project),
        name='project_delete'),
    url(r'^at/delete/(?P<pk>\d+)$', 
        views.BaseDeleteView.as_view(model=AccountTitle,
                                     template_name='%s/at_confirm_delete.html' % APP_NAME),
        name='at_delete'),

    #BaseListView
    url(r'^project/search$', views.ProjectSearch.as_view(template_name='%s/project_list.html' % APP_NAME),name='project_search'),
    url(r'^at/search$', views.AccountTitleSearch.as_view(template_name='%s/at_list.html' % APP_NAME),name='at_search'),

]
