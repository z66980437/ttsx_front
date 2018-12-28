
from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    # 商品详情
    url(r'^detail/(\d+)/', views.detail, name='detail'),
    # 商品分类
    url(r'^category/(\d+)/(\d+)/', views.category, name='category'),
    # 商品搜索
    url(r'^search/(.*)/(\d+)/', views.search, name='search'),

]