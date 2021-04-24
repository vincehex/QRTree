from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .email_send import sendEmail
from .form import FormL, FormR, FormF, FormC
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
        trees.append({'id': i.id, 'imgUrl': i.img, 'height': i.height, 'width': i.width})
    return render(request, 'projects.html', {'trees': trees})


def tree_detail(request, id):
    obj = TreeInformation.objects.get(id=id)
    type = TreeType.objects.get(id=obj.type_id)
    if (obj.user_id is None):
        name = "暂无"
    else:
        name = User.objects.get(id=obj.user_id)
    return render(request, 'project-details.html', {'detail': obj, 'type': type, 'name': name})


def contact(request):
    return render(request, 'contact.html')


def showUpload(request, img):
    return HttpResponse('<img src="/static/upload/%s" />' % img)


def login(request):
    # if request.method=="POST":
    #     data = request.POST
    #     msg = "登录失败"
    #     print(type(User.objects))
    #     obj = User.objects.filter(username = data.get('username'))
    #     if(obj is not None and len(obj) > 0):
    #         obj = obj.values()[0]
    #         if(check_password(data.get('pwd'), obj.get('password'))):
    #             msg = ""
    # return render(request, 'index.html', {'msg': msg})

    if request.method == "GET":
        form = FormL()  # 初始化form对象
        key = CaptchaStore.generate_key()
        imgUrl = captcha_image_url(key)
        return render(request, "login.html", locals())
    else:
        form = FormL(request.POST)  # 将数据传给form对象
        if form.is_valid():  # 进行校验
            data = form.cleaned_data
            request.session['username'] = data.get('name')
            request.session['is_login'] = True
            return redirect("/index")
        else:  # 校验失败
            key = CaptchaStore.generate_key()
            imgUrl = captcha_image_url(key)
            clear_errors = form.errors.get("__all__")  # 获取全局钩子错误信息
            return render(request, "login.html", locals())


def register(request):
    if request.method == "GET":
        form = FormR()  # 初始化form对象
        return render(request, "register.html", locals())
    else:
        form = FormR(request.POST)  # 将数据传给form对象
        if form.is_valid():  # 进行校验
            data = form.cleaned_data
            if (request.session.get('code') != data.get('captcha')):
                clear_errors = "验证码无效！"
                return render(request, "register.html", {'form': form, 'clear_errors': clear_errors})
            elif User.objects.filter(email=data.get('email')):
                clear_errors = "该邮箱已被注册！"
                return render(request, "register.html", {'form': form, 'clear_errors': clear_errors})
            User.objects.create(username=data.get('name'), password=data.get('pwd'), email=data.get('email'),
                                phone=data.get('phone'), sex=data.get('sex'))
            request.session['username'] = data.get('name')
            request.session['is_login'] = True
            return redirect("/index")
        else:  # 校验失败
            clear_errors = form.errors.get("__all__")  # 获取全局钩子错误信息
            return render(request, "register.html", locals())


def logout(request):
    if (request.session):
        request.session.flush()
    return render(request, 'index.html')


def sendRegisterEmail(request, email):
    code = sendEmail(email, "register")
    request.session['code'] = code
    return HttpResponse("")


def sendFindEmail(request, email):
    code = sendEmail(email, '找回密码')
    request.session['code'] = code
    return HttpResponse("")


def findPwd(request):
    if request.method == "GET":
        form = FormF()  # 初始化form对象
        return render(request, "findPwd.html", locals())
    else:
        form = FormF(request.POST)  # 将数据传给form对象
        if form.is_valid():  # 进行校验
            data = form.cleaned_data
            # if(request.session.get('code') != data.get('captcha')):
            #     clear_errors = "验证码无效！"
            #     return render(request, "findPwd.html", {'form': form, 'clear_errors': clear_errors})
            obj = User.objects.filter(email=data.get('email'))
            if not obj:
                clear_errors = "邮箱无效"
                return render(request, "findPwd.html", {'form': form, 'clear_errors': clear_errors})
            obj.update(password=make_password(data.get('pwd')))
            return redirect("/login")
        else:  # 校验失败
            clear_errors = form.errors.get("__all__")  # 获取全局钩子错误信息
            return render(request, "findPwd.html", locals())


def changeinfo(request):
    username = request.session.get("username")
    obj = User.objects.filter(username=username)
    if request.method == "GET":
        form = FormC()  # 初始化form对象
        obj = obj.values()[0]
        dict = {'pwd': obj.get('password'), 'sex': obj.get('sex'), 'phone': obj.get('phone')}
        return render(request, "changeinfo.html", dict)
    else:
        form = FormC(request.POST)  # 将数据传给form对象
        if form.is_valid():  # 进行校验
            data = form.cleaned_data
            print(data)
            dict = {}
            if (data.get('pwd') != ''):
                dict['password'] = make_password(data.get('pwd'))
            if (data.get('sex') != ''):
                dict['sex'] = data.get('sex')
            if (data.get('phone') != ''):
                dict['phone'] = data.get('phone')

            print(dict)
            # obj.update(dict)
            return redirect("/")
        else:  # 校验失败
            clear_errors = form.errors.get("__all__")  # 获取全局钩子错误信息
            return render(request, "changeinfo.html", locals())
