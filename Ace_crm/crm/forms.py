from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib


class ShowForm(forms.ModelForm):
    #给所有的框加上form-control的样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': "form-control"})

class RegForm(ShowForm):
    re_pwd = forms.CharField(widget=forms.PasswordInput,label='确认密码')

    class Meta:
        model = models.UserProfile
        fields = '__all__'  # ['username','password']
        exclude = ['memo', 'is_active']
        #修改显示名称的第二种方法
        labels = {
            'username': '用户名'
        }

        widgets = {
            'password': forms.PasswordInput(attrs={'class': "form-control", 'k1': 'v1'}),
        }
        error_messages = {
            'password':{
                'required':'必填的'
            },
            'username': {
                'required': '必填的'
            },
            'name': {
                'required': '必填的'
            },


        }


    def clean(self):
        pwd = self.cleaned_data.get('password','')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd == re_pwd:
            md5 = hashlib.md5()
            print('---->',pwd)
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            # print(pwd)
            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        self.add_error('re_pwd','两次密码不一致')
        raise ValidationError('两次密码不一致')


class CustomerForm(ShowForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        # exclude = []
    #将咨询课程中的class样式去掉
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.pop('class')

