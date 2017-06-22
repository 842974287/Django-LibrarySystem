# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from Library.models import *
from django import forms
import time
# Create your views here.

def HomePage(request):
    return render(request, 'HomePage.html')

def ReaderInfo(request):
    return render(request, 'ReaderInfo.html')

class LoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        max_length = 20,
        widget = forms.TextInput(attrs = {'placeholder': '用户名'}),
        error_messages = {'required': '用户名不能为空.', 'max_length': '最多20位'},
    )
    pwd = forms.CharField(
        required = True,
        max_length = 20,
        widget = forms.TextInput(attrs={'placeholder': '密码', 'type': 'password'}),
        error_messages = {'required': '密码不能为空.', 'max_length':"最多20位"},
    )
    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('pwd')
        user = LibraryUser.objects.filter(Username = username)
        if not user:
            raise forms.ValidationError('用户不存在!')
        else:
            if user.Password != password:
                raise forms.ValidationError('密码错误!')
        return cleaned_data

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class RegisterForm(forms.Form):
    username = forms.CharField(
        required = True,
        min_length = 6,
        max_length = 20,
        error_messages = {'required': '用户名不能为空', 'min_length': '用户名至少6位', 'max_length': '用户名最多16位'},
    )
    pwd = forms.CharField(
        required = True,
        max_length = 20,
        widget = forms.PasswordInput,
        error_messages = {'required': '密码不能为空', 'max_length': '密码最多20位'},
    )
    pwd2 = forms.CharField(
        required = False,
        max_length = 20,
        widget = forms.PasswordInput,
    )
    phone = forms.CharField(
        validators = [mobile_validate],
        required = True,
        error_messages = {'required': '手机号码不能为空'},
    )

    def clean_user(self):
        pattern = re.compile(u"[\u4e00-\u9fa5]+")
        username = self.cleaned_data.get('username')
        if pattern.findall(username):
            raise forms.ValidationError('用户名不允许输入中文')
            return username
        user = LibraryUser.objects.filter(UserID = user)
        if user:
            raise forms.ValidationError('用户名已经注册!')
        return username

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('pwd') and cleaned_data.has_key('pwd2'):
            pwd = cleaned_data['pwd']
            pwd2 = cleaned_data['pwd2']
            if pwd != pwd2:
                raise forms.ValidationError('二次输入密码不匹配')
        return cleaned_data

@csrf_exempt
def UserCheck(request):
    if request.POST:
        username = request.POST.get('username')
        user = LibraryUser.objects.filter(Username = username)
        if user:
            dic = {'info': 1}
            data = json.dumps(dic)
            return HttpResponse(data)
        else:
            dic={'info': 0}
            data = json.dumps(dic)
            return HttpResponse(data)

@csrf_exempt
def Register(request):
    if request.POST:
        objPost = RegisterForm(request.POST)
        ret = objPost.is_valid()
        if ret:
            username = objPost.cleaned_data['username']
            password = objPost.cleaned_data['pwd']
            telephone = objPost.cleaned_data['phone']
            user = LibraryUser(Username = username, Password = password)
            user.save()
            Reader(ReaderId = time.strftime("%Y%m%d%H%M%S", time.gmtime()), Telephone = phone, User = user)
            request.session['username'] = username
            return HttpResponseRedirect('/ReaderInfo/')
        return render(request, 'Register.html', {'obj1': objPost})
    else:
        if not request.session.has_key('username'):
            objGet = RegisterForm()
            return render(request, 'Register.html', {'obj1': objGet})
        return HttpResponseRedirect('/ReaderInfo/')

@csrf_exempt
def Login(request):
    context = {}
    if request.POST:
        objPost = LoginForm(request.POST)
        ret = objPost.is_valid()
        if ret:
            username = objPost.cleaned_data['username']
            request.session['username'] = username
            user = LibraryUser.objects.get(Username = username)
            context['UserType'] = 1
            return HttpResponseRedirect('/PersonalInfo/')
        context['obj1'] = objPost
        return render(request,'Login.html', context)
    else:
        if not request.session.has_key('UserID'):
            objGet = LoginForm()
            context['obj1'] = objGet
            return render(request,'Login.html', context)
        return HttpResponseRedirect('/ReaderInfo/')

@csrf_exempt
def Logout(request):
    if request.session.has_key('username'):
        request.session.pop('username')
    return HttpResponseRedirect('/Login/')
