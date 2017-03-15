from django.shortcuts import render
from django.views.generic import *
from django.views.generic.edit import *

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *

APP_NAME = 'common'

class MyPage(ListView):
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/%s/login/?next=%s' % (APP_NAME,request.path))
        else:
            return super(MyPage, self).dispatch(request,*args, **kwargs)

    def get_queryset(self):
        return Menu.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super(MyPage,self).get_context_data(**kwargs)
        ctx['is_logined'] = True
        ctx['userid']   = self.request.user

        return ctx


