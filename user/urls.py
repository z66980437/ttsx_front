
from django.conf.urls import url

from user import views

urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 注销
    url(r'^logout/', views.logout, name='logout'),
    # 个人信息
    url(r'^info/', views.info, name='info'),
    # 全部订单
    url(r'^all_orders/(\d+)/', views.all_orders, name='all_orders'),
    # 收货地址
    url(r'^address/', views.address, name='address'),

]