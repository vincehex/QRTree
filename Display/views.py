import qrcode
from django.http import HttpResponse
from django.shortcuts import render

from .models import TreeInformation, TreeType, User


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def tree(request):
    list = TreeInformation.objects.all()
    trees = []
    for i in list:
        im = qrcode.make(i.img)
        im.save('./statics/QRCode/' + str(i.id))
        trees.append({'id': i.id, 'imgUrl': i.img, 'height': i.height, 'width': i.width})
    return render(request, 'projects.html', {'trees': trees})


def tree_detail(request, id):
    obj = TreeInformation.objects.get(id=id)
    type = TreeType.objects.get(id=obj.type_id)
    if (obj.user_id is None):
        name = "暂无"
    else:
        name = User.objects.get(obj.user_id)
    return render(request, 'project-details.html', {'detail': obj, 'type': type, 'name': name})


def contact(request):
    return render(request, 'contact.html')


def showUpload(request, img):
    return HttpResponse('<img src="/static/upload/%s" />' % img)
