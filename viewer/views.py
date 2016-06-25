from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    contex={}
    return HttpResponse("<h1>DA</h1>")
    #return render(request, 'viewer/index.html', contex)
