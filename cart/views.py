from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from cart.models import ShoppingCart
from goods.models import Goods


def add_cart(request):
    if request.method == 'POST':
        # 加入到购物车，需判断用户是否登录
        # 如果登录，加入到购物车中的数据，其实就是加入到数据库中购物车表中(设计不好的办法)
        # 如果登录，加入到购物车中的数据，存储到session中（设计相对比较好的）
        # 如果没有登录，则加入到购物车中的数据，是加入到session中
        # session中存储数据: 商品id，商品数量，商品的选择状态
        # 如果登录，则把session中数据同步到数据库中（中间件同步数据）

        # 1. 获取商品id和商品数量
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get(
'goods_num'))
        # 2. 组装存到session中的数据格式
        goods_list = [goods_id,goods_num,1]
        # {'goods':[[1,2,1],[2,5,1],[5,1,1]....]}
        if request.session.get('goods'):
            # 说明session中和购物车中有商品数据
            # 判断当前加入到购物车中的数据，是否已经存在于session中
            # 如果存在，则修改session中该商品的数量
            # 如果不存在，则新增
            flag = 0
            session_goods = request.session['goods']
            for goods in session_goods:
                # 判断目前正在添加的商品是否已经在购物车中存在
                if goods[0] == goods_id:
                    # 存在
                    goods[1] = int(goods[1]) + int(goods_num)
                    flag = 1
            if not flag:
                # 不存在该商品，添加商品
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            goods_count = len(session_goods)
        else:
            # 添加商品，目前购物车为空
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            goods_count = 1

        return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_count': goods_count})

def cart(request):
    if request.method == 'GET':
        #无论是否登录都从session中取数据
        session_goods = request.session.get('goods')
        #判断购物车中是否有商品
        if session_goods:
            # 获取session中所有的商品id值
            goods_all = []
            for goods in session_goods:
                # 获取商品对象
                # 前台需要商品信息，商品的个数，商品的总价
                # 后台返回结构[[goods objects, number, total_price],[goods objects, number, total_price]]
                cart_goods = Goods.objects.filter(pk=goods[0]).first()
                goods_number = goods[1]
                total_price = goods[1] * cart_goods.shop_price
                goods_is_select = goods[2]
                goods_all.append([cart_goods, goods_number, '%.2f'%total_price,goods_is_select])
        else:
            goods_all = ''
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0
        return render(request, 'cart.html', {'goods_all': goods_all,'goods_kind':goods_kind})


def change_cart(request, option):
    if request.method == 'POST':
        print('11111')
        #改变数量
        if option == '1':
            goods_id = int(request.POST.get('goods_id'))
            goods_num = int(request.POST.get(
                'goods_num'))
            goods_list = request.session['goods']
            for i in range(len(goods_list)):
                if goods_id == goods_list[i][0]:
                    goods_list[i][1] = goods_num
            request.session['goods'] = goods_list

            user_id = request.session.get('user_id')
            if user_id:
                cart = ShoppingCart.objects.filter(user_id=user_id,
                                                   goods_id=goods_id).first()
                cart.nums = goods_num
                cart.save()
            return JsonResponse({'code': 200, 'msg': '请求成功'})
        #选择状态切换
        elif option == '2':
            goods_id = int(request.POST.get('goods_id'))
            goods_status = request.POST.get('goods_status')
            goods_list = request.session['goods']
            # 全选
            if goods_id == -1:
                if len(goods_list):
                    for i in range(len(goods_list)):
                        if goods_status == 'true':
                            goods_list[i][2] = True
                        else:
                            goods_list[i][2] = False
                    request.session['goods'] = goods_list
                    # 修改数据库
                    user_id = request.session.get('user_id')
                    if user_id:
                        carts = ShoppingCart.objects.filter(user_id=user_id)
                        for cart in carts:
                            if goods_status == 'true':
                                cart.is_select = True
                            else:
                                cart.is_select = False
                            cart.save()
                return JsonResponse({'code': 200, 'msg': '请求成功'})
            # 单选
            else:
                for i in range(len(goods_list)):
                    if goods_id == goods_list[i][0]:
                        if goods_status == 'true':
                            goods_list[i][2] = True
                        else:
                            goods_list[i][2] = False
                        break
                request.session['goods'] = goods_list

                # 修改数据库
                user_id = request.session.get('user_id')
                if user_id:
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=goods_id).first()
                    if goods_status == 'true':
                        cart.is_select = True
                    else:
                        cart.is_select = False
                    cart.save()
                return JsonResponse({'code': 200, 'msg': '请求成功'})

        #删除商品
        elif option == '3':
            goods_id = int(request.POST.get('goods_id'))
            goods_list = request.session['goods']
            for i in range(len(goods_list)):
                if goods_id == goods_list[i][0]:
                    del goods_list[i]
                    break
            request.session['goods'] = goods_list

            user_id = request.session.get('user_id')
            if user_id:
                cart = ShoppingCart.objects.filter(user_id=user_id,
                                                   goods_id=goods_id).first()
                cart.delete()
            if goods_list:
                goods_kind = len(goods_list)
            else:
                goods_kind = 0
            return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_kind':goods_kind})

    pass


