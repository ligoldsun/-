from django.shortcuts import render,redirect,reverse,HttpResponse
from crm import models
from crm.forms import RegForm
from crm.utils.pagination import Pagination
import hashlib

def index(request):
    return HttpResponse('登录成功')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()
        obj = models.UserProfile.objects.filter(username=user,password=pwd).first()
        if obj:
            request.session['pk'] = obj.pk
            return redirect(reverse('customer_list'))
        # else:
        #     return HttpResponse('登录失败')

    return render(request,'login.html')

def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # form_obj.cleaned_data.pop('re_pwd')  #方法1存入数据库
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            form_obj.save()   #方法2.存入数据库
            return redirect(reverse('login'))
    return render(request,'reg.html',{'form_obj':form_obj})


