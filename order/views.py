from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from cart.models import ShoppingCart
from order.models import OrderGoods, OrderInfo
from user.models import UserAddress
from goods.models import Goods

# Create your views here.


def order(request):
    if request.method == 'POST':
        # 1. 从购物车表中取出当前登录系统用户且is_select为1的商品信息
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).first()
        carts = ShoppingCart.objects.filter(user_id=user_id,
                                            is_select=1).all()
        if len(carts) == 0:
            return JsonResponse({'code': 400, 'msg': '添加失败'})
        # 计算总金额
        order_mount = 0
        for cart in carts:
            order_mount += int(cart.nums) * int(cart.goods.shop_price)
        # 2. 创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         address=user_address.province+user_address.city+user_address.district+user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile,
                                         order_mount=order_mount)
        # 3. 创建订单详情信息
        for cart in carts:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4. 删除购物车中已经下单的商品信息
        carts.delete()
        goods_list = request.session.get('goods')
        new_goods_list = []
        for i in range(len(goods_list)):
            if not goods_list[i][2]:
                new_goods_list.append(goods_list[i])
        request.session['goods'] = new_goods_list
        return JsonResponse({'code':200, 'msg': '请求成功'})

def submit(request):
    if request.method == 'GET':

        #购物车图片旁的数量
        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0
        #无选中
        flag = False
        for good in session_goods:
            if good[2]:
                flag = True
        if not flag:
            return HttpResponseRedirect(reverse('cart:cart'))

        user_id = request.session.get('user_id')
        carts = ShoppingCart.objects.filter(user_id=user_id,is_select=True)

        #新增属性
        carts.goods_nums = 0
        carts.all_price = 0
        if len(carts) == 0:
            carts.carriage = 0
        else:
            carts.carriage = 10
        carts.payment_amount = 0

        for cart in carts:
            cart.total_price = cart.nums * cart.goods.shop_price
            carts.goods_nums += cart.nums
            carts.all_price += cart.total_price
        carts.payment_amount = '%.2f'%(carts.carriage + carts.all_price)
        carts.all_price = '%.2f'%(carts.all_price)

        # 收货地址
        user_address = UserAddress.objects.filter(user_id=user_id).first()
        return render(request,'place_order.html',{'carts':carts,'goods_kind':goods_kind,'user_address':user_address})


def nowsubmit(request,goods_id,goods_nums):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=goods_id).first()
        if not goods:
            return None
        goods_total = int(goods_nums)*float(goods.shop_price)

        carriage = 0
        if not goods.ship_free:
            carriage = 10

        payment_amount = '%.2f'% (goods_total + carriage)
        goods_total = '%.2f'% (goods_total)

        # 获取用户地址
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).first()

        # 添加立即购买商品信息到session
        buynow_goods = {'goods_id':goods_id,'goods_nums':goods_nums}
        request.session['buynow_goods'] = buynow_goods


        #我的购物车商品数量
        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0

        return render(request,'buynow.html',{'goods':goods,'goods_total':goods_total,'goods_nums':goods_nums, 'carriage':carriage, 'payment_amount':payment_amount, 'user_address':user_address,'goods_kind':goods_kind})


def noworder(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).first()
        buynow_goods = request.session.get('buynow_goods')
        goods_id = buynow_goods['goods_id']
        goods_nums = buynow_goods['goods_nums']
        goods = Goods.objects.filter(pk=goods_id).first()
        # 计算总金额
        order_mount = int(goods_nums) * float(goods.shop_price)

        # 2. 创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         address=user_address.province + user_address.city + user_address.district + user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile,
                                         order_mount=order_mount)
        # 3. 创建订单详情信息
        OrderGoods.objects.create(order=order,
                                  goods=goods,
                                  goods_nums=goods_nums)
        # 4. 删除session中已经下单的立即购买的商品信息
        request.session['buynow_goods'] = {}
        return JsonResponse({'code': 200, 'msg': '请求成功'})
