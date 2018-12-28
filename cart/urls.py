
from django.conf.urls import url

from cart import views

urlpatterns = [
    # 加入购物车
    url(r'add_cart/', views.add_cart, name='add_cart'),
    # 购物车
    url(r'cart/', views.cart, name='cart'),
    # 修改购物车
    url(r'change/(\d+)/', views.change_cart, name='change_cart'),

]