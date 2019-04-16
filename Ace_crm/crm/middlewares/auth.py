# from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.deprecation import MiddlewareMixin
from crm import models
from django.shortcuts import render,reverse,redirect
class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #拿到id,获取到对象
        if request.path_info in [reverse('login'),reverse('reg')]:
            return
        pk = request.session.get('pk')
        obj = models.UserProfile.objects.filter(pk=pk).first()
        if obj:
            request.user_obj = obj
            return
        return redirect(reverse('login'))