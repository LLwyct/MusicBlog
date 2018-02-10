# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app.models import essay,isopen,like,comment
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
import json
import time
# Create your views here.

class loginform(forms.Form):
    username = forms.CharField(label='用户名:',max_length=20)
    password = forms.CharField(label='密码:', max_length=20)

def userlogin(request):
    if request.method == 'POST':
        print("send post")
        form = loginform(request.POST)
        if form.is_valid():
            print("form.is_valid is true")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # login is successful
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    print("login successfully")
                    return HttpResponseRedirect('/index/')
                else:
                    # Return a 'disabled account' error message
                    print("not active")
        else:
            print("form.is_valid is false")
    else:
        form = loginform
    return render(request,'index.html')

def logout(requset):
    user = requset.user
    auth.logout(requset)
    return HttpResponseRedirect(requset.META['HTTP_REFERER'])

def index(request):
    blog_list = essay.objects.all().order_by('-popular')
    paginator = Paginator(blog_list,10)
    page = request.GET.get('page')
    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = paginator.page(1)
    numlist = range(1,paginator.num_pages+1)
    
    lablelist = []
    for e in blog_list:
        lablelist.append(str(e.lable).split(';')[1:])
    return render(request, 'index.html', {'posts': blog_list,'numlist':numlist,'lablelist':lablelist,'state':1})

def indexbynew(request):
    blog_list = essay.objects.all().order_by('-creatdate')
    paginator = Paginator(blog_list,10)
    page = request.GET.get('page')
    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = paginator.page(1)
    numlist = range(1,paginator.num_pages+1)
    
    lablelist = []
    for e in blog_list:
        lablelist.append(str(e.lable).split(';')[1:])
    return render(request, 'index.html', {'posts': blog_list,'numlist':numlist,'lablelist':lablelist,'state':2})

def home(request):
    return render(request, 'home.html')

def showblog(request, essay_id=''):
    likenumber = essay.objects.get(id=essay_id).like
    islike = 0
    if request.user.is_authenticated():
        felt = isopen.objects.filter(user=request.user.username,essayid=essay_id)
        if felt:
            pass
        else:
            haveopen = isopen(essayid=essay_id,user=request.user.username)
            haveopen.save()
            this_essay = essay.objects.get(id=essay_id)
            this_essay.open = this_essay.open + 1
            this_essay.popular = this_essay.like * 2 + this_essay.open
            this_essay.save()
    felt2 = like.objects.filter(user=request.user.username, essayid=essay_id)
    if felt2:
        islike = 0
    else:
        islike = 1
    blog_list = essay.objects.get(id=essay_id)
    lablelist = str(blog_list.lable).split(';')[1:]
    commentlist = comment.objects.filter(essayid=essay_id)
    
    return render(request, 'showblog.html', {'blog_content': blog_list,
                                             'lablelist':lablelist,
                                             'commentlist':commentlist,
                                             'likenumber':likenumber,
                                             'islike':islike,})

def add_essay(requset):
    if requset.user.is_authenticated():
        return render(requset,'add_essay.html')
    else:
        return render(requset,'login_state.html',{'state':'请先登录'})

def changelink(link):
    newlink1 = '<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&'
    pos = link.find('id')
    newlink2 = link[pos:]
    newlink3 = '&auto=0&height=66"></iframe>'
    return newlink1+newlink2+newlink3

def sub_essay(requset):
    if requset.method == 'POST':
        uptitle = requset.POST['essay_title']
        upcontent = requset.POST['essay_editor']
        upplatformtype = requset.POST['platformtype']
        uplink = requset.POST['musiclink']
        lable = requset.POST.getlist('lable')
        uplable = ""
        if lable:
            for e in lable:
                uplable = uplable + ';' + e
        
        #upcontent = re.sub('\\r\\n', '<br>', upcontent)
        
        upessay = essay(
            title = uptitle,
            auther=requset.user.username,
            creatdate = time.localtime(),
            content = upcontent,
            platform = upplatformtype,
            link = changelink(uplink),
            lable = uplable,
        )
        upessay.save()
        return HttpResponseRedirect('/index/')



class registerform(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', max_length=20)
    repassword = forms.CharField(label='确认密码', max_length=20)
    email = forms.CharField(label='邮箱', max_length=20)

def register(requset):
    if requset.method == 'POST':
        username = requset.POST['username']
        password = requset.POST['password']
        repassword = requset.POST['repassword']
        email = requset.POST['email']
        isexist = User.objects.filter(username__exact=username)
        if isexist:
            return render(requset,'login_state.html',{'state':'用户名已被注册'})
        else:
            user = User.objects.create_user(username, email, password)
            return HttpResponseRedirect('/index/')
    return render(requset,'register.html')

def submitcomment(requset, essay_id=''):
    if requset.method == 'POST':
        upcommentcontent = requset.POST['commentcontent']
        if len(upcommentcontent) > 0:
            upcomment = comment(
                essayid = essay_id,
                user = requset.user.username,
                commentcontent = upcommentcontent,
            )
            upcomment.save()
            return HttpResponseRedirect(requset.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect('/index/')

def likeit(requset):
    if requset.method =='POST':
        thisid = requset.POST['content_id']
        addnum = requset.POST['number']
        thisessay = essay.objects.get(id=thisid)
        if addnum == "1":
            thisessay.like = thisessay.like + 1
            thisessay.popular = thisessay.like * 2 + thisessay.open
            thisessay.save()
            thislike = like(essayid=thisid, user=requset.user.username)
            thislike.save()
        if addnum == "-1":
            thisessay.like = thisessay.like - 1
            thisessay.popular = thisessay.like*2 + thisessay.open
            thisessay.save()
            thislike = like.objects.filter(essayid=thisid, user=requset.user.username)
            if thislike:
                thislike.delete()
    return HttpResponse()

