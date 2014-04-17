import logging


from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.template.context import RequestContext

from apps.blog.forms import UserRegisterForm


def home(request):
    return render(request, "core/home.html")


#def example_00(request):
    #return HttpResponse("<html><b>Esto es HTML crudo!!</b></html>", RequestContext(request))

#def example_01(request):
    #return render_to_response("core/home.html", {}, RequestContext(request))

#def example_02(request):
    #return render(request, "core/home.html", {'user': 'Martin'})

#def example(request):
    #logging.critical("[VIEW] Entro en la vista!")
    #return HttpResponse("Renderizo!!", RequestContext(request))
