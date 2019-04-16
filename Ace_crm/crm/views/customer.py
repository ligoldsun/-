from django.shortcuts import render, redirect, reverse, HttpResponse
from crm import models
from crm.utils.pagination import Pagination
from crm.forms import CustomerForm
from django.db.models import Q


def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.user_obj)
    print('---->>>', request.POST)
    return render(request, 'customer_list.html', {'all_customer': all_customer})


from django.views import View


class CustomerList(View):
    def get(self, request):
        query = request.GET.get('query', '')
        print(query)
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = self.search(['qq','name','sex'])

        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q,consultant=request.user_obj)
        return render(request, 'customer_list.html', {'all_customer': all_customer})

    def post(self, request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法请求')
        getattr(self, action)(request)
        return self.get(request)

    def muti_apply(self, request):
        ids = request.POST.getlist('ids')
        models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)

    def muti_pub(self, request):
        ids = request.POST.getlist('ids')
        models.Customer.objects.filter(pk__in=ids).update(consultant=None)

    def muti_del(self, request):
        ids = request.POST.getlist('ids')
        models.Customer.objects.filter(pk__in=ids).delete()

    def search(self,field_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('{}__contains'.format(field),query)))
        return q


# 添加客户 暂下
def add_customer(request):
    form_obj = CustomerForm()
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'add_customer.html', {'form_obj': form_obj})


# 编辑客户 暂下
def edit_customer(request, edit_id):
    form_obj = CustomerForm()
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'edit_customer.html', {'form_obj': form_obj})


# 将添加客户和编辑客户整合到一起
def customer_change(request, edit_id=None):
    form_obj = CustomerForm()
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    title = '编辑客户' if edit_id else '添加客户'
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'customer_change.html', {'form_obj': form_obj, 'title': title})


# def user_list(request):
#     userlist = [{'name': 'alex - {}'.format(i), 'pwd': 'dab - {}'.format(i)} for i in range(1, 302)]
#     page_num = request.GET.get('page','1')
#     try:
#         page_num = int(page_num)
#         if page_num <= 0:
#             page_num = 1
#     except Exception as e:
#         page_num = 1
#     total_data_num = len(userlist) #总数据条数
#     per_page = 15    #每页显示条数
#     total_page_num,more = divmod(total_data_num,per_page)
#     if more:
#         total_page_num += 1
#     max_show = 11
#     half_show = max_show // 2
#     page_start = page_num - half_show
#     page_end = page_num + half_show
#     if total_page_num >= max_show:
#         if page_start <= 0:
#             page_start = 1
#             page_end = max_show
#         elif page_end > total_page_num:
#             page_start = total_page_num - max_show + 1
#             page_end = total_page_num
#     else:
#         page_start = 1
#         page_end = total_page_num
#     start = (page_num-1) * per_page
#     end = page_num * per_page
#     #上下翻页和点击的页面效果
#     page_list = []
#     if page_num == 1:
#         page_list.append('<li class="disabled"><a >上一页</a></li>')
#     else:
#         page_list.append('<li><a href="?page={}">上一页</a></li>'.format(page_num - 1))
#     for i in range(page_start,page_end+1):
#         if i == page_num:
#             page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i,i))
#         else:
#             page_list.append('<li><a href="?page={}">{}</a></li>'.format(i,i))
#     if page_num == total_page_num:
#         page_list.append('<li class="disabled"><a>下一页</a></li>')
#     else:
#         page_list.append('<li><a href="?page={}">下一页</a></li>'.format(page_num + 1))
#     page_html = ''.join(page_list)
#     return render(request,'user_list.html',{'users':userlist[start:end],'page_html':page_html })

def user_list(request):
    userlist = [{'name': 'alex - {}'.format(i), 'pwd': 'dab - {}'.format(i)} for i in range(1, 302)]
    page = Pagination(request.GET.get('page', '1'), len(userlist), )
    return render(request, 'user_list.html', {'users': userlist[page.start:page.end], 'page_html': page.page_html})
