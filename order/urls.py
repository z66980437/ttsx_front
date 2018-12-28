
from django.conf.urls import url

from order import views

urlpatterns = [
    # 下单
    url(r'^order/', views.order, name='order'),
    # 提交订单
    url(r'^submit/', views.submit, name='submit'),

    # 立即购买的下单
    url(r'noworder/', views.noworder, name='noworder'),
    # 立即购买的提交订单
    url(r'nowsubmit/(\d+)/(\d+)/', views.nowsubmit, name='nowsubmit'),

]

