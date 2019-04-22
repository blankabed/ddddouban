from django.shortcuts import render
from django.shortcuts import render_to_response
from  django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from douban import models
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
import random
import time
import json
# Create your views here.

def index(request):
    return render(request,'index.html')
def login_action(request):
    if request.method == 'POST':
        # 如果登录成功，绑定参数到cookie中，set_cookie
        name = request.POST.get('username')
        password = request.POST.get('password')
        # 查询用户是否在数据库中
        if models.user.objects.filter(user=name).exists():
            user = models.user.objects.get(user=name)
            if password==user.password:
                # ticket = 'agdoajbfjad'
                ticket = ''
                for i in range(15):
                    s = 'abcdefghijklmnopqrstuvwxyz'
                    # 获取随机的字符串
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                # response = HttpResponse()
                response = HttpResponseRedirect('/event_manage/')
                # max_age 存活时间(秒)
                response.set_cookie('ticket', ticket, max_age=100)
                # 存在服务端
                user.u_ticket = ticket
                user.save()  # 保存
                return response
            else:
                # return HttpResponse('用户密码错误')
                return render(request, 'aaa.html', {'password': '用户密码错误'})
        else:
            # return HttpResponse('用户不存在')
            return render(request, 'bbb.html', {'name': '用户不存在'})
def event_manage(request):
    return render(request, "successlogin.html")

def search_movie(request):
    if request.method == 'POST':

        if 'search' in request.POST:
            from douban import models

            movie_info=models.movie.objects.all()

            searchinfo = request.POST.get('searchname','')
            # for key in keylist:
            #     if key=='moviename':
            #         post_list1 = models.movie.objects.filter(moviename__icontains=searchinfo)
            #         return render(request, 'search.html', {'post_list': post_list1})
            #     if key=='director':
            #         post_list2 = models.movie.objects.filter(moviename__icontains=searchinfo)
            #         return render(request, 'search.html', {'post_list': post_list1})
            post_list1=models.movie.objects.filter(moviename__icontains=searchinfo)
            post_list2 = models.movie.objects.filter(actoranddirector__icontains=searchinfo)
            post_list3 = models.movie.objects.filter(grade__icontains=searchinfo)
            if post_list1:
                return render(request, 'search.html', {'post_list': post_list1})
            if post_list2:
                return render(request, 'search.html', {'post_list': post_list2})
            if post_list3:
                return render(request, 'search.html', {'post_list': post_list3})
            # return  render(request,"search.html",{'movie_info':movie_info})
def register(request):
    return render(request,'register.html')
def add_user(request):
    if request.method == 'POST':
        regname=request.POST.get('username')
        regpwd=request.POST.get('login_password')
        info=models.user.objects.all().last()
        models.user.objects.create(user=regname, password=regpwd)
        return render(request,'index.html')