from django.conf.urls import url,include
from crm.views import customer
urlpatterns = [
    #公户
    url(r'customer_list/',customer.CustomerList.as_view(),name='customer_list'),
    #私户
    url(r'my_customer/',customer.CustomerList.as_view(),name='my_customer'),
    # url(r'user_list/',customer.user_list,name='user_list'),
    url(r'add_customer/',customer.customer_change,name='add_customer'),
    url(r'edit_customer/(\d+)',customer.edit_customer,name='edit_customer'),
]
