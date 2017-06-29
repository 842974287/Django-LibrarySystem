# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from Library.models import *
from django import forms
import time
import re
import json
# Create your views here.

def HomePage(request):
    context = {}
    if request.session.has_key('username'):
        context = {'Login_active': True}
    return render(request, 'HomePage.html', context)

def MyBook(request):
    context = {}
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/Login/')
    username = request.session.get('username')
    user = LibraryUser.objects.get(Username = username)
    reader = Reader.objects.get(User = user)
    context['bookSet'] = ShowMyBooks(reader)
    context['Login_active'] = True
    return render(request, 'MyBookPage.html', context)

def ReturnBookPage(request):
    context = {}
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/Login/')
    username = request.session.get('username')
    user = LibraryUser.objects.get(Username = username)
    if user.Type == 0:
        return HttpResponseRedirect('/ReaderInfo/')
    context['readerSet'] = ShowAllReaders()
    context['Login_active'] = True
    return render(request, 'ReturnBookPage.html', context)

def BeginReturnPage(request):
    context = {}
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/Login/')
    username = request.session.get('username')
    user = LibraryUser.objects.get(Username = username)
    if user.Type == 0:
        return HttpResponseRedirect('/ReaderInfo/')
    try:
        un = request.GET.get('id')
        u = LibraryUser.objects.get(Username = un)
        reader = Reader.objects.get(User = u)
    except Exception as e:
        return HttpResponse(e)
    context['bookSet'] = ShowMyBooks(reader)
    context['Login_active'] = True
    return render(request, 'BeginReturnPage.html', context)

def ReaderInfo(request):
    context = {}
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/Login/')
    username = request.session.get('username')
    user = LibraryUser.objects.get(Username = username)
    reader = Reader.objects.get(User = user)
    if reader.Gender == 0:
        Gender = '保密'
    elif reader.Gender == 1:
        Gender = '男'
    else:
        Gender = '女'
    usera = {
        'ReaderName': reader.ReaderName,
        'Gender': Gender,
        'Username': username,
        'MaxBook': reader.MaxBook,
        'Borrowed': reader.Borrowed,
        'Telephone': reader.Telephone,
    }
    if user.Type == 1:
        context['admin'] = True
    context['Login_active'] = True
    context['user'] = usera
    return render(request, 'ReaderInfo.html', context)

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
        try:
            user = LibraryUser.objects.get(Username = username)
        except Exception as e:
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
        widget = forms.TextInput(attrs = {'placeholder': '在6位与20位之间'}),
        error_messages = {'required': '用户名不能为空', 'min_length': '用户名至少6位', 'max_length': '用户名最多16位'},
    )
    pwd = forms.CharField(
        required = True,
        max_length = 20,
        min_length = 6,
        widget = forms.PasswordInput(attrs = {'placeholder': '在6位与20位之间'}),
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
    context = {}
    if request.POST:
        objPost = RegisterForm(request.POST)
        ret = objPost.is_valid()
        if ret:
            username = objPost.cleaned_data['username']
            password = objPost.cleaned_data['pwd']
            telephone = objPost.cleaned_data['phone']
            user = LibraryUser(Username = username, Password = password)
            user.save()
            Reader(ReaderId = time.strftime("%Y%m%d%H%M%S", time.gmtime()), Telephone = telephone, User = user).save()
            request.session['username'] = username
            context['UserType'] = 0
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
            context['Login_active'] = True
            return HttpResponseRedirect('/ReaderInfo/')
        context['obj1'] = objPost
        context['Login_active'] = False
        return render(request,'Login.html', context)
    else:
        if not request.session.has_key('UserID'):
            objGet = LoginForm()
            context['obj1'] = objGet
            context['Login_active'] = False
            return render(request,'Login.html', context)
        context['Login_active'] = True
        return HttpResponseRedirect('/ReaderInfo/')

@csrf_exempt
def Logout(request):
    if request.session.has_key('username'):
        request.session.pop('username')
    return HttpResponseRedirect('/Login/')

def BorrowBookPage(request):
    context = {}
    if request.session.has_key('username'):
        context['Login_active'] = True
        context['BookSet'] = ShowAllBooks()
        return render(request, 'BorrowBookPage.html', context)
    return HttpResponseRedirect('/Login/')

def ShowAllBooks():
    bookList = Book.objects.all();
    bookSet = []
    for book in bookList:
		q={}
		q['ISBN'] = book.ISBN
		q['BookName'] = book.BookName
		q['PublishingCompany'] = book.PublishingCompany
		q['Author'] = book.Author
		q['Storage'] = book.Storage
		q['Number'] = book.Number
		q['CanBorrow'] = (book.Number > 0)
		bookSet.append(q)
    return bookSet

def ShowAllReaders():
    bookList = Reader.objects.all();
    bookSet = []
    for book in bookList:
		q={}
		q['Username'] = book.User.Username
		q['ReaderName'] = book.ReaderName
		bookSet.append(q)
    return bookSet

def ShowMyBooks(reader):
    bookList = BorrowList.objects.filter(Reader = reader).order_by('DeadLine');
    bookSet = []
    for book in bookList:
        if (timezone.now() - book.DeadLine).days > 0:
            book.Panelty = (timezone.now() - book.DeadLine).days
            book.save()
        q={}
        q['ISBN'] = book.Book.ISBN
        q['BookName'] = book.Book.BookName
        q['DeadLine'] = book.DeadLine
        q['Panelty'] = book.Panelty
        q['ListId'] = book.ListId
        bookSet.append(q)
    return bookSet

@csrf_exempt
def BorrowBook(request):
    if not request.session.has_key('username'):
        dic = {'info':'please login first!'}
        data = json.dumps(dic)
        return HttpResponse(data)
    if request.POST:
        username = request.session.get('username')
        ISBN = request.POST.get('ISBN')
        try:
            user = LibraryUser.objects.get(Username = username)
            reader = Reader.objects.get(User = user)
            book = Book.objects.get(ISBN = ISBN)
        except Exception as e:
            return HttpResponse(json.dumps({'info': str(e)}))
        if book.Number == 0:
            dic = {'info': '借书失败！\n原因：图书数量不足'}
            data = json.dumps(dic)
            return HttpResponse(data)
        if reader.Borrowed == reader.MaxBook:
            dic = {'info': '借书失败！\n原因：借书数量到达上限'}
            data = json.dumps(dic)
            return HttpResponse(data)
        try:
            BorrowList(ListId = reader.ReaderId + time.strftime("%Y%m%d%H%M%S", time.gmtime()), Reader = reader, Book = book).save()
        except Exception as e:
            return HttpResponse(json.dumps({'info': str(e)}))
        try:
            book.Number -= 1
            reader.Borrowed += 1
            book.save()
            reader.save()
        except Exception as e:
            HttpResponse(json.dumps(e))
        return HttpResponse(json.dumps({'info': 'ok'}))
    return HttpResponse('Whoops!')

@csrf_exempt
def ModifyData(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/Login/')
    if request.POST:
        ReaderName = request.POST.get('ReaderName')
        Gender = request.POST.get('Gender')
        if Gender == u'保密':
            g = 0
        elif Gender == u'男':
            g = 1
        else:
            g = 2
        username = request.session.get('username')
        user = LibraryUser.objects.get(Username = username)
        reader = Reader.objects.get(User = user)
        reader.ReaderName = ReaderName
        reader.Gender = g
        reader.save()
        return HttpResponseRedirect('/ReaderInfo/')
    return HttpResponse('Whoops!')

@csrf_exempt
def ReturnBook(request):
    if not request.session.has_key('username'):
        dic = {'info':'please login first!'}
        data = json.dumps(dic)
        return HttpResponse(data)
    if request.POST:
        user = LibraryUser.objects.get(Username = request.session.get('username'))
        if user.Type != 1:
            return HttpResponse(json.dumps({'info': '没有权限'}))
        ListId = request.POST.get('ListId')
        try:
            l = BorrowList.objects.get(ListId = ListId)
            l.Book.Number += 1
            l.Book.save()
            l.Reader.Borrowed -= 1
            l.Reader.save()
            l.delete()
        except Exception as e:
            return HttpResponse(json.dumps({'info': str(e)}))
        return HttpResponse(json.dumps({'info': 'ok'}))
    return HttpResponse('Whoops')
