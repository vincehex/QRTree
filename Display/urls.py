from django.urls import path, include

from .views import login, register, logout, sendRegisterEmail, findPwd, sendFindEmail, changeinfo

urlpatterns = [
    path('login', login),
    path('register', register),
    path('captcha', include('captcha.urls')),
    path('logout', logout),
    path('registeremail/<str:email>', sendRegisterEmail),
    path('find', findPwd),
    path('findemail/<str:email>', sendFindEmail),
    path('changeinfo', changeinfo),
]
