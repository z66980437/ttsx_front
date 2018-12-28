from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from goods.models import Goods
from order.models import OrderInfo,OrderGoods
from user.forms import UserRegisterForm
from django.contrib.auth.hashers import make_password, check_password
from user.models import User, UserAddress
from django.urls import reverse

# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        data = request.POST
        form = UserRegisterForm(data)
        if form.is_valid():
            # form表单数据无问题
            # 密码加密
            password = make_password(form.cleaned_data.get('pwd'))
            # 注册，在数据库中增加用户
            User.objects.create(username=form.cleaned_data.get('username'),password=password,email=form.cleaned_data.get('email'))


            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 有错，返回错误
            return render(request,'register.html',{'errors':form.errors})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        # 验证完整性
        if not all([username, pwd]):
            msg = '用户名或密码不全！'
            return render(request, 'login.html', {'msg_userpass':msg})
        user = User.objects.filter(username=username).first()
        # 判断用户是否存在
        if not user:
            msg = '该用户不存在！'
            return render(request, 'login.html', {'msg_username': msg})

        # 验证密码正确性
        if check_password(pwd, user.password):
            # django自带auth模块，签名token，会话上下文session
            request.session['user_id'] = user.id

            return HttpResponseRedirect(reverse('goods:index'))
        else:
            msg = '密码错误！'
            return render(request, 'login.html', {'msg_password':msg})

def logout(request):
    if request.method == 'GET':
        del request.session['user_id']
        del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))

# 个人信息
def info(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user = User.objects.filter(pk=user_id).first()
        del user.password

        # 获取最近浏览商品
        goods_history = request.session.get('goods_history')
        goods_list = []
        if goods_history:
            goods_history = goods_history[::-1]
            for i in range(len(goods_history)):
                goods = Goods.objects.filter(pk=goods_history[i]).first()
                if goods in goods_list:
                    continue
                goods_list.append(goods)
                if len(goods_list) == 5:
                    break

        return render(request,'user_center_info.html',{'user':user, 'goods_list':goods_list})


# 全部订单
def all_orders(request,page):
    if request.method == 'GET':
        orders = []
        user_id = request.session.get('user_id')
        orders = OrderInfo.objects.filter(user_id=user_id)[::-1]
        page = int(page)
        pages = len(orders) // 5
        if len(orders) % 5 > 0:
            pages += 1
        if page > pages and pages != 0:
            return None
        if page == pages:
            orders = orders[(page - 1) * 5:]
        else:
            orders = orders[(page - 1) * 5:page * 5]

        page_list = [page, range(1, pages + 1), pages]
        for i in range(len(orders)):
            orders[i].goods_order_list = orders[i].goods.all()
            for j in range(len(orders[i].goods_order_list)):
                orders[i].goods_order_list[j].goods = Goods.objects.filter(pk=orders[i].goods_order_list[j].goods_id).first()
                orders[i].goods_order_list[j].total_price = orders[i].goods_order_list[j].goods.shop_price * orders[i].goods_order_list[j].goods_nums
        return render(request,'user_center_order.html',{'orders':orders, 'page_list':page_list})


def address(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address =  UserAddress.objects.filter(user_id=user_id).first()
        return render(request,'user_center_site.html',{'user_address':user_address})


    # 修改地址
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).first()
        if not user_address:
            user_address = UserAddress()
            user_address.user_id = user_id
        user_address.signer_name = request.POST.get('signer_name')
        user_address.province = request.POST.get('province')
        user_address.city = request.POST.get('city')
        user_address.district = request.POST.get('district')
        user_address.address = request.POST.get('address')
        user_address.signer_postcode = request.POST.get('signer_postcode')
        user_address.signer_mobile = request.POST.get('signer_mobile')
        user_address.save()
        return HttpResponseRedirect(reverse('user:address'))

