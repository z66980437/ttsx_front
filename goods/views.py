from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from goods.models import Goods, GoodsCategory
import random
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def index(request):
    if request.method == 'GET':
        categorys = GoodsCategory.CATEGORY_TYPE
        goods = Goods.objects.all()
        goods_dict = {}
        for category in categorys:
            goods_list = []
            count = 0
            for good in goods:
                # if 判断商品分类和商品对象
                if count < 4:
                    if category[0] == good.category_id and random.randint(0,1):
                        goods_list.append(good)
                        count += 1
            # {'新鲜水果':[], '羊肉': [].....}

            goods_dict[category] = goods_list

        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0
        return render(request, 'index.html', {'goods_dict': goods_dict,'goods_kind':goods_kind})


def detail(request, goods_id):
    if request.method == 'GET':
        # 查看商品详情，返回商品对象
        goods = Goods.objects.filter(pk=goods_id).first()

        # 新品推荐
        newgoods = Goods.objects.filter(is_new=1).filter(category_id=goods.category_id)
        newgoodsnum1 = random.randint(0, len(newgoods) - 1)
        newgoodsnum2 = random.randint(0, len(newgoods) - 1)
        #避免新品推荐重复
        while newgoodsnum1 == newgoodsnum2:
            newgoodsnum2 = random.randint(0, len(newgoods) - 1)
        newgoods1 = newgoods[newgoodsnum1]
        newgoods2 = newgoods[newgoodsnum2]

        #存储商品浏览记录
        goods_history = request.session.get('goods_history')
        if goods_history:
            goods_history.append(goods_id)
        else:
            goods_history = [goods_id]
        request.session['goods_history'] = goods_history

        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0

        goods.category_name = GoodsCategory.CATEGORY_TYPE[int(goods.category_id)-1][1]

        goods.goods_desc = goods.goods_desc.replace('\\n','').replace('\\','').replace('data-lazyload','src')

        return render(request, 'detail.html', {'goods': goods,'newgoods1':newgoods1,'newgoods2':newgoods2,'goods_kind':goods_kind})


def category(request, category_id, page):
    if request.method == 'GET':
        page=int(page)

        all_goods = Goods.objects.filter(category_id=category_id).all()
        paginator = Paginator(all_goods, 20)

        try:
            goods_list = paginator.page(int(page))
        except PageNotAnInteger:
            goods_list = paginator.page(1)
        except EmptyPage:
            goods_list = paginator.page(paginator.num_pages)

        page = int(page)
        if paginator.num_pages < 8:
            page_list = range(1, paginator.num_pages + 1)
        else:
            if page <= 3:
                page_list = range(1, 8)
            elif page >= paginator.num_pages - 2:
                page_list = range(paginator.num_pages - 5, paginator.num_pages + 1)
            else:
                page_list = range(page - 3, page + 4)

        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0
        return render(request,'category.html',{'goods_list':goods_list,'goods_kind':goods_kind,'page':page,'page_list':page_list,'max_page':paginator.num_pages,'category_id':category_id})


def search(request,name,page):
    if request.method == 'GET':
        #判断搜索是否为空
        if not name:
            return HttpResponseRedirect(reverse('goods:index'))

        all_goods = Goods.objects.filter(Q(name__icontains=name) | Q(goods_brief__icontains=name) | Q(goods_desc__icontains=name)).all()
        paginator = Paginator(all_goods, 20)

        try:
            goods_list = paginator.page(int(page))
        except PageNotAnInteger:
            goods_list = paginator.page(1)
        except EmptyPage:
            goods_list = paginator.page(paginator.num_pages)

        page = int(page)
        if paginator.num_pages < 8:
            page_list = range(1, paginator.num_pages + 1)
        else:
            if page <= 3:
                page_list = range(1, 8)
            elif page >= paginator.num_pages - 2:
                page_list = range(paginator.num_pages - 5, paginator.num_pages + 1)
            else:
                page_list = range(page - 3, page + 4)

        session_goods = request.session.get('goods')
        if session_goods:
            goods_kind = len(session_goods)
        else:
            goods_kind = 0
        return render(request,'search.html',{'goods_list':goods_list,'goods_kind':goods_kind,'page':page,'page_list':page_list,'max_page':paginator.num_pages,'name':name})


