from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from Display.models import User


class FormL(forms.Form):
    name = forms.CharField(min_length=4, label="姓名", error_messages={"required": "该字段不能为空!"})
    pwd = forms.CharField(label='密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码', error_messages={'invalid': u"验证码错误"})

    def clean_name(self):  # 局部钩子
        val = self.cleaned_data.get("name")
        if not User.objects.filter(username=val):
            raise ValidationError("用户不存在！")
        else:
            return val

    def clean(self):
        val = self.cleaned_data.get("pwd")
        obj = User.objects.filter(username=self.cleaned_data.get("name"))
        if obj:
            obj = obj.values()[0]
            if (check_password(val, obj.get('password'))):
                return self.cleaned_data
            else:
                raise ValidationError("用户名或密码错误~")


class FormR(forms.Form):
    name = forms.CharField(min_length=6, label="姓名", error_messages={"required": "该字段不能为空!"},
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}))
    pwd = forms.CharField(min_length=4, label='密码',
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd'}))
    pwd2 = forms.CharField(min_length=4, label='再输一次密码',
                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd2'}))
    captcha = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'captcha'}))
    email = forms.EmailField(label="电子邮箱", widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
    phone = forms.CharField(label="电话", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}))
    sex_choices = [['male', 'male'], ['female', 'femal']]
    sex = forms.ChoiceField(label='性别', widget=forms.Select(attrs={'class': 'form-control', 'id': 'sex'}),
                            choices=sex_choices, initial='male')

    def clean_name(self):  # 局部钩子
        val = self.cleaned_data.get("name")
        if User.objects.filter(username=val):
            raise ValidationError("用户已存在！")
        else:
            return val

    def clean_pwd2(self):
        pwd = self.cleaned_data.get('pwd')
        pwd2 = self.cleaned_data.get('pwd2')
        if (pwd != pwd2):
            raise ValidationError("两次密码不一致")
        else:
            return pwd2


class FormF(forms.Form):
    captcha = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'captcha'}))
    email = forms.EmailField(label="电子邮箱", widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
    pwd = forms.CharField(min_length=4, label='密码',
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd'}))
    pwd2 = forms.CharField(min_length=4, label='再输一次密码',
                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd2'}))
