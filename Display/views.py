from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def team(request):
    return render(request, 'team.html')


def contact(request):
    return render(request, 'contact.html')


def showUpload(request, img):
    return HttpResponse('<img src="/static/upload/%s" />' % img)
